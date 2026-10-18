"""Plain-assert tests. Run from repo root: py tests/test_engine.py"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))

from app import engine

DATA = os.path.join(HERE, "..", "app", "data")
FPL = engine.load_fpl(os.path.join(DATA, "fpl_2026.json"))
POLICY = engine.load_policy(os.path.join(DATA, "policy_cumberland_synthetic.json"))


def bill(statement="2026-10-01", amount=481240, confirmed=True):
    def f(v):
        return {"value": v, "confidence": 0.9, "confirmed": confirmed}
    return {"contract_version": 1, "fields": {
        "statement_date": f(statement),
        "amount_due_cents": f(amount),
    }}


def answers(income, size=4, tax=False):
    return {"contract_version": 1, "language": "en", "for_whom": "family",
            "household_size": size, "annual_income_cents": income,
            "files_tax_return": tax}


def run(income, size=4, tax=False, **kw):
    return engine.evaluate(bill(**kw), answers(income, size, tax), POLICY, FPL)


def test_fpl():
    assert engine.fpl_cents(FPL, 1) == 1_596_000
    assert engine.fpl_cents(FPL, 4) == 3_300_000
    assert engine.fpl_cents(FPL, 8) == 5_572_000
    for bad in (0, 13, -1):
        try:
            engine.fpl_cents(FPL, bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"size {bad} should raise")


def test_boundaries():
    cases = [
        (6_600_000, "free_care", "Free care (100% discount)"),
        (6_600_100, "discount", "75% discount"),
        (9_900_000, "discount", "75% discount"),
        (9_900_100, "discount", "50% discount"),
        (13_200_000, "discount", "50% discount"),
        (13_200_100, "not_eligible",
         "Not eligible under this policy - payment plan available"),
    ]
    for income, tid, label in cases:
        t = run(income)["tier"]
        assert t["id"] == tid and t["label_en"] == label, (income, t)
        assert t["eligible"] == (tid != "not_eligible")


def test_demo_case():
    r = run(3_800_000)
    assert r["percent_of_fpl"] == 115
    assert r["tier"]["id"] == "free_care"
    assert r["fpl"]["amount_cents"] == 3_300_000
    assert r["hospital_id"] == "cumberland_synthetic"
    assert r["contract_version"] == 1
    assert r["locked_numbers"] == [
        "115", "4", "38,000", "33,000", "4,812.40", "2027-05-29", "100", "240"]
    assert r["tier"]["discount_percent"] == 100


def test_tiers_table():
    r = run(3_800_000)
    tiers = r["tiers"]
    assert len(tiers) == 4
    current = [i for i, t in enumerate(tiers) if t["current"]]
    assert current == [0], current
    assert tiers[0]["label_en"] == r["tier"]["label_en"]
    got = [(t["min_percent_exclusive"], t["max_percent"]) for t in tiers]
    assert got == [(None, 200), (200, 300), (300, 400), (400, None)], got
    for income, idx in ((6_600_100, 1), (13_200_000, 2), (13_200_100, 3)):
        current = [i for i, t in enumerate(run(income)["tiers"]) if t["current"]]
        assert current == [idx], (income, current)


def test_deadline():
    r = run(3_800_000, statement="2026-10-01")
    assert r["deadline"]["date"] == "2027-05-29"
    assert "2027-05-29" in r["deadline"]["text_en"]
    assert r["deadline"]["citation"]["source"]


def test_documents():
    ids = [d["id"] for d in run(3_800_000, tax=False)["documents"]]
    assert ids == ["proof_income", "bill_copy"], ids
    ids = [d["id"] for d in run(3_800_000, tax=True)["documents"]]
    assert ids == ["proof_income", "tax_return", "bill_copy"], ids


def test_citations_and_contacts():
    r = run(3_800_000)
    assert r["fpl"]["citation"]["url"] == "https://aspe.hhs.gov/poverty-guidelines"
    assert r["tier"]["citation"]["effective_date"] == "2026-01-13"
    assert r["contacts"]["phone"] == "(615) 555-0100"
    assert r["contacts"]["email"] == "financial.assistance@example.org"
    assert r["contacts"]["citation"]["source"]
    for d in r["documents"]:
        assert d["citation"]["source"]


def test_unconfirmed_rejected():
    try:
        run(3_800_000, confirmed=False)
    except ValueError:
        return
    raise AssertionError("unconfirmed fields should raise ValueError")


def test_null_value_rejected():
    try:
        run(3_800_000, statement=None)
    except ValueError:
        return
    raise AssertionError("null required value should raise ValueError")


def test_hospital_match():
    def match(name):
        b = bill()
        if name is not None:
            b["fields"]["hospital_name"] = {"value": name, "confidence": 0.9, "confirmed": True}
        r = engine.evaluate(b, answers(3_800_000), POLICY, FPL)
        assert r["policy_hospital_name"] == "Cumberland General Hospital (SYNTHETIC)"
        return r["hospital_matches_policy"]
    assert match("Cumberland General Hospital (SYNTHETIC)") is True
    assert match("CUMBERLAND GENERAL HOSPITAL") is True
    assert match("Cumberland General") is True
    assert match("Vanderbilt University Medical Center") is False
    assert match(None) is None                       # no name on the bill: unknown, not a mismatch
    for blank in ("", "   "):
        assert match(blank) is None, blank
    assert match("NOT Cumberland General Hospital") is False     # anchored: the name must start with the policy name
    assert match("St Cumberland General") is False
    assert match("Cumberland General Hospital Nashville") is True
    assert match("The Cumberland General Hospital") is True       # a leading "The" (OCR, letterhead) still matches
    assert engine._hospital_matches(123, "Cumberland General Hospital") is None


def test_statement_date_strict():
    for bad in (20261001, "20261001", "2026-W40-4", "2026-02-30", "9999-12-31"):
        try:
            run(3_800_000, statement=bad)
        except ValueError:
            continue
        raise AssertionError("statement_date %r should raise ValueError" % (bad,))
    assert run(3_800_000, statement="2026-10-01")["deadline"]["date"] == "2027-05-29"


def test_amount_and_date_limits():
    assert run(3_800_000, amount=10**12)["locked_numbers"]
    for bad in (10**12 + 1, 10**30, -1, 1.5, True, "5"):
        try:
            run(3_800_000, amount=bad)
        except ValueError:
            continue
        raise AssertionError("amount %r should raise ValueError" % (bad,))
    try:
        run(10**12 + 1)
    except ValueError:
        pass
    else:
        raise AssertionError("income above the cap should raise ValueError")

    def with_service(v):
        b = bill()
        b["fields"]["date_of_service"] = {"value": v, "confidence": None, "confirmed": True}
        return engine.evaluate(b, answers(3_800_000), POLICY, FPL)
    with_service(None)
    with_service("2026-09-12")
    for bad in ("2026-13-01", "20260912", "2026-W37-6", "not a date", "", 20260912, True):
        try:
            with_service(bad)
        except ValueError as e:
            assert "date_of_service" in str(e), e
            continue
        raise AssertionError("date_of_service %r should raise ValueError" % (bad,))


def many_bills(service_override=None):
    rows = [
        ("b1", 481240, "2026-10-01", "2026-09-12"),
        ("b2", 185850, "2026-10-05", "2026-09-20"),
        ("b3", 64200, "2026-10-09", "2026-09-26"),
        ("b4", 31875, "2026-10-12", "2026-09-26"),
        ("b5", 120600, "2026-10-14", "2026-10-02"),
    ]
    out = []
    for i, (bid, amount, stmt, service) in enumerate(rows):
        if service_override and i == 2:
            service = service_override

        def f(v):
            return {"value": v, "confidence": None, "confirmed": True}
        out.append({"id": bid, "label_en": "Bill " + bid, "source": "demo", "fields": {
            "hospital_name": f("Cumberland General Hospital (SYNTHETIC)"),
            "statement_date": f(stmt),
            "date_of_service": f(service),
            "amount_due_cents": f(amount),
        }})
    return out


def test_evaluate_many():
    from datetime import date, timedelta
    as_of = date(2026, 10, 17)
    r = engine.evaluate_many(many_bills(), answers(3_800_000), POLICY, FPL, as_of)
    assert "contract_version" not in r
    assert r["as_of"] == "2026-10-17"
    assert r["eligible"] is True and r["tier"]["id"] == "free_care"
    assert r["percent_of_fpl"] == 115
    assert r["estimate_cents"] == 883765, r["estimate_cents"]
    assert r["estimate_text_en"] == "Up to $8,837.65 could be reduced if the hospital approves."
    assert r["one_application_covers_all"] is True
    assert r["earliest_deadline"]["date"] == "2027-05-29"
    assert [b["reduction_cents"] for b in r["bills"]] == [481240, 185850, 64200, 31875, 120600]
    assert r["bills"][0]["deadline"]["date"] == "2027-05-29"
    assert r["bills"][0]["date_of_service"] == "2026-09-12"
    assert r["coverage"]["text_en"] == POLICY["coverage_period"]["text_en"]
    assert r["contacts"]["phone"] == "(615) 555-0100"
    ln = r["locked_numbers"]
    assert len(ln) == len(set(ln)), ln
    for want in ("115", "8,837.65", "4,812.40", "1,858.50", "642.00", "318.75", "1,206.00",
                 "2027-05-29", "2027-06-02", "2027-06-06", "2027-06-09", "2027-06-11", "180"):
        assert want in ln, (want, ln)

    r = engine.evaluate_many(many_bills(), answers(20_000_000), POLICY, FPL, as_of)
    assert r["eligible"] is False and r["estimate_cents"] == 0
    assert r["estimate_text_en"] == "Not eligible under this policy."

    # exactly 240 days before as_of is covered, 241 is not
    assert date(2026, 2, 18) == as_of - timedelta(days=241)
    r = engine.evaluate_many(many_bills("2026-02-18"), answers(3_800_000), POLICY, FPL, as_of)
    assert r["one_application_covers_all"] is False
    r = engine.evaluate_many(many_bills("2026-02-19"), answers(3_800_000), POLICY, FPL, as_of)
    assert r["one_application_covers_all"] is True

    # one_application_covers_all needs an eligible family: a covered, not-eligible household gets False
    r = engine.evaluate_many(many_bills(), answers(20_000_000), POLICY, FPL, as_of)
    assert r["one_application_covers_all"] is False and r["eligible"] is False

    # another hospital's bill is listed but not counted in the estimate or in "one application covers all"
    other = many_bills()
    other[1]["fields"]["hospital_name"]["value"] = "Vanderbilt University Medical Center"
    other[1]["fields"]["date_of_service"]["value"] = "2025-01-01"           # would break coverage if it counted
    r = engine.evaluate_many(other, answers(3_800_000), POLICY, FPL, as_of)
    assert [b["hospital_matches_policy"] for b in r["bills"]] == [True, False, True, True, True]
    assert len(r["bills"]) == 5 and r["bills"][1]["reduction_cents"] == 185850
    assert r["estimate_cents"] == 883765 - 185850, r["estimate_cents"]
    assert r["one_application_covers_all"] is True
    assert r["estimate_text_en"] == "Up to $6,979.15 could be reduced if the hospital approves."

    # a bill with no hospital name is unknown (None), still counted
    blank = many_bills()
    blank[0]["fields"]["hospital_name"]["value"] = None
    r = engine.evaluate_many(blank, answers(3_800_000), POLICY, FPL, as_of)
    assert r["bills"][0]["hospital_matches_policy"] is None and r["estimate_cents"] == 883765

    # only other-hospital bills: nothing counted, so no "one application covers all"
    for b in other:
        b["fields"]["hospital_name"]["value"] = "Vanderbilt University Medical Center"
    r = engine.evaluate_many(other, answers(3_800_000), POLICY, FPL, as_of)
    assert r["estimate_cents"] == 0 and r["one_application_covers_all"] is False

    try:
        engine.evaluate_many([], answers(3_800_000), POLICY, FPL, as_of)
    except ValueError:
        pass
    else:
        raise AssertionError("empty bills should raise ValueError")


# ---------------------------------------------------------------- real policies (plan v2 S1)
VUMC = engine.load_policy(os.path.join(DATA, "policy_vumc.json"))
AST = engine.load_policy(os.path.join(DATA, "policy_ascension_saint_thomas.json"))
POLICIES = {p["hospital_id"]: p for p in (VUMC, AST, POLICY)}
FPL1 = engine.fpl_cents(FPL, 1)


def pct(n):
    """Exactly n% of the household-of-1 poverty guideline, in cents."""
    assert FPL1 * n % 100 == 0
    return FPL1 * n // 100


def run_p(policy, income, name=None, size=1, tax=False):
    b = bill()
    if name is not None:
        b["fields"]["hospital_name"] = {"value": name, "confidence": 0.9, "confirmed": True}
    return engine.evaluate(b, answers(income, size, tax), policy, FPL)


def test_words():
    w = engine._words
    assert w("St. Thomas Midtown") == "saint thomas midtown"
    assert w("St Thomas") == w("Saint Thomas") == "saint thomas"
    assert w("Stones River Hospital") == "stones river"                       # only the whole word "st" becomes "saint"
    assert w("Monroe Carell Jr. Children's Hospital at Vanderbilt") == "monroe carell jr childrens at vanderbilt"
    assert w("Monroe Carell Jr. Children’s Hospital at Vanderbilt") == w("Monroe Carell Jr Childrens Hospital at Vanderbilt")
    assert w("The Cumberland General Hospital (SYNTHETIC)") == "cumberland general"
    assert w("Vanderbilt   University,  Medical-Center") == "vanderbilt university medical center"
    assert w("  HOSPITAL ") == "" and w("") == "" and w("(SYNTHETIC)") == ""
    assert w("Hospital for Specialty Surgery") == "for specialty surgery"      # only the word "hospital" is dropped


def test_name_matches():
    m = engine.name_matches
    assert m("Vanderbilt University Medical Center", "Vanderbilt University Medical Center")
    assert m("Vanderbilt University Medical Center (SYNTHETIC)", "Vanderbilt University Medical Center")
    assert m("Vanderbilt University Medical Center Nashville", "Vanderbilt University Medical Center")
    assert not m("Vanderbilt University Medical Centers", "Vanderbilt University Medical Center")   # whole words
    assert not m("Vanderbilt University", "Vanderbilt University Medical Center")                   # shorter than the name
    assert not m("NOT Vanderbilt University Medical Center", "Vanderbilt University Medical Center")  # anchored at the start
    assert m("Children's Hospital at Vanderbilt", "Childrens Hospital at Vanderbilt")
    assert m("Childrens Hospital at Vanderbilt", "Children's Hospital at Vanderbilt")
    assert m("St. Thomas Midtown", "Saint Thomas Midtown Hospital")
    assert not m("Anything", "") and not m("Anything", "(SYNTHETIC)") and not m("", "Anything")
    assert not m(None, "x") and not m(123, "x") and not m("x", None)


def test_policy_selection_by_bill_name():
    cases = [
        ("Vanderbilt University Medical Center (SYNTHETIC)", "vumc"),                      # bill-01, -02, -03, -05
        ("Vanderbilt Wilson County Hospital (SYNTHETIC)", "vumc"),                         # bill-04
        ("Monroe Carell Jr. Children's Hospital at Vanderbilt", "vumc"),
        ("Vanderbilt University Hospital", "vumc"),
        ("Ascension Saint Thomas Midtown (SYNTHETIC)", "ascension_saint_thomas"),          # bill-06
        ("Ascension Saint Thomas West (SYNTHETIC)", "ascension_saint_thomas"),             # bill-07, -09
        ("Ascension Saint Thomas Rutherford (SYNTHETIC)", "ascension_saint_thomas"),       # bill-08
        ("Saint Thomas Midtown Hospital", "ascension_saint_thomas"),
        ("St. Thomas West", "ascension_saint_thomas"),
        ("Cumberland General Hospital (SYNTHETIC)", "cumberland_synthetic"),               # bill-10
    ]
    for name, want in cases:
        policy, matched = engine.select_policy(name, POLICIES, "vumc")
        assert policy["hospital_id"] == want and matched is True, (name, policy["hospital_id"], matched)
    for p in (VUMC, AST):                                   # every name a policy lists selects that policy
        for name in p["match_names"]:
            policy, matched = engine.select_policy(name, POLICIES, "vumc")
            assert policy is p and matched is True, name
    # excluded and unknown hospitals: no policy matches -> the default policy, matched False
    for name in ("Vanderbilt Clarksville Hospital (SYNTHETIC)", "Vanderbilt Stallworth Rehabilitation Hospital",
                 "Ascension Saint Thomas Behavioral Health Hospital", "Ascension Saint Thomas Rehabilitation Hospital",
                 "TriStar Centennial Medical Center", "St Cumberland General"):
        policy, matched = engine.select_policy(name, POLICIES, "vumc")
        assert policy["hospital_id"] == "vumc" and matched is False, (name, policy["hospital_id"], matched)
    assert engine.policy_matches("Ascension Saint Thomas Behavioral Health Hospital", AST) is False   # exclude wins
    assert engine.policy_matches("Vanderbilt Clarksville Hospital", VUMC) is False
    # no name on the bill: unknown, default policy
    for blank in (None, "", "   ", 123):
        policy, matched = engine.select_policy(blank, POLICIES, "vumc")
        assert policy is VUMC and matched is None, blank
    assert engine.policy_matches(None, VUMC) is None and engine.policy_matches("  ", AST) is None
    # the default is whichever id the caller names
    policy, matched = engine.select_policy("TriStar Centennial Medical Center", POLICIES, "ascension_saint_thomas")
    assert policy is AST and matched is False
    # evaluate() reports the same answer
    assert run_p(VUMC, pct(100), "Vanderbilt University Medical Center (SYNTHETIC)")["hospital_matches_policy"] is True
    assert run_p(VUMC, pct(100), "Ascension Saint Thomas West (SYNTHETIC)")["hospital_matches_policy"] is False
    assert run_p(VUMC, pct(100), "Vanderbilt Clarksville Hospital")["hospital_matches_policy"] is False
    assert run_p(AST, pct(100), "Ascension Saint Thomas Rehabilitation Hospital")["hospital_matches_policy"] is False
    assert run_p(VUMC, pct(100))["hospital_matches_policy"] is None


def test_vumc_boundaries():
    rows = [
        (pct(300), "free_care", 100, True), (pct(300) + 1, "discount", 85, True),
        (pct(350), "discount", 85, True), (pct(350) + 1, "not_eligible", 0, False),
        (0, "free_care", 100, True),
    ]
    for income, tid, disc, eligible in rows:
        r = run_p(VUMC, income)
        t = r["tier"]
        assert (t["id"], t["discount_percent"], t["eligible"]) == (tid, disc, eligible), (income, t)
        current = [i for i, x in enumerate(r["tiers"]) if x["current"]]
        assert len(current) == 1, (income, current)
    assert run_p(VUMC, pct(300) + 1)["percent_of_fpl"] == 300 and run_p(VUMC, pct(350) + 1)["percent_of_fpl"] == 350
    r = run_p(VUMC, pct(350) + 1)
    assert "Catastrophic" in r["tier"]["other_route_en"] and r["tier"]["other_route_en"] == VUMC["tiers"][2]["other_route_en"]
    assert "other_route_en" not in run_p(VUMC, pct(350))["tier"]                  # only the not-eligible tier carries it
    assert "other_route_en" not in run_p(POLICY, 13_200_100)["tier"]              # Cumberland has none


def test_ascension_boundaries():
    rows = [
        (pct(250), "free_care", 100, True), (pct(250) + 1, "discount", 86, True),
        (pct(300), "discount", 86, True), (pct(300) + 1, "discount", 81, True),
        (pct(350), "discount", 81, True), (pct(350) + 1, "discount", 79, True),
        (pct(400), "discount", 79, True), (pct(400) + 1, "not_eligible", 0, False),
    ]
    for income, tid, disc, eligible in rows:
        r = run_p(AST, income)
        t = r["tier"]
        assert (t["id"], t["discount_percent"], t["eligible"]) == (tid, disc, eligible), (income, t)
        current = [i for i, x in enumerate(r["tiers"]) if x["current"]]
        assert len(current) == 1 and r["tiers"][current[0]]["discount_percent"] == disc, (income, current)
    assert len(run_p(AST, 0)["tiers"]) == 5
    r = run_p(AST, pct(400) + 1)
    assert "Means Test" in r["tier"]["other_route_en"] and r["tier"]["other_route_en"] == AST["tiers"][4]["other_route_en"]
    assert "other_route_en" not in run_p(AST, pct(400))["tier"]


def test_conditions_synthetic_and_documents():
    for policy, name in ((VUMC, "vumc"), (AST, "ascension_saint_thomas")):
        r = run_p(policy, pct(100))
        assert r["hospital_id"] == name and r["synthetic"] is False
        assert r["conditions"] == policy["conditions"] and len(r["conditions"]) >= 7
        assert r["conditions"] is not policy["conditions"] and r["conditions"][0] is not policy["conditions"][0]
        original = policy["conditions"][0]["text_en"]
        r["conditions"][0]["text_en"] = "changed"
        assert policy["conditions"][0]["text_en"] == original                   # a copy: the policy is never mutated
        for c in policy["conditions"]:
            assert c["text_en"] and c["citation"]["page"]
    r = run_p(POLICY, pct(100))
    assert r["synthetic"] is True and r["conditions"] == []
    # documents: the hospital's own form carries a url; the others do not
    def want(policy, tax):
        return [d["id"] for d in policy["documents"] if d["required_if"] == "always" or (tax and d["required_if"] == "files_tax_return")]
    ids = [d["id"] for d in run_p(VUMC, pct(100))["documents"]]
    assert ids == want(VUMC, False) and ids[0] == "hospital_form" and "tax_return" not in ids, ids
    ids = [d["id"] for d in run_p(VUMC, pct(100), tax=True)["documents"]]
    assert ids == want(VUMC, True) and "tax_return" in ids, ids
    docs = {d["id"]: d for d in run_p(VUMC, pct(100), tax=True)["documents"]}
    assert docs["hospital_form"]["url"] == VUMC["documents"][0]["url"] and docs["hospital_form"]["url"].startswith("https://")
    assert "url" not in docs["proof_income"] and "url" not in docs["tax_return"]
    ids = [d["id"] for d in run_p(AST, pct(100))["documents"]]
    assert ids == want(AST, False) and ids[0] == "hospital_form" and "tax_return" not in ids, ids
    assert [d["id"] for d in run_p(AST, pct(100), tax=True)["documents"]] == want(AST, True)
    assert run_p(AST, pct(100))["documents"][0]["url"].startswith("https://")
    assert all("url" not in d for d in run_p(POLICY, pct(100))["documents"])


def named_bills(name, service_override=None):
    rows = many_bills(service_override)
    for r in rows:
        r["fields"]["hospital_name"]["value"] = name
    return rows


def test_evaluate_many_real_policies():
    from datetime import date
    as_of = date(2026, 10, 17)
    ineligible_text = "Not eligible for the income tiers. The hospital may still help another way; ask the hospital."
    # VUMC: days_before_application and days_after_approval are null
    vname = "Vanderbilt University Medical Center (SYNTHETIC)"
    r = engine.evaluate_many(named_bills(vname), answers(3_800_000), VUMC, FPL, as_of)
    assert r["estimate_cents"] == 883765 and r["eligible"] is True and r["one_application_covers_all"] is True
    assert r["synthetic"] is False and r["conditions"] == VUMC["conditions"]
    assert r["coverage"] == {"text_en": VUMC["coverage_period"]["text_en"],
                             "citation": VUMC["coverage_period"]["citation"]}
    assert "None" not in r["locked_numbers"] and all(isinstance(x, str) for x in r["locked_numbers"])
    assert len(r["locked_numbers"]) == len(set(r["locked_numbers"]))
    for want in ("115", "8,837.65", "4,812.40", "2027-05-29", "100", "240"):
        assert want in r["locked_numbers"], want
    assert "182" not in r["locked_numbers"]                                  # null days_after_approval is not locked
    # no lower limit: a very old service date is still covered
    r = engine.evaluate_many(named_bills(vname, "2019-01-01"), answers(3_800_000), VUMC, FPL, as_of)
    assert r["one_application_covers_all"] is True
    # a bill with no service date is covered too when there is no lower limit
    nodate = named_bills(vname)
    nodate[0]["fields"]["date_of_service"]["value"] = None
    assert engine.evaluate_many(nodate, answers(3_800_000), VUMC, FPL, as_of)["one_application_covers_all"] is True
    # other-route text, VUMC and Ascension; Cumberland keeps the old text
    r = engine.evaluate_many(named_bills(vname), answers(20_000_000), VUMC, FPL, as_of)
    assert r["eligible"] is False and r["estimate_cents"] == 0 and r["estimate_text_en"] == ineligible_text
    assert r["one_application_covers_all"] is False and r["tier"]["other_route_en"]
    # Ascension: coverage_period is null -> the note, never "covers all"
    aname = "Ascension Saint Thomas West (SYNTHETIC)"
    r = engine.evaluate_many(named_bills(aname), answers(3_800_000), AST, FPL, as_of)
    assert AST["coverage_period"] is None
    assert r["eligible"] is True and r["estimate_cents"] == 883765 and r["one_application_covers_all"] is False
    assert r["coverage"] == {"text_en": AST["coverage_note_en"], "citation": AST["application_window"]["citation"]}
    assert r["coverage"]["citation"] is not AST["application_window"]["citation"]
    assert "None" not in r["locked_numbers"] and "180" not in r["locked_numbers"]
    r = engine.evaluate_many(named_bills(aname), answers(20_000_000), AST, FPL, as_of)
    assert r["eligible"] is False and r["estimate_text_en"] == ineligible_text
    assert engine.evaluate_many(named_bills("Cumberland General Hospital (SYNTHETIC)"), answers(20_000_000), POLICY, FPL,
                                as_of)["estimate_text_en"] == "Not eligible under this policy."
    # Cumberland keeps its fields
    r = engine.evaluate_many(many_bills(), answers(3_800_000), POLICY, FPL, as_of)
    assert r["synthetic"] is True and r["conditions"] == []


def test_load_policy_needs_coverage_note():
    import json
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "p.json")
        bad = dict(AST)
        del bad["coverage_note_en"]
        with open(p, "w", encoding="utf-8") as f:
            json.dump(bad, f)
        try:
            engine.load_policy(p)
        except ValueError as e:
            assert "coverage_note_en" in str(e)
        else:
            raise AssertionError("a policy with null coverage_period and no note should raise ValueError")
        with open(p, "w", encoding="utf-8") as f:
            json.dump(AST, f)
        assert engine.load_policy(p)["coverage_period"] is None
    assert engine.coverage_of(VUMC)["text_en"] == VUMC["coverage_period"]["text_en"]


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
    print("ALL PASS")
