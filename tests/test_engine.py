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


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
    print("ALL PASS")
