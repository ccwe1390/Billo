"""Answer key for the engine, computed by hand from the Federal Register table (not from the engine).
Run from repo root: FAKE_AI=1 py tests/test_answer_key.py"""
import os
import sys

os.environ["FAKE_AI"] = "1"
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))

from app import engine

DATA = os.path.join(HERE, "..", "app", "data")
FPL = engine.load_fpl(os.path.join(DATA, "fpl_2026.json"))
POLICY = engine.load_policy(os.path.join(DATA, "policy_cumberland_synthetic.json"))

# (household_size, annual_income_cents, tier id, discount_percent, percent_of_fpl)
ROWS = [
    (1, 0, "free_care", 100, 0),
    (1, 3192000, "free_care", 100, 200),
    (1, 3192001, "discount", 75, 200),
    (1, 4788000, "discount", 75, 300),
    (1, 4788001, "discount", 50, 300),
    (1, 6384000, "discount", 50, 400),
    (1, 6384001, "not_eligible", 0, 400),
    (2, 4328000, "free_care", 100, 200),
    (2, 6500000, "discount", 50, 300),
    (3, 2732000, "free_care", 100, 100),
    (3, 8196001, "discount", 50, 300),
    (4, 3800000, "free_care", 100, 115),
    (4, 6600000, "free_care", 100, 200),
    (4, 9900000, "discount", 75, 300),
    (4, 13200001, "not_eligible", 0, 400),
    (5, 7736000, "free_care", 100, 200),
    (6, 13308000, "discount", 75, 300),
    (8, 11144000, "free_care", 100, 200),
    (10, 20176000, "discount", 50, 300),
    (12, 30000000, "discount", 50, 382),
]


def confirmed(value):
    return {"value": value, "confidence": 0.9, "confirmed": True}


def evaluate(size, income):
    bill = {"contract_version": 1, "fields": {
        "statement_date": confirmed("2026-10-01"),
        "amount_due_cents": confirmed(481240),
    }}
    answers = {"contract_version": 1, "language": "en", "for_whom": "family",
               "household_size": size, "annual_income_cents": income,
               "files_tax_return": True}
    return engine.evaluate(bill, answers, POLICY, FPL)


for size, income, tier_id, discount, pct in ROWS:
    r = evaluate(size, income)
    got = (r["tier"]["id"], r["tier"]["discount_percent"], r["percent_of_fpl"])
    assert got == (tier_id, discount, pct), ((size, income), got, (tier_id, discount, pct))

print("ALL PASS")
