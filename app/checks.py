"""Fixed-rule bill checks (Phase 2). Pure Python: no AI, no I/O, no app.main import.

run(bill) reads bill["fields"] and bill["lines"] (the BillIn shape) and returns
{"flags": [...], "total_to_ask_cents": int, "lines_checked": bool}.
Each flag: {id, text_en, letter_en, amount_cents|None, line_indexes, citation|None}.
Rules and strings: plan section D5 as amended by A3.
"""
import re

MEDICAID_CITATION = {
    "source": "42 CFR 438.106 (eCFR, current to 2026-10-15)",
    "url": "https://www.ecfr.gov/current/title-42/chapter-IV/subchapter-C/part-438/subpart-C/section-438.106",
}

MEDICAID_TEXT_EN = (
    "Did you have TennCare on the date of service? "
    "If this was a TennCare-covered service, a hospital that takes TennCare generally must accept "
    "what your TennCare health plan pays, plus any copay TennCare requires, as payment in full. "
    "Ask the hospital and your TennCare health plan why you were billed."
)
MEDICAID_LETTER_EN = (
    "My bill lists TennCare coverage. Please confirm whether this bill was "
    "submitted to my TennCare health plan, and whether this amount is a copay TennCare requires."
)


def _money(cents):
    """Cents -> '$1,385.00' (commas, 2 decimals; '-$5.00' for negatives)."""
    sign = "-" if cents < 0 else ""
    whole, rem = divmod(abs(cents), 100)
    return f"{sign}${whole:,}.{rem:02d}"


def _is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def _norm_desc(s):
    """Lowercase, punctuation removed, whitespace collapsed."""
    s = re.sub(r"[^\w\s]|_", "", str(s).lower())
    return " ".join(s.split())


def _flag(id_, text_en, letter_en, amount_cents=None, line_indexes=None, citation=None):
    return {
        "id": id_,
        "text_en": text_en,
        "letter_en": letter_en,
        "amount_cents": amount_cents,
        "line_indexes": list(line_indexes or []),
        "citation": citation,
    }


def _field(bill, name):
    f = (bill.get("fields") or {}).get(name)
    return f.get("value") if isinstance(f, dict) else None


def _duplicates(items):
    groups = {}
    for i, it in enumerate(items):
        amt = it.get("amount_cents")
        norm = _norm_desc(it.get("description") or "")
        if not _is_int(amt) or not norm:
            continue  # shortcut: rows with no readable amount or description are never grouped
        groups.setdefault((it.get("date"), norm, amt), []).append(i)
    flags = []
    for idxs in sorted(groups.values(), key=lambda g: g[0]):
        count = len(idxs)
        if count < 2:
            continue
        first = items[idxs[0]]
        desc = str(first.get("description")).strip()
        amt = first["amount_cents"]
        flags.append(_flag(
            "duplicate",
            f"This charge appears {count} times with the same description and amount: "
            f"{desc} ({_money(amt)} each). Ask whether it was billed more than once.",
            f'The charge "{desc}" ({_money(amt)}) appears {count} times. '
            f"Please confirm whether it was provided {count} times or billed more than once.",
            amt * (count - 1),
            idxs,
        ))
    return flags


def run(bill):
    fields_due = _field(bill, "amount_due_cents")
    due = fields_due if _is_int(fields_due) else None
    insurance = _field(bill, "insurance_status")
    lines = bill.get("lines")

    items = []
    total = None
    payments = None
    line_rules = False
    if isinstance(lines, dict):
        items = lines.get("items") or []
        t = lines.get("total_charges_cents")
        p = lines.get("payments_cents")
        total = t if _is_int(t) else None
        payments = p if _is_int(p) else None
        line_rules = lines.get("confirmed") is True and len(items) > 0

    flags = []
    if line_rules:
        flags.extend(_duplicates(items))

        amounts = [it.get("amount_cents") for it in items]
        if total is not None and all(_is_int(a) for a in amounts):
            s = sum(amounts)
            if s != total:
                flags.append(_flag(
                    "lines_sum",
                    f"The charges listed add up to {_money(s)}, but the total charges shown are {_money(total)}.",
                    f"The listed charges add up to {_money(s)}, but the total charges shown are "
                    f"{_money(total)}. Please explain the difference.",
                    total - s if total - s > 0 else None,
                ))

        if total is not None and payments is not None and due is not None:
            expected = total - payments
            if due != expected:
                sentence = (
                    f"Total charges {_money(total)} minus payments and adjustments {_money(payments)} "
                    f"is {_money(expected)}, but the amount due is {_money(due)}."
                )
                flags.append(_flag(
                    "due_mismatch",
                    sentence,
                    sentence + " Please explain the difference.",
                    due - expected if due - expected > 0 else None,
                ))

    # Insurance rules always run; insurance_unpaid needs payments the person confirmed (lines.confirmed), else it is quiet.
    payments_confirmed = isinstance(lines, dict) and lines.get("confirmed") is True
    if insurance == "insured" and payments_confirmed and payments == 0 and due is not None and due > 0:
        flags.append(_flag(
            "insurance_unpaid",
            "The bill lists insurance but shows no insurance payment. "
            "Ask whether the bill was sent to your insurer.",
            "My bill lists insurance but shows no insurance payment. Please confirm whether this "
            "bill was submitted to my insurer, and tell me the result.",
        ))
    if insurance == "medicaid" and due is not None and due > 0:
        flags.append(_flag(
            "medicaid", MEDICAID_TEXT_EN, MEDICAID_LETTER_EN,
            citation=dict(MEDICAID_CITATION),
        ))

    amount_sum = sum(f["amount_cents"] for f in flags if f["amount_cents"] is not None)
    total_to_ask = max(0, min(amount_sum, due) if due is not None else amount_sum)
    # "the math adds up" is only shown when the sum check really ran: a total and every amount were read (O2 #2)
    math_ran = line_rules and total is not None and all(_is_int(it.get("amount_cents")) for it in items)
    return {"flags": flags, "total_to_ask_cents": total_to_ask, "lines_checked": math_ran}
