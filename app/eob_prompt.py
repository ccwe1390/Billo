"""The prompt that reads an insurer's explanation of benefits (EOB): Phase 3 insurance check."""

EOB_PROMPT = (
    "Read this explanation of benefits (EOB) from a health insurer. "
    "The patient's hospital bill is for a visit on {date_of_service}. "
    "Return only JSON with keys insurer_name, provider_name, date_of_service, claim_number, "
    "claim_status, amount_billed, plan_discount, plan_paid, patient_owes, denial_reason, "
    "appeal_deadline, insurer_phone, service_lines. "
    "If the EOB lists several claims, use only the one for that visit date. "
    "service_lines is a list with one object per printed service line, each with keys date, "
    "description, amount_billed, patient_owes. "
    "Copy every service line exactly as printed, in order. "
    "claim_status is one of paid, partially_paid, denied, pending. "
    "patient_owes is the total the patient may owe the provider for this claim. "
    "Give money as plain numbers. "
    "Do not return the member ID, group number, or anyone's name. "
    "Use null for anything you cannot read clearly. Do not guess. "
    'If this is not an explanation of benefits, return {"not_eob": true}.'
)


def build(date_of_service):
    # str.replace, not str.format: the prompt contains literal JSON braces
    date = date_of_service if isinstance(date_of_service, str) and date_of_service else "an unknown date"
    return EOB_PROMPT.replace("{date_of_service}", date)


if __name__ == "__main__":
    assert "a visit on 2026-09-12." in build("2026-09-12")
    assert "a visit on an unknown date." in build(None)
    assert '{"not_eob": true}' in build("2026-09-12") and "{date_of_service}" not in build(None)
    print("ok")
