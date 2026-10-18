"""Bill-vs-EOB rules (Phase 3). Pure Python: no AI, no I/O, no app.main import.

run(bill, eob=None, not_yet=False, p2=None) compares a bill with the insurer's explanation of
benefits and merges the result with the Phase 2 (bill-only) checks. Money is integer cents.
Returns {"flags": [...], "total_to_ask_cents": int, "lines_checked": bool, "insurer_letter": dict|None}.
Phase 2 flags are copied with kind "bill"; insurance flags carry kind "insurance", citation None.
"""
import copy

from app import checks

_money = checks._money
_is_int = checks._is_int
_field = checks._field

TOLERANCE = 100  # cents: differences of $1.00 or less are rounding, not a flag
KNOWN_STATUSES = ("paid", "partially_paid", "denied", "pending")


def _ins(id_, text_en, letter_en, amount_cents=None, line_indexes=None):
    f = checks._flag(id_, text_en, letter_en, amount_cents, line_indexes, None)
    f["kind"] = "insurance"
    return f


def _s(v):
    """A field value as stripped text, or None when missing/blank."""
    if v is None:
        return None
    v = str(v).strip()
    return v or None


def _int_or_none(v):
    return v if _is_int(v) else None


def _status(eob):
    s = _s(_field(eob, "claim_status")) if eob is not None else None
    s = s.lower() if s else None
    return s if s in KNOWN_STATUSES else None


def _norm_name(s):
    s = "".join(c.lower() if c.isalnum() else " " for c in str(s))
    return " ".join(w for w in s.split() if w != "synthetic")


def _provider_mismatch(hospital, provider):
    if hospital is None or provider is None:
        return False
    a, b = _norm_name(hospital), _norm_name(provider)
    # shortcut: an insurer's abbreviation (e.g. "VANDERBILT UNIV MED CTR") reads as a different visit;
    # upgrade = a per-hospital alias list.
    return not (a == b or a.startswith(b + " ") or b.startswith(a + " "))


def _times(m):
    return "1 time" if m == 1 else "%d times" % m


def _line_groups(items, doc_dos, amount_key):
    """(date or the document's date of service, amount) -> [item indexes]. Lines with no amount are skipped."""
    groups = {}
    for i, it in enumerate(items):
        if not isinstance(it, dict):
            continue
        amt = it.get(amount_key)
        if not _is_int(amt):
            continue
        groups.setdefault((it.get("date") or doc_dos, amt), []).append(i)
    return groups


def _confirmed_items(doc):
    lines = doc.get("lines")
    if isinstance(lines, dict) and lines.get("confirmed") is True and lines.get("items"):
        return lines["items"]
    return None


def _line_flags(bill, eob, bill_dos, eob_dos):
    bill_items = _confirmed_items(bill)
    eob_items = _confirmed_items(eob)
    if bill_items is None or eob_items is None:
        return []
    bill_groups = _line_groups(bill_items, bill_dos, "amount_cents")
    eob_groups = _line_groups(eob_items, eob_dos, "amount_billed_cents")

    def desc(i):
        return str(bill_items[i].get("description")).strip()

    flags = []
    for (date, amt), idxs in bill_groups.items():
        n = len(idxs)
        m = len(eob_groups.get((date, amt), []))
        if n > m >= 1:
            d = date or "unknown"
            flags.append(_ins(
                "charged_more",
                f'"{desc(idxs[0])}" for {_money(amt)} on {d} is on this bill {n} times, '
                f"but your insurer's summary lists it {_times(m)}.",
                f'"{desc(idxs[0])}" for {_money(amt)} on {d} is listed {n} times on this bill, '
                f"but my insurer's explanation of benefits lists it {_times(m)}. "
                "Please remove the extra charge.",
                amt * (n - m),
                idxs,
            ))
    rows = sorted((i, key) for key, idxs in bill_groups.items() for i in idxs)
    for i, (date, amt) in rows:
        if (date, amt) not in eob_groups:
            d = date or "unknown"
            flags.append(_ins(
                "not_on_eob",
                f'"{desc(i)}" for {_money(amt)} on {d} is on this bill but not on your insurer\'s summary.',
                f'"{desc(i)}" for {_money(amt)} on {d} is on this bill but not on my insurer\'s '
                "explanation of benefits. Please explain this charge or remove it.",
                amt,
                [i],
            ))
    return flags


def _money_flags(bill, eob):
    lines = bill.get("lines") if isinstance(bill.get("lines"), dict) else {}
    bill_total = _int_or_none(lines.get("total_charges_cents"))
    payments = _int_or_none(lines.get("payments_cents"))
    due = _int_or_none(_field(bill, "amount_due_cents"))
    eob_billed = _int_or_none(_field(eob, "amount_billed_cents"))
    discount = _int_or_none(_field(eob, "plan_discount_cents"))
    plan_paid = _int_or_none(_field(eob, "plan_paid_cents"))
    owes = _int_or_none(_field(eob, "patient_owes_cents"))
    claim = _s(_field(eob, "claim_number"))

    flags = []
    if bill_total is not None and eob_billed is not None and abs(bill_total - eob_billed) > TOLERANCE:
        flags.append(_ins(
            "totals_mismatch",
            f"This bill's total charges are {_money(bill_total)}, but your insurer's summary shows "
            f"{_money(eob_billed)} billed for this visit.",
            f"This bill's total charges are {_money(bill_total)}, but my insurer's explanation of benefits "
            f"shows {_money(eob_billed)} billed for this visit. "
            "Please tell me which charges were sent to my insurance.",
        ))
    if payments is not None and plan_paid is not None:
        credit = plan_paid + (discount or 0)
        if abs(payments - credit) > TOLERANCE:
            flags.append(_ins(
                "credit_mismatch",
                f"Your insurer says it paid {_money(plan_paid)} and took off a plan discount of "
                f"{_money(discount or 0)} ({_money(credit)} in all), but this bill shows "
                f"{_money(payments)} in payments and adjustments.",
                f"My insurer says it paid {_money(plan_paid)} and applied a plan discount of "
                f"{_money(discount or 0)}, a total of {_money(credit)}, but this bill shows "
                f"{_money(payments)} in payments and adjustments. "
                "Please apply the full insurance payment and discount.",
            ))
    if due is not None and owes is not None and due > owes + TOLERANCE:
        claim_part = f" (claim {claim})" if claim else ""
        flags.append(_ins(
            "billed_more",
            f"Your insurer's summary says you owe {_money(owes)} for this visit, but this bill asks for "
            f"{_money(due)}. That is {_money(due - owes)} to ask the hospital about.",
            f"My insurer's explanation of benefits for this visit{claim_part} says I owe {_money(owes)}, "
            f"but this bill says {_money(due)}. Please correct the bill to match.",
            due - owes,
        ))
    return flags


def _denied(bill, eob):
    """Returns (flag, insurer_letter), or (None, None) when the bill asks for less than the denied amount."""
    due = _int_or_none(_field(bill, "amount_due_cents"))
    billed = _int_or_none(_field(eob, "amount_billed_cents"))
    if due is None or billed is None or not due >= billed - TOLERANCE:
        return None, None
    reason = _s(_field(eob, "denial_reason"))
    deadline = _s(_field(eob, "appeal_deadline"))
    phone = _s(_field(eob, "insurer_phone"))
    text = "Your insurer denied this claim."
    if reason:
        text += f' Reason printed on your summary: "{reason}".'
    if deadline:
        text += f" Appeal by {deadline}."
    if phone:
        text += f" Insurer phone: {phone}."
    flag = _ins(
        "denied", text,
        "My insurer denied this claim, and I am asking them to reconsider. "
        "Please hold this bill while that review is open.",
    )
    letter = {k: _field(eob, k) for k in (
        "insurer_name", "claim_number", "date_of_service", "provider_name",
        "denial_reason", "appeal_deadline", "insurer_phone")}
    return flag, letter


def run(bill, eob=None, not_yet=False, p2=None):
    if p2 is None:
        p2 = checks.run(bill)
    bill_flags = [dict(copy.deepcopy(f), kind="bill") for f in p2["flags"]]
    p2_total = p2["total_to_ask_cents"]
    lines_checked = p2["lines_checked"]

    def result(flags, total=p2_total, letter=None):
        return {"flags": bill_flags + flags, "total_to_ask_cents": total,
                "lines_checked": lines_checked, "insurer_letter": letter}

    # 1. nothing from the insurer and not waiting on it: Phase 2 as is.
    if eob is None and not not_yet:
        return result([])

    # 2. still processing: one flag, no other insurance rule.
    status = _status(eob)
    if not_yet or status == "pending":
        return result([_ins(
            "pending",
            "Your insurance is still processing this visit. Ask the hospital whether you can wait for your insurer's summary before paying.",
            "My insurance claim for this visit is still being processed. Please hold this bill until it "
            "is finished and send me a corrected bill.",
        )])

    # 3. a summary for another visit: only this flag.
    bill_dos = _s(_field(bill, "date_of_service"))
    eob_dos = _s(_field(eob, "date_of_service"))
    hospital = _s(_field(bill, "hospital_name"))
    provider = _s(_field(eob, "provider_name"))
    date_differs = bill_dos is not None and eob_dos is not None and bill_dos != eob_dos
    if date_differs or _provider_mismatch(hospital, provider):
        return result([_ins(
            "different_visit",
            f"This insurance summary is for a different visit (date of service {eob_dos or 'unknown'}, "
            f"{provider or 'unknown'}). Ask your insurer for the summary for {bill_dos or 'unknown'}.",
            None,
        )])

    # the insurer's summary answers the unpaid-insurance question once its status is known
    if status in ("paid", "partially_paid", "denied"):
        bill_flags = [f for f in bill_flags if f["id"] != "insurance_unpaid"]

    # 4. unknown status: no more insurance rules.
    if status is None:
        return result([])

    # 5. denied.
    if status == "denied":
        flag, letter = _denied(bill, eob)
        return result([flag] if flag else [], letter=letter)

    # 6. paid / partially_paid.
    flags = _line_flags(bill, eob, bill_dos, eob_dos) + _money_flags(bill, eob)

    # 7. merge with Phase 2.
    charged_idx = set()
    for f in flags:
        if f["id"] == "charged_more":
            charged_idx.update(f["line_indexes"])
    bill_flags = [f for f in bill_flags
                  if not (f["id"] == "duplicate" and set(f["line_indexes"]) & charged_idx)]
    due = _int_or_none(_field(bill, "amount_due_cents"))
    owes = _int_or_none(_field(eob, "patient_owes_cents"))
    total = p2_total
    if due is not None and owes is not None:
        total = due - owes if due > owes + TOLERANCE else 0
    return result(flags, total)
