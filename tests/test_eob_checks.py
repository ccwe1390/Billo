"""Plain-assert tests for app/eob_checks.py. Run from repo root: py tests/test_eob_checks.py

Set EOB_CHECKS_PATH to a file to test that file instead of app/eob_checks.py (used for mutation checks).
"""
import copy
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))

from app import checks

_path = os.environ.get("EOB_CHECKS_PATH")
if _path:
    _spec = importlib.util.spec_from_file_location("eob_checks_under_test", _path)
    eob_checks = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(eob_checks)
else:
    from app import eob_checks

BANNED = ("savings", "error confirmed", "illegal", "your rights")
VUMC = "Vanderbilt University Medical Center (SYNTHETIC)"
PLAN = "Example Health Plan (SYNTHETIC)"


def fld(v):
    return {"value": v, "confidence": 0.9, "confirmed": True}


def bline(desc, amt, date=None):
    return {"date": date, "description": desc, "quantity": 1, "amount_cents": amt}


def eline(desc, billed, owes, date=None):
    return {"date": date, "description": desc, "amount_billed_cents": billed, "patient_owes_cents": owes}


def make_bill(dos, hospital, insurance, due, items, total, payments, confirmed=True):
    return {
        "fields": {
            "date_of_service": fld(dos), "hospital_name": fld(hospital),
            "insurance_status": fld(insurance), "amount_due_cents": fld(due),
        },
        "lines": {"items": items, "total_charges_cents": total, "payments_cents": payments,
                  "confirmed": confirmed, "read": True},
    }


def make_eob(dos, provider, claim, status, billed, disc, paid, owes, items=None, confirmed=True,
             reason=None, deadline=None, phone=None):
    return {
        "fields": {
            "insurer_name": fld(PLAN), "provider_name": fld(provider), "date_of_service": fld(dos),
            "claim_number": fld(claim), "claim_status": fld(status),
            "amount_billed_cents": fld(billed), "plan_discount_cents": fld(disc),
            "plan_paid_cents": fld(paid), "patient_owes_cents": fld(owes),
            "denial_reason": fld(reason), "appeal_deadline": fld(deadline), "insurer_phone": fld(phone),
        },
        "lines": ({"items": items, "confirmed": confirmed, "read": True} if items is not None else None),
    }


def pair06(eob_dos="2026-09-12"):
    bill = make_bill(
        "2026-09-12", VUMC, "insured", 158500,
        [bline("ED visit, high complexity", 264000), bline("CT scan, head, without contrast", 138500),
         bline("CT scan, head, without contrast", 138500), bline("Blood test panel", 41240)],
        582240, 423740)
    eob = make_eob(
        eob_dos, VUMC, "CLM-SYN-0612", "paid", 443740, 223740, 200000, 20000,
        [eline("ER VISIT LVL 5", 264000, 20000), eline("CT HEAD W/O CONTRAST", 138500, 0),
         eline("COMPREHENSIVE METABOLIC PANEL", 41240, 0)])
    return bill, eob


def pair07():
    bill = make_bill("2026-10-03", VUMC, "insured", 220600, [bline("Hospital stay", 220600)], 220600, 0)
    eob = make_eob("2026-10-03", VUMC, None, "pending", None, None, None, None)
    return bill, eob


def pair08():
    bill = make_bill("2026-09-20", VUMC, "insured", 185850, [bline("MRI", 185850)], 185850, 0)
    eob = make_eob(
        "2026-09-20", VUMC, "CLM-SYN-0822", "denied", 185850, 0, 0, 185850,
        reason="Prior authorization was not obtained for this service.",
        deadline="2027-03-18", phone="(800) 555-0199")
    return bill, eob


def pair10():
    bill = make_bill("2026-09-12", VUMC, "insured", 35000, [bline("ED visit", 264000)], 264000, 229000)
    eob = make_eob("2026-09-12", VUMC, "CLM-SYN-0912", "paid", 264000, 119000, 110000, 35000,
                   [eline("ER VISIT LVL 5", 264000, 35000)])
    return bill, eob


def ids(r, kind=None):
    return [f["id"] for f in r["flags"] if kind is None or f["kind"] == kind]


def ins_flags(r):
    return [f for f in r["flags"] if f["kind"] == "insurance"]


def ins_ids(r):
    return ids(r, "insurance")


def flag(r, id_):
    found = [f for f in r["flags"] if f["id"] == id_]
    assert len(found) == 1, (id_, ids(r))
    return found[0]


def set_field(doc, name, value):
    doc["fields"][name] = fld(value)


def test_pair06_demo():
    bill, eob = pair06()
    r = eob_checks.run(bill, eob)
    assert ins_ids(r) == ["charged_more", "totals_mismatch", "billed_more"], ins_ids(r)
    cm = flag(r, "charged_more")
    assert cm["amount_cents"] == 138500 and cm["line_indexes"] == [1, 2], cm
    assert cm["text_en"] == ('"CT scan, head, without contrast" for $1,385.00 on 2026-09-12 is on this bill '
                             "2 times, but your insurer's summary lists it 1 time.")
    assert cm["letter_en"] == ('"CT scan, head, without contrast" for $1,385.00 on 2026-09-12 is listed 2 times '
                               "on this bill, but my insurer's explanation of benefits lists it 1 time. "
                               "Please remove the extra charge.")
    tm = flag(r, "totals_mismatch")
    assert tm["amount_cents"] is None and tm["line_indexes"] == []
    assert tm["text_en"] == ("This bill's total charges are $5,822.40, but your insurer's summary shows "
                             "$4,437.40 billed for this visit.")
    assert tm["letter_en"] == ("This bill's total charges are $5,822.40, but my insurer's explanation of benefits "
                               "shows $4,437.40 billed for this visit. "
                               "Please tell me which charges were sent to my insurance.")
    bm = flag(r, "billed_more")
    assert bm["amount_cents"] == 138500 and bm["line_indexes"] == []
    assert bm["text_en"] == ("Your insurer's summary says you owe $200.00 for this visit, but this bill asks for "
                             "$1,585.00. That is $1,385.00 to ask the hospital about.")
    assert bm["letter_en"] == ("My insurer's explanation of benefits for this visit (claim CLM-SYN-0612) says I owe "
                               "$200.00, but this bill says $1,585.00. Please correct the bill to match.")
    assert "credit_mismatch" not in ids(r) and "not_on_eob" not in ids(r)
    assert "duplicate" not in ids(r), ids(r)          # Phase 2 duplicate dropped
    assert ids(r) == ["charged_more", "totals_mismatch", "billed_more"]
    assert r["total_to_ask_cents"] == 138500, r["total_to_ask_cents"]   # not 277000
    assert r["lines_checked"] is True and r["insurer_letter"] is None
    for f in ins_flags(r):
        assert f["citation"] is None and isinstance(f["line_indexes"], list)


def test_pair06_credit_mismatch():
    bill, eob = pair06()
    bill["lines"]["payments_cents"] = 423740 - 101      # one cent over the allowance
    r = eob_checks.run(bill, eob)
    assert "credit_mismatch" in ids(r)
    f = flag(r, "credit_mismatch")
    assert f["amount_cents"] is None
    assert f["text_en"] == ("Your insurer says it paid $2,000.00 and took off a plan discount of $2,237.40 "
                            "($4,237.40 in all), but this bill shows $4,236.39 in payments and adjustments.")
    assert f["letter_en"] == ("My insurer says it paid $2,000.00 and applied a plan discount of $2,237.40, "
                              "a total of $4,237.40, but this bill shows $4,236.39 in payments and adjustments. "
                              "Please apply the full insurance payment and discount.")
    bill["lines"]["payments_cents"] = 423740 - 100       # exactly the allowance: quiet
    assert "credit_mismatch" not in ids(eob_checks.run(bill, eob))
    # discount None counts as 0: payments equal plan_paid alone -> quiet
    bill2, eob2 = pair06()
    bill2["lines"]["payments_cents"] = 200000
    set_field(eob2, "plan_discount_cents", None)
    assert "credit_mismatch" not in ids(eob_checks.run(bill2, eob2))


def test_pair07_pending():
    bill, eob = pair07()
    p2 = checks.run(bill)
    assert ids(p2) == ["insurance_unpaid"], ids(p2)
    r = eob_checks.run(bill, eob)
    assert ins_ids(r) == ["pending"], ins_ids(r)
    assert "insurance_unpaid" in ids(r, "bill")
    assert r["total_to_ask_cents"] == p2["total_to_ask_cents"]
    f = flag(r, "pending")
    assert f["text_en"] == "Your insurance is still processing this visit. Ask the hospital whether you can wait for your insurer's summary before paying."
    assert f["letter_en"] == ("My insurance claim for this visit is still being processed. Please hold this bill "
                              "until it is finished and send me a corrected bill.")
    assert f["amount_cents"] is None and f["citation"] is None and f["line_indexes"] == []
    # not_yet with no EOB at all
    r2 = eob_checks.run(bill, None, not_yet=True)
    assert ins_ids(r2) == ["pending"] and "insurance_unpaid" in ids(r2, "bill")
    assert r2["total_to_ask_cents"] == p2["total_to_ask_cents"] and r2["insurer_letter"] is None
    # not_yet beats a paid EOB: no other insurance rule runs
    bill6, eob6 = pair06()
    r3 = eob_checks.run(bill6, eob6, not_yet=True)
    assert ins_ids(r3) == ["pending"], ins_ids(r3)
    assert "duplicate" in ids(r3, "bill")
    assert r3["total_to_ask_cents"] == checks.run(bill6)["total_to_ask_cents"]
    # pending status with a different-visit date: pending wins, no different_visit
    bill7, eob7 = pair07()
    set_field(eob7, "date_of_service", "2026-01-01")
    assert ins_ids(eob_checks.run(bill7, eob7)) == ["pending"]


def test_pair08_denied():
    bill, eob = pair08()
    p2 = checks.run(bill)
    assert ids(p2) == ["insurance_unpaid"] and p2["total_to_ask_cents"] == 0
    r = eob_checks.run(bill, eob)
    assert ins_ids(r) == ["denied"], ins_ids(r)
    assert "insurance_unpaid" not in ids(r)
    assert r["total_to_ask_cents"] == 0
    f = flag(r, "denied")
    assert f["amount_cents"] is None
    assert f["text_en"] == ('Your insurer denied this claim. Reason printed on your summary: '
                            '"Prior authorization was not obtained for this service.". '
                            'Appeal by 2027-03-18. Insurer phone: (800) 555-0199.')
    assert f["letter_en"] == ("My insurer denied this claim, and I am asking them to reconsider. "
                              "Please hold this bill while that review is open.")
    assert r["insurer_letter"] == {
        "insurer_name": PLAN, "claim_number": "CLM-SYN-0822", "date_of_service": "2026-09-20",
        "provider_name": VUMC, "denial_reason": "Prior authorization was not obtained for this service.",
        "appeal_deadline": "2027-03-18", "insurer_phone": "(800) 555-0199"}


def test_denied_variants():
    # no reason / deadline / phone: bare sentence, letter fields None
    bill, eob = pair08()
    for k in ("denial_reason", "appeal_deadline", "insurer_phone", "claim_number"):
        set_field(eob, k, None)
    r = eob_checks.run(bill, eob)
    assert flag(r, "denied")["text_en"] == "Your insurer denied this claim."
    assert r["insurer_letter"]["denial_reason"] is None and r["insurer_letter"]["claim_number"] is None
    assert set(r["insurer_letter"]) == {"insurer_name", "claim_number", "date_of_service", "provider_name",
                                        "denial_reason", "appeal_deadline", "insurer_phone"}
    # due == billed - 100: still denied; billed - 101: the bill asks for less, no insurance flags
    bill, eob = pair08()
    bill["fields"]["amount_due_cents"] = fld(185850 - 100)
    assert ins_ids(eob_checks.run(bill, eob)) == ["denied"]
    bill["fields"]["amount_due_cents"] = fld(185850 - 101)
    r = eob_checks.run(bill, eob)
    assert ins_ids(r) == [] and r["insurer_letter"] is None, ins_ids(r)
    # bill asks for more than denied amount: still denied, and no money flags
    bill, eob = pair08()
    bill["fields"]["amount_due_cents"] = fld(999999)
    r = eob_checks.run(bill, eob)
    assert ins_ids(r) == ["denied"] and r["insurer_letter"] is not None
    # a missing due or billed: nothing to compare, no flag
    bill, eob = pair08()
    set_field(eob, "amount_billed_cents", None)
    assert ins_ids(eob_checks.run(bill, eob)) == []
    bill, eob = pair08()
    bill["fields"]["amount_due_cents"] = fld(None)
    assert ins_ids(eob_checks.run(bill, eob)) == []
    # denied does not run the money rules (totals differ here)
    bill, eob = pair08()
    bill["lines"]["total_charges_cents"] = 1
    assert ins_ids(eob_checks.run(bill, eob)) == ["denied"]


def test_pair09_different_visit():
    bill, eob = pair06("2026-08-02")
    p2 = checks.run(bill)
    r = eob_checks.run(bill, eob)
    assert ins_ids(r) == ["different_visit"], ins_ids(r)
    assert "duplicate" in ids(r, "bill")
    assert r["total_to_ask_cents"] == p2["total_to_ask_cents"] == 138500
    f = flag(r, "different_visit")
    assert f["letter_en"] is None and f["amount_cents"] is None
    assert f["text_en"] == ("This insurance summary is for a different visit (date of service 2026-08-02, "
                            "Vanderbilt University Medical Center (SYNTHETIC)). "
                            "Ask your insurer for the summary for 2026-09-12.")


def test_different_visit_conditions():
    # unpaid-insurance flag is kept for a different visit
    bill, eob = pair08()
    set_field(eob, "date_of_service", "2026-01-01")
    r = eob_checks.run(bill, eob)
    assert ins_ids(r) == ["different_visit"] and "insurance_unpaid" in ids(r, "bill")
    assert r["insurer_letter"] is None
    # missing date on one side is not a mismatch
    bill, eob = pair10()
    set_field(eob, "date_of_service", None)
    assert "different_visit" not in ins_ids(eob_checks.run(bill, eob))
    bill, eob = pair10()
    bill["fields"]["date_of_service"] = fld(None)
    assert "different_visit" not in ins_ids(eob_checks.run(bill, eob))
    # different provider and a missing EOB date: "unknown" wording
    bill, eob = pair10()
    set_field(eob, "date_of_service", None)
    set_field(eob, "provider_name", "Ascension Saint Thomas West (SYNTHETIC)")
    f = flag(eob_checks.run(bill, eob), "different_visit")
    assert f["text_en"] == ("This insurance summary is for a different visit (date of service unknown, "
                            "Ascension Saint Thomas West (SYNTHETIC)). Ask your insurer for the summary "
                            "for 2026-09-12.")
    # unknown status still gets the different_visit check
    bill, eob = pair10()
    set_field(eob, "claim_status", "processing")
    set_field(eob, "date_of_service", "2026-01-01")
    assert ins_ids(eob_checks.run(bill, eob)) == ["different_visit"]


def test_provider_matching():
    def verdict(hospital, provider):
        bill, eob = pair10()
        bill["fields"]["hospital_name"] = fld(hospital)
        set_field(eob, "provider_name", provider)
        return "different_visit" in ins_ids(eob_checks.run(bill, eob))

    assert not verdict("Vanderbilt University Medical Center", "VANDERBILT UNIVERSITY MEDICAL CENTER (SYNTHETIC)")
    assert not verdict("VANDERBILT UNIVERSITY MEDICAL CENTER (SYNTHETIC)", "Vanderbilt University Medical Center")
    assert not verdict("Vanderbilt University Medical Center", "Vanderbilt University Medical Center - Adult Hospital")
    assert not verdict("Vanderbilt University Medical Center Adult Hospital", "Vanderbilt University Medical Center")
    assert verdict("Ascension Saint Thomas West (SYNTHETIC)", "Vanderbilt University Medical Center")
    assert verdict(VUMC, "Ascension Saint Thomas West (SYNTHETIC)")
    assert verdict("Mercy", "Mercyland Hospital")                    # prefix needs a word boundary
    assert verdict("Foo Synthetic Hospital", "Mercy") and not verdict("Foo Synthetic Hospital", "Foo Hospital")
    assert not verdict("St. Mary's  Hospital", "ST MARY S HOSPITAL")  # punctuation and spacing do not matter
    # shortcut documented in the module: an abbreviation reads as a different visit
    assert verdict("Vanderbilt University Medical Center", "VANDERBILT UNIV MED CTR")
    # one name missing: not a mismatch
    assert not verdict(None, "Mercy") and not verdict("Mercy", None)


def test_pair10_clean():
    bill, eob = pair10()
    p2 = checks.run(bill)
    assert p2["flags"] == [] and p2["total_to_ask_cents"] == 0
    r = eob_checks.run(bill, eob)
    assert r["flags"] == [] and r["total_to_ask_cents"] == 0, r
    assert r["lines_checked"] is True and r["insurer_letter"] is None


def test_rule1_no_eob():
    bill, _ = pair06()
    p2 = checks.run(bill)
    r = eob_checks.run(bill)
    assert ids(r) == ["duplicate"] and r["flags"][0]["kind"] == "bill"
    assert r["total_to_ask_cents"] == p2["total_to_ask_cents"] == 138500
    assert r["lines_checked"] is True and r["insurer_letter"] is None
    assert {k: v for k, v in r["flags"][0].items() if k != "kind"} == p2["flags"][0]


def test_p2_passed_in_and_not_mutated():
    bill, eob = pair06()
    p2 = checks.run(bill)
    snap = copy.deepcopy(p2)
    bill_snap, eob_snap = copy.deepcopy(bill), copy.deepcopy(eob)
    r = eob_checks.run(bill, eob, p2=p2)
    assert p2 == snap, "p2 was mutated"
    assert bill == bill_snap and eob == eob_snap
    assert all("kind" not in f for f in p2["flags"])
    # a supplied p2 is used as is (not recomputed)
    fake = {"flags": [], "total_to_ask_cents": 4242, "lines_checked": False}
    r = eob_checks.run(bill, None, p2=fake)
    assert r["flags"] == [] and r["total_to_ask_cents"] == 4242 and r["lines_checked"] is False
    r = eob_checks.run(bill, None, not_yet=True, p2=fake)
    assert r["total_to_ask_cents"] == 4242 and ins_ids(r) == ["pending"]
    # r's bill flags are copies: editing them leaves p2 alone
    r = eob_checks.run(bill, eob, p2=p2)
    for f in r["flags"]:
        f["line_indexes"].append(99)
    assert p2 == snap


def test_decoy_same_amount_other_date():
    bill = make_bill("2026-09-12", VUMC, "insured", 6000,
                     [bline("Lab", 5000, "2026-09-12"), bline("Lab", 5000, "2026-09-13")], 10000, 4000)
    eob = make_eob("2026-09-12", VUMC, "C1", "paid", 5000, 0, 4000, 1000,
                   [eline("LAB", 5000, 1000, "2026-09-12")])
    r = eob_checks.run(bill, eob)
    assert ins_ids(r) == ["not_on_eob", "totals_mismatch", "billed_more"], ins_ids(r)
    f = flag(r, "not_on_eob")
    assert f["line_indexes"] == [1] and f["amount_cents"] == 5000
    assert f["text_en"] == '"Lab" for $50.00 on 2026-09-13 is on this bill but not on your insurer\'s summary.'
    assert f["letter_en"] == ('"Lab" for $50.00 on 2026-09-13 is on this bill but not on my insurer\'s '
                              "explanation of benefits. Please explain this charge or remove it.")
    assert "charged_more" not in ids(r)
    # a line with no date takes the document's date of service: matches the dated EOB line
    bill["lines"]["items"][1]["date"] = None
    bill["fields"]["date_of_service"] = fld("2026-09-12")
    assert "not_on_eob" not in ids(eob_checks.run(bill, eob))


def test_not_on_eob_counts_each_line():
    bill = make_bill("2026-09-12", VUMC, "insured", 10000,
                     [bline("Saline", 700), bline("Gauze", 700), bline("Lab", 5000)], 6400, 0)
    eob = make_eob("2026-09-12", VUMC, "C1", "paid", 6400, 0, 6400, 0, [eline("LAB", 5000, 0)])
    r = eob_checks.run(bill, eob)
    nf = [f for f in r["flags"] if f["id"] == "not_on_eob"]
    assert [f["line_indexes"] for f in nf] == [[0], [1]] and [f["amount_cents"] for f in nf] == [700, 700]
    assert "charged_more" not in ids(r)


def test_charged_more_counts():
    # bill 3 copies, EOB 1: extra = 2 x amount; EOB 3 copies: quiet; EOB 2 copies: 1 extra
    def go(n_eob):
        bill = make_bill("2026-09-12", VUMC, "insured", 0, [bline("X", 100)] * 3, 300, 300)
        eob = make_eob("2026-09-12", VUMC, "C1", "paid", 100 * n_eob, 0, 300, 0,
                       [eline("X", 100, 0)] * n_eob)
        return eob_checks.run(bill, eob)
    r = go(1)
    f = flag(r, "charged_more")
    assert f["amount_cents"] == 200 and f["line_indexes"] == [0, 1, 2]
    assert "lists it 1 time." in f["text_en"]
    assert flag(go(2), "charged_more")["amount_cents"] == 100
    assert "lists it 2 times." in flag(go(2), "charged_more")["text_en"]
    assert "charged_more" not in ids(go(3))


def test_duplicate_kept_when_eob_also_lists_it_twice():
    # A is on the bill twice and on the EOB twice (a real repeat); B is on the bill twice, on the EOB once
    bill = make_bill("2026-09-12", VUMC, "insured", 500,
                     [bline("A", 1000), bline("A", 1000), bline("B", 500), bline("B", 500)], 3000, 2500)
    eob = make_eob("2026-09-12", VUMC, "C1", "paid", 2500, 0, 2500, 500,
                   [eline("A", 1000, 0), eline("A", 1000, 0), eline("B", 500, 0)])
    r = eob_checks.run(bill, eob)
    assert ids(r, "bill") == ["duplicate"], ids(r, "bill")
    assert r["flags"][0]["line_indexes"] == [0, 1]
    assert flag(r, "charged_more")["line_indexes"] == [2, 3]


def test_totals_boundary():
    for diff, expect in ((99, False), (100, False), (101, True), (-99, False), (-101, True)):
        bill, eob = pair10()
        bill["lines"]["total_charges_cents"] = 264000 + diff
        bill["lines"]["items"][0]["amount_cents"] = 264000 + diff     # keep Phase 2 quiet
        bill["fields"]["amount_due_cents"] = fld(35000 + diff)
        bill["lines"]["payments_cents"] = 229000
        set_field(eob, "patient_owes_cents", 35000 + diff)             # keep billed_more quiet
        r = eob_checks.run(bill, eob)
        assert ("totals_mismatch" in ids(r)) is expect, (diff, ids(r))


def test_billed_more_boundary():
    for extra, expect in ((0, False), (100, False), (101, True)):
        bill, eob = pair10()
        bill["fields"]["amount_due_cents"] = fld(35000 + extra)
        bill["lines"]["payments_cents"] = 229000 - extra
        r = eob_checks.run(bill, eob)
        assert ("billed_more" in ids(r)) is expect, (extra, ids(r))
        if expect:
            assert flag(r, "billed_more")["amount_cents"] == 101
    # claim number missing: letter drops the "(claim ...)" part
    bill, eob = pair10()
    bill["fields"]["amount_due_cents"] = fld(50000)
    bill["lines"]["payments_cents"] = 214000
    set_field(eob, "claim_number", None)
    assert flag(eob_checks.run(bill, eob), "billed_more")["letter_en"] == (
        "My insurer's explanation of benefits for this visit says I owe $350.00, "
        "but this bill says $500.00. Please correct the bill to match.")
    # owes above due: no flag
    bill, eob = pair10()
    set_field(eob, "patient_owes_cents", 99999)
    assert "billed_more" not in ids(eob_checks.run(bill, eob))


def test_partially_paid_and_status_spelling():
    bill, eob = pair06()
    base = eob_checks.run(bill, eob)
    for spelling in ("partially_paid", " PAID ", "Partially_Paid"):
        b2, e2 = pair06()
        set_field(e2, "claim_status", spelling)
        assert eob_checks.run(b2, e2) == base, spelling
    b2, e2 = pair06()
    set_field(e2, "claim_status", "PENDING ")
    assert ins_ids(eob_checks.run(b2, e2)) == ["pending"]
    b3, e3 = pair08()
    set_field(e3, "claim_status", "Denied")
    assert ins_ids(eob_checks.run(b3, e3)) == ["denied"]


def test_unknown_status():
    for status in ("processing", None, "", "partially paid", "paid in full"):
        bill, eob = pair06()
        set_field(eob, "claim_status", status)
        p2 = checks.run(bill)
        r = eob_checks.run(bill, eob)
        assert ins_ids(r) == [], (status, ins_ids(r))
        assert ids(r) == ids(p2) and r["total_to_ask_cents"] == p2["total_to_ask_cents"]
        assert r["insurer_letter"] is None
    # insurance_unpaid stays when the status is unknown
    bill, eob = pair07()
    set_field(eob, "claim_status", "processing")
    assert "insurance_unpaid" in ids(eob_checks.run(bill, eob))


def test_eob_lines_not_confirmed():
    bill, eob = pair06()
    eob["lines"]["confirmed"] = False
    r = eob_checks.run(bill, eob)
    assert ins_ids(r) == ["totals_mismatch", "billed_more"], ins_ids(r)
    assert "duplicate" in ids(r, "bill")          # no charged_more, so Phase 2 duplicate stays
    assert r["total_to_ask_cents"] == 138500
    # bill lines not confirmed: same
    bill, eob = pair06()
    bill["lines"]["confirmed"] = False
    r = eob_checks.run(bill, eob)
    assert "charged_more" not in ids(r) and "not_on_eob" not in ids(r)
    assert "totals_mismatch" in ids(r) and "billed_more" in ids(r)
    # EOB with no lines at all, or an empty list
    bill, eob = pair06()
    eob["lines"] = None
    assert ins_ids(eob_checks.run(bill, eob)) == ["totals_mismatch", "billed_more"]
    bill, eob = pair06()
    eob["lines"]["items"] = []
    assert ins_ids(eob_checks.run(bill, eob)) == ["totals_mismatch", "billed_more"]
    bill, eob = pair06()
    bill["lines"] = None
    assert ins_ids(eob_checks.run(bill, eob)) == ["billed_more"]


def test_unpaid_flag_dropped_for_paid():
    for status in ("paid", "partially_paid"):
        bill = make_bill("2026-09-12", VUMC, "insured", 220600, [bline("Stay", 220600)], 220600, 0)
        eob = make_eob("2026-09-12", VUMC, "C1", status, 220600, 0, 200600, 20000,
                       [eline("STAY", 220600, 20000)])
        assert "insurance_unpaid" in ids(checks.run(bill))
        r = eob_checks.run(bill, eob)
        assert "insurance_unpaid" not in ids(r), (status, ids(r))


def test_total_rule():
    # due - owes, not Phase 2's total and not the sum of flag amounts
    bill, eob = pair06()
    set_field(eob, "patient_owes_cents", 40000)
    r = eob_checks.run(bill, eob)
    assert r["total_to_ask_cents"] == 118500, r["total_to_ask_cents"]
    assert checks.run(bill)["total_to_ask_cents"] == 138500
    # due within the allowance of owes: 0 even though Phase 2 still asks for something
    bill, eob = pair06()
    bill["fields"]["amount_due_cents"] = fld(20100)
    bill["lines"]["payments_cents"] = 582240 - 20100
    r = eob_checks.run(bill, eob)
    assert checks.run(bill)["total_to_ask_cents"] > 0
    assert r["total_to_ask_cents"] == 0, r["total_to_ask_cents"]
    # due below owes: 0
    bill, eob = pair06()
    bill["fields"]["amount_due_cents"] = fld(100)
    assert eob_checks.run(bill, eob)["total_to_ask_cents"] == 0
    # owes or due missing: Phase 2's total
    for which in ("owes", "due"):
        bill, eob = pair06()
        if which == "owes":
            set_field(eob, "patient_owes_cents", None)
        else:
            bill["fields"]["amount_due_cents"] = fld(None)
        assert eob_checks.run(bill, eob)["total_to_ask_cents"] == checks.run(bill)["total_to_ask_cents"]
    # non-paid statuses never use the rule
    bill, eob = pair06()
    set_field(eob, "patient_owes_cents", 40000)
    set_field(eob, "claim_status", "processing")
    assert eob_checks.run(bill, eob)["total_to_ask_cents"] == checks.run(bill)["total_to_ask_cents"]


def test_flag_shape_and_order():
    bill, eob = pair06()
    eob["lines"]["confirmed"] = False
    bill["lines"]["items"][3]["amount_cents"] = 41241     # make Phase 2 add lines_sum
    r = eob_checks.run(bill, eob)
    kinds = [f["kind"] for f in r["flags"]]
    assert kinds == sorted(kinds), kinds                   # "bill" flags first, then "insurance"
    for f in r["flags"]:
        assert set(f) == {"id", "text_en", "letter_en", "amount_cents", "line_indexes", "citation", "kind"}, f


def test_none_safety():
    def variants():
        for k in ("amount_due_cents", "date_of_service", "hospital_name", "insurance_status"):
            b, e = pair06()
            b["fields"][k] = fld(None)
            yield b, e
        for k in ("total_charges_cents", "payments_cents"):
            b, e = pair06()
            b["lines"][k] = None
            yield b, e
        for i in range(4):
            b, e = pair06()
            b["lines"]["items"][i]["amount_cents"] = None
            yield b, e
            b, e = pair06()
            b["lines"]["items"][i]["description"] = ""
            yield b, e
        for k in ("insurer_name", "provider_name", "date_of_service", "claim_number", "claim_status",
                  "amount_billed_cents", "plan_discount_cents", "plan_paid_cents", "patient_owes_cents",
                  "denial_reason", "appeal_deadline", "insurer_phone"):
            b, e = pair06()
            e["fields"][k] = fld(None)
            yield b, e
            b, e = pair08()
            e["fields"][k] = fld(None)
            yield b, e
        for i in range(3):
            for k in ("amount_billed_cents", "patient_owes_cents", "description", "date"):
                b, e = pair06()
                e["lines"]["items"][i][k] = None
                yield b, e
        b, e = pair06()
        b["lines"] = None
        e["lines"] = None
        yield b, e
        b, e = pair06()
        b["fields"] = {}
        e["fields"] = {}
        yield b, e
        b, e = pair06()
        e["fields"].pop("claim_status")
        yield b, e

    n = 0
    for b, e in variants():
        for kwargs in ({}, {"not_yet": True}):
            r = eob_checks.run(b, e, **kwargs)
            assert set(r) == {"flags", "total_to_ask_cents", "lines_checked", "insurer_letter"}
            assert isinstance(r["total_to_ask_cents"], int) and r["total_to_ask_cents"] >= 0
            n += 1
        r = eob_checks.run(b, None)
        assert r["insurer_letter"] is None
    assert n > 60, n


def all_texts():
    cases = []
    for build in (pair06, pair07, pair08, pair10):
        bill, eob = build()
        cases.append((bill, eob, False))
    bill, eob = pair06("2026-08-02")
    cases.append((bill, eob, False))
    bill, eob = pair06()
    cases.append((bill, None, True))
    cases.append((bill, None, False))
    b, e = pair06()
    b["lines"]["payments_cents"] = 1
    cases.append((b, e, False))
    b, e = pair06()
    e["fields"]["claim_number"] = fld(None)
    cases.append((b, e, False))
    b = make_bill("2026-09-12", VUMC, "insured", 10000,
                  [bline("Lab", 5000, "2026-09-12"), bline("Lab", 5000, "2026-09-13")], 10000, 0)
    e = make_eob("2026-09-12", VUMC, "C1", "paid", 5000, 0, 4000, 1000, [eline("LAB", 5000, 1000, "2026-09-12")])
    cases.append((b, e, False))
    out = []
    for bill, eob, not_yet in cases:
        r = eob_checks.run(bill, eob, not_yet=not_yet)
        for f in r["flags"]:
            out.extend(t for t in (f["text_en"], f["letter_en"]) if t)
    return out


def test_banned_words():
    texts = all_texts()
    assert len(texts) > 20, len(texts)
    for t in texts:
        low = t.lower()
        for w in BANNED:
            assert w not in low, (w, t)
        t.encode("ascii")
    src_path = _path or os.path.join(HERE, "..", "app", "eob_checks.py")
    with open(src_path, encoding="utf-8") as fh:
        src = fh.read().lower()
    src.encode("ascii")
    for w in BANNED:
        assert w not in src, w


if __name__ == "__main__":
    tests = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_") and callable(f)]
    for name, fn in tests:
        fn()
        print("ok", name)
    print("ALL PASS (%d tests)" % len(tests))
