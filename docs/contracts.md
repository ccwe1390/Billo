# JSON contracts - DRAFT for team agreement (PRD fork F6 gate ~1:45 PM)

Drafted 2026-10-17 ~13:20 CDT by Claude. Each shape changes only by team
agreement; when one changes, bump `contract_version`.

Rules that apply to all four:
- **Money:** integer cents (`4812.40` -> `481240`), never floats.
- **Dates:** `YYYY-MM-DD`.
- **Languages:** `"en" | "es" | "ar"`.
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
  effective date. Values are filled from the policy registry (JSON or
  HeatWave), never by the model.
- `locked_numbers`: every number exactly as the UI shows it. `/explain` and
  `/packet` check generated text against this list.

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
