"""Pure eligibility engine. Money is integer cents. No I/O except the loaders."""
import copy
import json
from datetime import date, timedelta

CONTRACT_VERSION = 1


def load_policy(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_fpl(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def fpl_cents(fpl, household_size):
    if isinstance(household_size, bool) or not isinstance(household_size, int):
        raise ValueError("household_size must be an integer")
    if not 1 <= household_size <= 12:
        raise ValueError("household_size must be 1-12")
    return fpl["base_cents"] + (household_size - 1) * fpl["per_extra_cents"]


def _fmt_dollars(cents):
    """Whole dollars -> '38,000'; otherwise '38,000.50'."""
    whole, rem = divmod(cents, 100)
    s = f"{whole:,}"
    return s if rem == 0 else f"{s}.{rem:02d}"


def _fmt_amount_due(cents):
    """Always two decimals: '4,812.40'."""
    whole, rem = divmod(cents, 100)
    return f"{whole:,}.{rem:02d}"


def _confirmed_fields(bill_fields):
    fields = bill_fields.get("fields", bill_fields)
    for name, f in fields.items():
        if not isinstance(f, dict) or f.get("confirmed") is not True:
            raise ValueError(f"bill field '{name}' is not confirmed")
    return fields


def _required(fields, name):
    f = fields.get(name)
    if f is None or f.get("value") is None:
        raise ValueError(f"bill field '{name}' is missing or has no value")
    return f["value"]


def _int_cents(value, name):
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{name} must be a non-negative integer (cents)")
    return value


def evaluate(bill_fields, answers, policy, fpl):
    fields = _confirmed_fields(bill_fields)
    statement_date = date.fromisoformat(_required(fields, "statement_date"))
    amount_due_cents = _int_cents(_required(fields, "amount_due_cents"), "amount_due_cents")

    size = answers.get("household_size")
    income_cents = _int_cents(answers.get("annual_income_cents"), "annual_income_cents")
    files_tax_return = answers.get("files_tax_return")
    if not isinstance(files_tax_return, bool):
        raise ValueError("files_tax_return must be true or false")

    fpl_c = fpl_cents(fpl, size)
    percent = (income_cents * 100) // fpl_c

    tier = None
    for t in policy["tiers"]:
        if t["max_percent"] is None or income_cents * 100 <= fpl_c * t["max_percent"]:
            tier = t
            break
    if tier is None:
        raise ValueError("policy has no matching tier")

    window = policy["application_window"]
    deadline_date = (statement_date + timedelta(days=window["days_from_statement"])).isoformat()

    documents = [
        {
            "id": d["id"],
            "label_en": d["label_en"],
            "required_if": d["required_if"],
            "citation": copy.deepcopy(d["citation"]),
        }
        for d in policy["documents"]
        if d["required_if"] == "always"
        or (d["required_if"] == "files_tax_return" and files_tax_return)
    ]

    return {
        "contract_version": CONTRACT_VERSION,
        "hospital_id": policy["hospital_id"],
        "fpl": {
            "year": fpl["year"],
            "household_size": size,
            "amount_cents": fpl_c,
            "citation": copy.deepcopy(fpl["citation"]),
        },
        "percent_of_fpl": percent,
        "tier": {
            "id": tier["id"],
            "label_en": tier["label_en"],
            "discount_percent": tier["discount_percent"],
            "eligible": tier["eligible"],
            "citation": copy.deepcopy(tier["citation"]),
        },
        "deadline": {
            "date": deadline_date,
            "text_en": window["text_template_en"].format(date=deadline_date),
            "citation": copy.deepcopy(window["citation"]),
        },
        "documents": documents,
        "contacts": copy.deepcopy(policy["contacts"]),
        "locked_numbers": [
            str(percent),
            str(size),
            _fmt_dollars(income_cents),
            _fmt_dollars(fpl_c),
            _fmt_amount_due(amount_due_cents),
            deadline_date,
            # Policy numbers the UI also shows (tier label, deadline text), so
            # generated text that repeats them is not flagged as unexpected.
            str(tier["discount_percent"]),
            str(window["days_from_statement"]),
        ],
    }
