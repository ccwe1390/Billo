# JSON contracts - in production since 14:53 CDT (drafted for the PRD fork F6 gate ~1:45 PM)

Drafted 2026-10-17 ~13:20 CDT by Claude. Each shape changes only by team
agreement; when one changes, bump `contract_version`.

Rules that apply to all four:
- **Money:** integer cents (`4812.40` -> `481240`), never floats.
- **Dates:** `YYYY-MM-DD`.
- **Languages:** ~~`"en" | "es" | "ar" | "zh-CN" | "zh-TW" | "vi" | "fr" | "ko" | "ru" | "de" | "hi"`~~
  2026-10-17 20:13 CDT (record AI): any `code` in `app/data/languages.json` (32 codes: the 31
  Oracle Translate codes + `hi`); any other value -> 422. Earlier note kept below:
  (tier 1 en/es/ar/zh-CN/zh-TW has a translated interface; corrected 2026-10-17
  from `"en" | "es" | "ar"`, which the code stopped matching at c5f04a9).
- **Eligibility math compares cents, not rounded percents:**
  `income_cents * 100 <= fpl_cents * limit_percent`.
  `percent_of_fpl` is for display only (rounded down to a whole number), so a
  household exactly at a boundary can never flip tiers because of rounding.

## 1. BillFields - output of `POST /extract` (image in)

```json
{
  "contract_version": 1,
  "fields": {
    "hospital_name":    {"value": "Cumberland General Hospital (SYNTHETIC)", "confidence": 0.95, "confirmed": false},
    "statement_date":   {"value": "2026-10-01", "confidence": 0.9, "confirmed": false},
    "account_number":   {"value": "CGH-00482913", "confidence": 0.9, "confirmed": false},
    "amount_due_cents": {"value": 481240, "confidence": 0.95, "confirmed": false},
    "date_of_service":  {"value": null, "confidence": 0.0, "confirmed": false},
    "insurance_status": {"value": "self_pay", "confidence": 0.8, "confirmed": false}
  }
}
```
- `value: null` means unreadable. The UI must ask for it; the model is never
  allowed to guess.
- `insurance_status` is one of `"self_pay" | "insured" | "unknown"`. The
  server maps the model's free text (e.g. "None on file (self-pay)") onto it.
- The server normalizes the model's `MM/DD/YYYY` dates and float amounts into
  this shape.
- `/evaluate` refuses any field with `confirmed: false`.

## 2. HouseholdAnswers - from screen 3

```json
{
  "contract_version": 1,
  "language": "ar",
  "for_whom": "family",
  "household_size": 4,
  "annual_income_cents": 3800000,
  "files_tax_return": false
}
```
- `household_size` is 1-12 and `for_whom` is `"self" | "family"`.
- There are no fields for immigration status, SSN, ID, or name.

## 3. EngineResult - output of `POST /evaluate` (BillFields + HouseholdAnswers in)

```json
{
  "contract_version": 1,
  "hospital_id": "cumberland_synthetic",
  "fpl": {"year": 2026, "household_size": 4, "amount_cents": 3300000,
          "citation": {"source": "HHS 2026 Poverty Guidelines", "url": "", "page": null, "effective_date": "2026-01-13"}},
  "percent_of_fpl": 115,
  "tier": {"id": "free_care", "label_en": "Free care (100% discount)", "discount_percent": 100, "eligible": true,
           "citation": {"source": "", "url": "", "page": 0, "effective_date": ""}},
  "deadline": {"date": "2027-05-29", "text_en": "", "citation": {}},
  "documents": [{"id": "proof_income", "label_en": "", "required_if": "always", "citation": {}}],
  "contacts": {"phone": "", "email": "", "payment_plan_phone": "", "citation": {}},
  "locked_numbers": ["115", "4", "38,000", "33,000", "4,812.40", "2027-05-29", "100", "240"]
}
```
- 2026-10-17 13:36 CDT, still draft so no version bump: added
  `tier.discount_percent`, `deadline.date`, `contacts.payment_plan_phone`, and
  the deadline, discount percent and window days to `locked_numbers` (review of
  the first engine build).
- `tier.id` is one of `"free_care" | "discount" | "not_eligible"`.
  `not_eligible` carries the payment-plan contact in `contacts`.
- Every rule-derived item carries a `citation` with source, url, page, and
  effective date. Values are filled from the policy file
  (app/data/policy_cumberland_synthetic.json; no database), never by the model.
- `locked_numbers`: every number exactly as the UI shows it. `/explain`
  requires every number of its fixed English facts in the generated text and
  allows `locked_numbers` too; `/packet` checks each translation against the
  numbers of its own English source (see the 2026-10-17 audit-fix note below).

## 4. Packet - output of `POST /packet` (EngineResult + BillFields + HouseholdAnswers in)

```json
{
  "contract_version": 1,
  "application_fields": [{"label_en": "Account number", "value": "CGH-00482913", "source": "bill"}],
  "checklist": [{"id": "proof_income", "label_en": "", "label_translated": ""}],
  "cover_letter_en": "",
  "cover_letter_translated": "",
  "translation_check": {"numbers_match": true, "fallback_used": false},
  "send_to": {"email": "", "phone": "", "citation": {}},
  "notice_en": "This is a draft you choose to send. The hospital makes the final decision."
}
```
- `source` is `"bill" | "answers" | "policy"`.
- The response is rendered as a printable HTML page (no server PDF).
- Nothing is stored after the response.

- 2026-10-17 ~13:44 CDT: `confidence` is `null` when the model gives no
  per-field score (Command A Vision gives none) and `0.0` when the value is
  null. `/explain` and `/packet` take BillFields + HouseholdAnswers and
  recompute the EngineResult on the server; a client-sent `result` is ignored.

- 2026-10-17 15:25 CDT, still draft (additive, no version bump):
  EngineResult gains `tiers`, the whole policy table for the Result screen,
  in policy order: `[{id, label_en, discount_percent, eligible,
  min_percent_exclusive, max_percent, citation, current}]`. `current` is true
  for exactly the matched tier, marked by position (two tiers share id
  "discount"). `locked_numbers` is unchanged: table numbers are rendered from
  data, never from generated text.

- 2026-10-17 audit fixes (record Appendix AA; additive except where marked):
  - EngineResult gains `policy_hospital_name` (the hospital whose policy was
    applied) and `hospital_matches_policy` (false when the bill names another
    hospital; the UI and packet then warn that the estimate is not about it).
  - Packet `translation_check` is `{numbers_match, fallback_used, translator}`
    with `translator` `"oci_language"` or `"command_a"` (Hindi). It REPLACES
    `back_checked`: no back-translation exists. Hindi now uses the same {n}
    placeholders, so the hospital-name check applies to every language.
  - `/explain` returns `{contract_version, language, text_en, text,
    numbers_match, fallback_used, ai_written}`.
  - Now enforced: `contract_version` must be 1; bill `fields` keys must be the
    six above; a text field value is at most 200 characters;
    `annual_income_cents` at most 10^12; `/extract` checks the PNG/JPEG
    file signature (415 otherwise).
  - `/extract`, `/explain` and `/packet` return 429 after 40 requests per 60 s
    from one client IP.

- 2026-10-17 18:30 CDT, F10 (branch f10; additive, no version bump). Fixed
  BEFORE the agents start; agents code against exactly these names.
  - app/data/demo_bills.json: `{"synthetic": true, "note_en": str, "bills":
    [{"id": str, "label_en": str, "fields": BillFields.fields}]}`; every field
    has `confirmed: true`, `confidence: null`. Five bills (PRD F10.1).
  - Policy JSON adds `coverage_period`: `{"days_before_application": 240,
    "days_after_approval": 180, "text_en": str, "citation": {..., "url":
    "/policy-cumberland.html#page-3", "page": 3}}` and top-level
    `"rules_review_by": "2027-01-13"`.
  - `POST /household` in: `{"answers": HouseholdAnswers, "bill": BillFields
    or null}` (the user's confirmed bill, optional). Out: `{contract_version,
    as_of, eligible, tier: {id, label_en, discount_percent, eligible,
    citation}, percent_of_fpl, bills: [{id, label_en, source: "demo"|"yours",
    hospital_name, statement_date, date_of_service, amount_due_cents,
    reduction_cents, deadline: {date, text_en, citation}}], estimate_cents,
    estimate_text_en, one_application_covers_all, coverage: {text_en,
    citation}, earliest_deadline: {date, text_en, citation}, contacts,
    locked_numbers}`. reduction_cents = amount_due_cents x discount_percent
    // 100. estimate_text_en = "Up to $X could be reduced if the hospital
    approves." (X formatted like amounts, 2 decimals), or "Not eligible under
    this policy." when not eligible. as_of = the server's local date.
  - `GET /stats` out: `{contract_version, since (server start, UTC, minute
    precision), counts: {photos_read, results_free_care, results_discount,
    results_not_eligible, packets, fallbacks, household_views}, languages:
    {code: n}, rules: [{rule_en, source, page, effective_date}],
    rules_review_by}`. Every count under 10 is the string "<10". Not rate
    limited. Counts live in server memory only and reset on restart.
