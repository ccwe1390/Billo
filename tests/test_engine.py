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


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
    print("ALL PASS")
