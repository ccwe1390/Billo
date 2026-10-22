"""Plain-assert tests for app/checks.py. Run from repo root: py tests/test_checks.py"""
import copy
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))

from app import checks

SPIKE = os.path.join(HERE, "..", "spikes", "synthetic-bill")
with open(os.path.join(SPIKE, "lines_key.json"), encoding="utf-8") as fh:
    LINES_KEY = json.load(fh)
with open(os.path.join(SPIKE, "answer_key.json"), encoding="utf-8") as fh:
    ANSWER_KEY = json.load(fh)

MEDICAID_CITATION = {
    "source": "42 CFR 438.106 (eCFR, current to 2026-10-15)",
    "url": "https://www.ecfr.gov/current/title-42/chapter-IV/subchapter-C/part-438/subpart-C/section-438.106",
}
MEDICAID_TEXT = (
    "Did you have TennCare on the date of service? If this was a TennCare-covered service, a hospital "
    "that takes TennCare generally must accept what your TennCare health plan pays, plus any copay "
    "TennCare requires, as payment in full. Ask the hospital and your TennCare health plan why you "
    "were billed."
)
MEDICAID_LETTER = (
    "My bill lists TennCare coverage. Please confirm whether this bill was submitted "
    "to my TennCare health plan, and whether this amount is a copay TennCare requires."
)


def fld(v):
    return {"value": v, "confidence": 0.9, "confirmed": True}


def make(due, insurance=None, items=None, total=None, payments=None, confirmed=True, lines=True):
    b = {"fields": {"amount_due_cents": fld(due), "insurance_status": fld(insurance)}}
    if lines:
        b["lines"] = {"items": items or [], "total_charges_cents": total,
                      "payments_cents": payments, "confirmed": confirmed, "read": True}
    else:
        b["lines"] = None
    return b


def row(desc, amt, date=None, qty=1):
    return {"date": date, "description": desc, "quantity": qty, "amount_cents": amt}


def key_bill(n):
    """Bill dict for bill-n from lines_key.json + answer_key.json (6 fields)."""
    k = LINES_KEY["bill-%d" % n]
    a = ANSWER_KEY["bill-%d" % n]
    fields = {name: fld(a.get(name)) for name in (
        "hospital_name", "statement_date", "account_number", "amount_due_cents",
        "date_of_service", "insurance_status")}
    fields["amount_due_cents"] = fld(k["amount_due_cents"])
    return {"fields": fields, "lines": {
        "items": copy.deepcopy(k["items"]), "total_charges_cents": k["total_charges_cents"],
        "payments_cents": k["payments_cents"], "confirmed": True, "read": True}}


def ids(r):
    return [f["id"] for f in r["flags"]]


def test_bill_11_duplicate_ct():
    r = checks.run(key_bill(11))
    assert ids(r) == ["duplicate"], ids(r)
    f = r["flags"][0]
    assert f["amount_cents"] == 138500
    assert f["line_indexes"] == [1, 2]
    assert f["citation"] is None
    assert "CT scan, head, without contrast" in f["text_en"]
    assert r["total_to_ask_cents"] == 138500
    assert r["lines_checked"] is True
    # decoy pair must be in no flag
    descs = [d for fl in r["flags"] for d in [fl["text_en"]]]
    assert not any("IV fluids" in d for d in descs)
    assert 3 not in f["line_indexes"] and 4 not in f["line_indexes"]


def test_bill_12_due_mismatch():
    r = checks.run(key_bill(12))
    assert ids(r) == ["due_mismatch"], ids(r)
    f = r["flags"][0]
    assert f["amount_cents"] == 20000  # 185850 due - 165850 expected
    assert f["text_en"] == ("Total charges $1,858.50 minus payments and adjustments $200.00 "
                            "is $1,658.50, but the amount due is $1,858.50.")
    assert f["letter_en"] == f["text_en"] + " Please explain the difference."
    assert r["total_to_ask_cents"] == 20000


def test_bill_13_insurance_unpaid():
    r = checks.run(key_bill(13))
    assert ids(r) == ["insurance_unpaid"], ids(r)
    f = r["flags"][0]
    assert f["amount_cents"] is None and f["line_indexes"] == [] and f["citation"] is None
    assert f["text_en"] == ("The bill lists insurance but shows no insurance payment. "
                            "Ask whether the bill was sent to your insurer.")
    assert f["letter_en"] == ("My bill lists insurance but shows no insurance payment. Please confirm "
                              "whether this bill was submitted to my insurer, and tell me the result.")
    assert r["total_to_ask_cents"] == 0


def test_bill_14_medicaid():
    b = key_bill(14)
    assert b["fields"]["insurance_status"]["value"] == "medicaid"
    r = checks.run(b)
    assert ids(r) == ["medicaid"], ids(r)
    f = r["flags"][0]
    assert f["citation"] == MEDICAID_CITATION
    assert f["text_en"] == MEDICAID_TEXT
    assert f["letter_en"] == MEDICAID_LETTER
    assert f["amount_cents"] is None
    assert r["total_to_ask_cents"] == 0
    # explicit override as the plan states it
    b["fields"]["insurance_status"]["value"] = "medicaid"
    assert ids(checks.run(b)) == ["medicaid"]


def test_other_bills_quiet():
    # bills 11-14 only plant one error each; the bill-11 decoys must not add any
    for n in (12, 13, 14):
        assert len(checks.run(key_bill(n))["flags"]) == 1


def test_duplicate_decoys():
    # same description, different dates
    r = checks.run(make(20000, items=[row("Lab panel", 10000, "2026-10-01"),
                                      row("Lab panel", 10000, "2026-10-02")], total=20000, payments=0))
    assert r["flags"] == [] and r["lines_checked"] is True
    # same description, different amounts
    r = checks.run(make(20000, items=[row("Lab panel", 10000), row("Lab panel", 10001)],
                        total=20001, payments=1))
    assert r["flags"] == []
    # null date vs real date are different
    r = checks.run(make(20000, items=[row("Lab panel", 10000, None),
                                      row("Lab panel", 10000, "2026-10-01")], total=20000, payments=0))
    assert r["flags"] == []


def test_duplicate_normalization():
    r = checks.run(make(20000, items=[row("CT Scan,  Head.", 10000), row("ct scan head", 10000)],
                        total=20000, payments=0))
    assert ids(r) == ["duplicate"]
    assert r["flags"][0]["amount_cents"] == 10000
    # null dates equal each other; real equal dates also group
    r = checks.run(make(10000, items=[row("X-ray", 5000, "2026-10-01"), row("x-ray", 5000, "2026-10-01")],
                        total=10000, payments=0))
    assert ids(r) == ["duplicate"]


def test_three_identical_rows():
    r = checks.run(make(30000, items=[row("Saline", 10000)] * 3, total=30000, payments=0))
    assert ids(r) == ["duplicate"]
    f = r["flags"][0]
    assert f["amount_cents"] == 20000
    assert f["line_indexes"] == [0, 1, 2]
    assert f["text_en"] == ("This charge appears 3 times with the same description and amount: Saline "
                            "($100.00 each). Ask whether it was billed more than once.")
    assert f["letter_en"] == ('The charge "Saline" ($100.00) appears 3 times. Please confirm whether it '
                              "was provided 3 times or billed more than once.")


def test_two_duplicate_groups_in_line_order():
    items = [row("B", 100), row("A", 200), row("B", 100), row("A", 200)]
    r = checks.run(make(600, items=items, total=600, payments=0))
    assert ids(r) == ["duplicate", "duplicate"]
    assert r["flags"][0]["line_indexes"] == [0, 2]
    assert r["flags"][1]["line_indexes"] == [1, 3]
    assert r["total_to_ask_cents"] == 300


def test_lines_sum_positive_and_negative():
    items = [row("A", 10000), row("B", 5000)]
    r = checks.run(make(20000, items=items, total=20000, payments=0))
    assert ids(r) == ["lines_sum"]
    f = r["flags"][0]
    assert f["amount_cents"] == 5000
    assert f["text_en"] == "The charges listed add up to $150.00, but the total charges shown are $200.00."
    assert f["letter_en"] == ("The listed charges add up to $150.00, but the total charges shown are "
                              "$200.00. Please explain the difference.")
    # negative difference: still flagged, amount None
    r = checks.run(make(12000, items=items, total=12000, payments=0))
    assert ids(r) == ["lines_sum"]
    assert r["flags"][0]["amount_cents"] is None
    assert r["total_to_ask_cents"] == 0
    # an unread amount or unread total: no lines_sum
    r = checks.run(make(20000, items=[row("A", 10000), row("B", None)], total=20000, payments=0))
    assert "lines_sum" not in ids(r)
    r = checks.run(make(15000, items=items, total=None, payments=0))
    assert "lines_sum" not in ids(r)


def test_due_mismatch_negative_and_nulls():
    items = [row("A", 10000)]
    # amount due below expected: flagged, amount None
    r = checks.run(make(8000, items=items, total=10000, payments=0))
    assert ids(r) == ["due_mismatch"] and r["flags"][0]["amount_cents"] is None
    # payments unread: quiet
    r = checks.run(make(8000, items=items, total=10000, payments=None))
    assert r["flags"] == []
    # amount due equals expected: quiet
    r = checks.run(make(9000, items=items, total=10000, payments=1000))
    assert "due_mismatch" not in ids(r)


def test_insurance_unpaid_rules():
    items = [row("A", 10000)]
    r = checks.run(make(10000, "insured", items, total=10000, payments=0))
    assert ids(r) == ["insurance_unpaid"]
    # payments None: quiet
    r = checks.run(make(10000, "insured", items, total=10000, payments=None))
    assert r["flags"] == []
    # payments non-zero: quiet
    r = checks.run(make(9000, "insured", items, total=10000, payments=1000))
    assert r["flags"] == []
    # amount due 0: quiet
    r = checks.run(make(0, "insured", items, total=10000, payments=0))
    assert "insurance_unpaid" not in ids(r)
    # other statuses: quiet
    for st in ("self_pay", "unknown", None):
        assert checks.run(make(10000, st, items, total=10000, payments=0))["flags"] == []


def test_medicaid_amount_due_zero_quiet():
    assert checks.run(make(0, "medicaid", lines=False))["flags"] == []


def test_lines_not_confirmed():
    items = [row("Saline", 10000), row("Saline", 10000)]
    r = checks.run(make(20000, "self_pay", items, total=99999, payments=0, confirmed=False))
    assert r["flags"] == [] and r["lines_checked"] is False
    # confirmed but empty items: lines_checked False
    r = checks.run(make(20000, "self_pay", [], total=20000, payments=0))
    assert r["flags"] == [] and r["lines_checked"] is False


def test_lines_none_insurance_still_runs():
    r = checks.run(make(31000, "medicaid", lines=False))
    assert ids(r) == ["medicaid"] and r["lines_checked"] is False
    r = checks.run(make(31000, "self_pay", lines=False))
    assert r["flags"] == [] and r["lines_checked"] is False and r["total_to_ask_cents"] == 0
    # no "lines" key at all
    b = make(31000, "medicaid", lines=False)
    del b["lines"]
    assert ids(checks.run(b)) == ["medicaid"]


def test_min_cap():
    # duplicates 2 x 150.00 -> 15000 flagged; amount due only 5000
    items = [row("Saline", 15000), row("Saline", 15000)]
    r = checks.run(make(5000, items=items, total=30000, payments=25000))
    assert r["flags"][0]["amount_cents"] == 15000
    assert r["total_to_ask_cents"] == 5000
    # uncapped when the amounts are below amount due
    r = checks.run(make(30000, items=items, total=30000, payments=0))
    assert r["total_to_ask_cents"] == sum(f["amount_cents"] or 0 for f in r["flags"])
    assert r["total_to_ask_cents"] < 630000


def test_flag_order_and_shape():
    items = [row("A", 10000), row("A", 10000), row("B", 1000)]
    # sum 21000, total 25000 -> lines_sum 4000; due 24000 vs expected 25000-0 -> negative -> None
    r = checks.run(make(24000, "insured", items, total=25000, payments=0))
    assert ids(r) == ["duplicate", "lines_sum", "due_mismatch", "insurance_unpaid"], ids(r)
    for f in r["flags"]:
        assert set(f) == {"id", "text_en", "letter_en", "amount_cents", "line_indexes", "citation"}
    # medicaid last
    r = checks.run(make(24000, "medicaid", items, total=25000, payments=0))
    assert ids(r)[-1] == "medicaid"
    assert set(r) == {"flags", "total_to_ask_cents", "lines_checked"}


def test_money_format():
    assert checks._money(138500) == "$1,385.00"
    assert checks._money(5) == "$0.05"
    assert checks._money(100000000) == "$1,000,000.00"
    assert checks._money(-500) == "-$5.00"


def test_input_not_mutated():
    b = key_bill(11)
    before = copy.deepcopy(b)
    checks.run(b)
    assert b == before


def test_insurance_unpaid_needs_confirmed_payments():
    r = checks.run(make(50000, "insured", items=[row("Visit", 50000)], total=50000, payments=0, confirmed=False))
    assert "insurance_unpaid" not in ids(r), ids(r)   # payments not confirmed by the person: quiet
    r = checks.run(make(50000, "insured", items=[row("Visit", 50000)], total=50000, payments=0, confirmed=True))
    assert ids(r) == ["insurance_unpaid"], ids(r)


def test_lines_checked_only_when_the_sum_ran():
    r = checks.run(make(50000, items=[row("Visit", 50000)], total=None))
    assert r["flags"] == [] and r["lines_checked"] is False, r      # no total read: no "math adds up"
    r = checks.run(make(50000, items=[row("Visit", None)], total=50000))
    assert r["lines_checked"] is False, r
    r = checks.run(make(-500, items=[row("A", 100), row("A", 100)], total=200))
    assert r["total_to_ask_cents"] == 0, r                           # never negative


if __name__ == "__main__":
    tests = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_") and callable(f)]
    for name, fn in tests:
        fn()
        print("ok", name)
    print("ALL PASS (%d tests)" % len(tests))
