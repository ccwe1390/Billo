"""Pure eligibility engine. Money is integer cents. No I/O except the loaders."""
import copy
import json
import re
from datetime import date, timedelta

CONTRACT_VERSION = 1


def load_policy(path):
    with open(path, encoding="utf-8") as f:
        policy = json.load(f)
    if policy.get("coverage_period") is None and not (
            isinstance(policy.get("coverage_note_en"), str) and policy["coverage_note_en"].strip()):
        raise ValueError("policy %s has no coverage_period, so it needs coverage_note_en" % policy.get("hospital_id"))
    return policy


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


MAX_CENTS = 10**12


def _int_cents(value, name):
    if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= MAX_CENTS:
        raise ValueError(f"{name} must be a non-negative integer (cents) up to {MAX_CENTS}")
    return value


def _words(s):
    """Hospital name -> comparable words: lowercase, no apostrophes, no (parenthesized part), no leading 'the',
    'st' read as 'saint', punctuation as single spaces, the word 'hospital' dropped."""
    s = s.lower().replace("'", "").replace("\u2019", "")
    s = re.sub(r"\(.*?\)", "", s)
    s = re.sub(r"^\s*the\s+", "", s)
    s = re.sub(r"[^a-z0-9]+", " ", s)
    words = ["saint" if w == "st" else w for w in s.split()]
    return " ".join(w for w in words if w != "hospital")


def name_matches(bill_name, name):
    """True when the bill's name is `name` or starts with it (whole words). A match anchors at the start."""
    if not isinstance(bill_name, str) or not isinstance(name, str):
        return False
    w, m = _words(bill_name), _words(name)
    return m != "" and (w == m or w.startswith(m + " "))


def policy_matches(bill_name, policy):
    """True / False, or None when the bill names no hospital (unknown, not a mismatch).
    An exclude name wins over a match name."""
    if not isinstance(bill_name, str) or not bill_name.strip():
        return None
    if any(name_matches(bill_name, n) for n in policy.get("exclude_names") or []):
        return False
    names = policy.get("match_names") or [policy["hospital_name"]]
    return any(name_matches(bill_name, n) for n in names)


def _hospital_matches(bill_name, policy_name):
    """policy_matches for a single policy name."""
    return policy_matches(bill_name, {"hospital_name": policy_name})


def select_policy(hospital_name, policies, default_id):
    """(policy, matched): the first policy that names this hospital -> (it, True); no name on the bill ->
    (default, None); a name no policy matches -> (default, False)."""
    default = policies[default_id]
    if not isinstance(hospital_name, str) or not hospital_name.strip():
        return default, None
    for p in policies.values():
        if policy_matches(hospital_name, p) is True:
            return p, True
    return default, False


def _iso_date(value, name):
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise ValueError(f"{name} must be YYYY-MM-DD")
    try:
        return date.fromisoformat(value)
    except ValueError:
        raise ValueError(f"{name} must be YYYY-MM-DD")


def evaluate(bill_fields, answers, policy, fpl):
    fields = _confirmed_fields(bill_fields)
    statement_date = _iso_date(_required(fields, "statement_date"), "statement_date")
    amount_due_cents = _int_cents(_required(fields, "amount_due_cents"), "amount_due_cents")
    service = _field_value(fields, "date_of_service")
    if service is not None:
        _iso_date(service, "date_of_service")

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
    # The policies count from the FIRST bill after discharge, which is never before the date of service; this
    # statement may be a later one. Counting from the service date can only move "Apply by" earlier, never too late.
    from_service = service is not None and date.fromisoformat(service) < statement_date
    anchor = date.fromisoformat(service) if from_service else statement_date
    try:
        deadline_date = (anchor + timedelta(days=window["days_from_statement"])).isoformat()
    except OverflowError:
        raise ValueError("statement_date is out of range")

    documents = [
        {
            "id": d["id"],
            "label_en": d["label_en"],
            "required_if": d["required_if"],
            "citation": copy.deepcopy(d["citation"]),
            **({"url": d["url"]} if d.get("url") else {}),
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
        "hospital_matches_policy": policy_matches(hospital_name, policy),
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
            **({"other_route_en": tier["other_route_en"]} if tier.get("other_route_en") else {}),
        },
        "tiers": tiers,
        "deadline": {
            "date": deadline_date,
            "counted_from": "date_of_service" if from_service else "statement_date",
            "text_en": window["service_template_en" if from_service else "text_template_en"].format(date=deadline_date),
            "citation": copy.deepcopy(window["citation"]),
        },
        "documents": documents,
        "conditions": copy.deepcopy(policy.get("conditions") or []),
        "synthetic": bool(policy.get("synthetic")),
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


def coverage_of(policy):
    """{text_en, citation}: the policy's coverage rule, or - when the policy has none - its coverage_note_en
    with the application-window citation."""
    cov = policy["coverage_period"]
    if cov is None:
        return {"text_en": policy["coverage_note_en"], "citation": copy.deepcopy(policy["application_window"]["citation"])}
    return {"text_en": cov["text_en"], "citation": copy.deepcopy(cov["citation"])}


def evaluate_many(bills, answers, policy, fpl, as_of):
    """Several confirmed bills under one set of answers: the /household response
    (docs/contracts.md) without `contract_version`. `as_of` is a date, passed in."""
    if not bills:
        raise ValueError("no bills")
    coverage = policy["coverage_period"]  # None: the policy does not say (coverage_note_en is shown instead)
    days_before = coverage["days_before_application"] if coverage else None
    cutoff = as_of - timedelta(days=days_before) if days_before is not None else None  # None: no lower limit

    results = [evaluate({"fields": b["fields"]}, answers, policy, fpl) for b in bills]
    first = results[0]
    discount = first["tier"]["discount_percent"]

    rows = []
    covered = True
    estimate_cents = 0
    counted = 0
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
            "hospital_matches_policy": r["hospital_matches_policy"],
            "deadline": r["deadline"],
        })
        if r["hospital_matches_policy"] is not True:  # another hospital's bill, or no hospital name: listed, never counted
            continue
        counted += 1
        estimate_cents += rows[-1]["reduction_cents"]
        if cutoff is not None and (not isinstance(service, str) or date.fromisoformat(service) < cutoff):
            covered = False

    eligible = first["tier"]["eligible"]
    if eligible:
        estimate_text_en = "Up to $%s could be reduced if the hospital approves." % _fmt_amount_due(estimate_cents)
    else:
        if first["tier"].get("other_route_en"):
            estimate_text_en = "Not eligible for the income tiers. The hospital may still help another way; ask the hospital."
        else:
            estimate_text_en = "Not eligible under this policy."
    # another hospital's bill has no deadline under this policy: the earliest is taken over counted rows
    pool = [row for row in rows if row["hospital_matches_policy"] is True] or rows
    earliest = min((row["deadline"] for row in pool), key=lambda d: d["date"])

    locked = list(first["locked_numbers"])
    locked.append(_fmt_amount_due(estimate_cents))
    locked.extend(_fmt_amount_due(row["amount_due_cents"]) for row in rows)
    locked.extend(row["deadline"]["date"] for row in rows)
    if coverage and coverage.get("days_after_approval") is not None:
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
        "one_application_covers_all": bool(coverage) and covered and eligible and counted > 0,
        "coverage": coverage_of(policy),
        "conditions": copy.deepcopy(policy.get("conditions") or []),
        "synthetic": bool(policy.get("synthetic")),
        "earliest_deadline": earliest,
        "contacts": copy.deepcopy(policy["contacts"]),
        "locked_numbers": locked,
    }
