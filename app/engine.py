"""Pure eligibility engine. Money is integer cents. No I/O except the loaders."""
import copy
import json
import re
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


def _name_core(s):
    """Lowercase, no parenthesized part, no 'hospital', letters and digits only."""
    s = re.sub(r"\(.*?\)", "", s.lower()).replace("hospital", "")
    return re.sub(r"[^a-z0-9]", "", s)


def _hospital_matches(bill_name, policy_name):
    core = _name_core(policy_name)
    return bool(core) and isinstance(bill_name, str) and core in _name_core(bill_name)


def _statement_date(value):
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise ValueError("statement_date must be YYYY-MM-DD")
    try:
        return date.fromisoformat(value)
    except ValueError:
        raise ValueError("statement_date must be YYYY-MM-DD")


def evaluate(bill_fields, answers, policy, fpl):
    fields = _confirmed_fields(bill_fields)
    statement_date = _statement_date(_required(fields, "statement_date"))
    amount_due_cents = _int_cents(_required(fields, "amount_due_cents"), "amount_due_cents")

    size = answers.get("household_size")
    income_cents = _int_cents(answers.get("annual_income_cents"), "annual_income_cents")
    files_tax_return = answers.get("files_tax_return")
    if not isinstance(files_tax_return, bool):
        raise ValueError("files_tax_return must be true or false")

    fpl_c = fpl_cents(fpl, size)
    percent = (income_cents * 100) // fpl_c

    tier = None
    tier_index = None
    for i, t in enumerate(policy["tiers"]):
        if t["max_percent"] is None or income_cents * 100 <= fpl_c * t["max_percent"]:
            tier = t
            tier_index = i
            break
    if tier is None:
        raise ValueError("policy has no matching tier")

    # Whole tier table for the Result screen; `current` is marked by position
    # because two tiers share the id "discount".
    tiers = [
        {
            "id": t["id"],
            "label_en": t["label_en"],
            "discount_percent": t["discount_percent"],
            "eligible": t["eligible"],
            "min_percent_exclusive": policy["tiers"][i - 1]["max_percent"] if i > 0 else None,
            "max_percent": t["max_percent"],
            "citation": copy.deepcopy(t["citation"]),
            "current": i == tier_index,
        }
        for i, t in enumerate(policy["tiers"])
    ]

    window = policy["application_window"]
    try:
        deadline_date = (statement_date + timedelta(days=window["days_from_statement"])).isoformat()
    except OverflowError:
        raise ValueError("statement_date is out of range")

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

    hospital_name = fields.get("hospital_name")
    hospital_name = hospital_name.get("value") if isinstance(hospital_name, dict) else None
    return {
        "contract_version": CONTRACT_VERSION,
        "hospital_id": policy["hospital_id"],
        "policy_hospital_name": policy["hospital_name"],
        "hospital_matches_policy": _hospital_matches(hospital_name, policy["hospital_name"]),
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
        "tiers": tiers,
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


def _field_value(fields, name):
    f = fields.get(name)
    return f.get("value") if isinstance(f, dict) else None


def evaluate_many(bills, answers, policy, fpl, as_of):
    """Several confirmed bills under one set of answers: the /household response
    (docs/contracts.md) without `contract_version`. `as_of` is a date, passed in."""
    if not bills:
        raise ValueError("no bills")
    coverage = policy["coverage_period"]
    cutoff = as_of - timedelta(days=coverage["days_before_application"])

    results = [evaluate({"fields": b["fields"]}, answers, policy, fpl) for b in bills]
    first = results[0]
    discount = first["tier"]["discount_percent"]

    rows = []
    covered = True
    for b, r in zip(bills, results):
        amount = _field_value(b["fields"], "amount_due_cents")
        service = _field_value(b["fields"], "date_of_service")
        rows.append({
            "id": b["id"],
            "label_en": b["label_en"],
            "source": b["source"],
            "hospital_name": _field_value(b["fields"], "hospital_name"),
            "statement_date": _field_value(b["fields"], "statement_date"),
            "date_of_service": service,
            "amount_due_cents": amount,
            "reduction_cents": amount * discount // 100,
            "deadline": r["deadline"],
        })
        if not isinstance(service, str) or date.fromisoformat(service) < cutoff:
            covered = False

    estimate_cents = sum(row["reduction_cents"] for row in rows)
    eligible = first["tier"]["eligible"]
    if eligible:
        estimate_text_en = "Up to $%s could be reduced if the hospital approves." % _fmt_amount_due(estimate_cents)
    else:
        estimate_text_en = "Not eligible under this policy."
    earliest = min((row["deadline"] for row in rows), key=lambda d: d["date"])

    locked = list(first["locked_numbers"])
    locked.append(_fmt_amount_due(estimate_cents))
    locked.extend(_fmt_amount_due(row["amount_due_cents"]) for row in rows)
    locked.extend(row["deadline"]["date"] for row in rows)
    locked.append(str(coverage["days_after_approval"]))
    locked = list(dict.fromkeys(locked))

    return {
        "as_of": as_of.isoformat(),
        "eligible": eligible,
        "tier": first["tier"],
        "percent_of_fpl": first["percent_of_fpl"],
        "bills": rows,
        "estimate_cents": estimate_cents,
        "estimate_text_en": estimate_text_en,
        "one_application_covers_all": covered,
        "coverage": {"text_en": coverage["text_en"], "citation": copy.deepcopy(coverage["citation"])},
        "earliest_deadline": earliest,
        "contacts": copy.deepcopy(policy["contacts"]),
        "locked_numbers": locked,
    }
