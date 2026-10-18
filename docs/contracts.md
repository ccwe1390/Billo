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

- 2026-10-17 23:30 CDT - audit 2 fixes (record AL; docs/2026-10-17_audit-2.md):
  - `hospital_matches_policy` (EngineResult and every /household bill row) is
    true, false or null; null = the bill names no hospital (unknown, no
    warning). A match needs the bill name (after an optional leading "The")
    to start with the policy hospital name.
  - /household rows with `hospital_matches_policy` false are listed but not
    counted: excluded from `estimate_cents`, `one_application_covers_all` and
    `earliest_deadline`. `one_application_covers_all` is also false when the
    household is not eligible or no row was counted. A user bill whose
    account number (trimmed) equals a demo bill's replaces that demo bill's
    fields.
  - /explain line 3 for a not-eligible tier has no deadline sentence; the
    letter says "about N%".
  - Field `value` is null, text or a number only (lists/objects -> 422);
    control characters become spaces; `amount_due_cents` <= 10^12;
    `date_of_service`, when present, must be YYYY-MM-DD. EvaluateIn and
    ResultIn reject unknown top-level keys.
  - 422 bodies are `{"detail": [{loc, msg, type}]}` (no input echo); a
    /household 422 detail is "A date or amount is not valid."
  - Limits: 429 after 60 paid requests per 60 s per client IP or 600 paid
    requests per hour in total; /extract with Content-Length over 8 MiB +
    64 KiB -> 413 before parsing. Supersedes "40 requests per 60 s" above.

## Addendum 2026-10-18 08:51 CDT - real policies (bdc76df; record AV)
- The server holds three policies (app/data/policy_vumc.json, policy_ascension_saint_thomas.json,
  policy_cumberland_synthetic.json; default vumc). /evaluate, /explain and /packet pick the policy by
  the bill's hospital_name (whole-word prefix match on each policy's match_names; exclude_names win).
- hospital_matches_policy false now means "no policy for this hospital": the result is the default
  policy's shape, the UI shows no estimate, /explain makes no OCI call, /packet returns 422
  "No application packet: this demo has no policy for this hospital."
- EngineResult and /household gain "conditions" [{text_en, citation}] and "synthetic" (bool); a
  not-eligible tier may carry "other_route_en"; documents may carry "url"; contacts.email may be null.
- coverage_period may be null (then coverage.text_en = the policy's coverage_note_en and
  one_application_covers_all is false); days_before_application / days_after_approval may be null.
- /stats gains "policies" [{hospital_id, hospital_name, rules_review_by}]; rules_review_by is the
  earliest across policies; "rules" still lists the default policy.
- /packet?format=json returns the Packet shape (the default is HTML).

## Addendum 2026-10-18 10:19 CDT - no hospital name (f6b6f05, f2c2135; audit 4 B2, landing check)
- EngineResult (/evaluate) gains "hospital_name_missing" (bool): true when the bill shows no hospital
  name (blank, whitespace or not text); then hospital_matches_policy is false (no estimate, /explain
  makes no OCI call). /packet returns 422 "No application packet: the bill shows no hospital name."
  (checked before the no-policy 422).
- /household rows keep hospital_matches_policy null for a bill with no hospital name, but such a row
  is now listed and NOT counted, like a false row: excluded from estimate_cents,
  one_application_covers_all and earliest_deadline. Supersedes "null = unknown, no warning" in the
  2026-10-17 23:30 addendum; Home shows the no-name note on that row.

## Addendum 2026-10-18 10:29 CDT - deadline anchor (feature review flaw 2)
- deadline.date counts days_from_statement from the bill's date_of_service when it is known and earlier
  than statement_date, else from statement_date. The policies count from the FIRST bill after discharge,
  which is never before the date of service, so the date can only move earlier, never too late.
- deadline gains "counted_from": "date_of_service" | "statement_date"; text_en uses the policy's new
  application_window.service_template_en ("To be safe we counted ... your real deadline is this date or
  later") or the existing text_template_en ("if not, your deadline is earlier"). /household rows and
  earliest_deadline follow. The bill-01 example date above becomes 2027-05-10 (service 2026-09-12).

## Addendum 2026-10-18 10:51 CDT - Phase 2 error checks (f12, NOT live until deployed)
Everything below is on branch f12 only. Live is 08265fa until f12 is deployed. contract_version stays 1
(all changes are additive).

### insurance_status gains "medicaid" (REPLACES docs/contracts.md:36)
- This REPLACES the 3-value list at docs/contracts.md:36, which currently reads: insurance_status is one
  of "self_pay" | "insured" | "unknown". The allowed values are now FOUR: "self_pay" | "insured" |
  "medicaid" | "unknown".
- The server maps model free text containing "tenncare" or "medicaid" (any case) to "medicaid" BEFORE the
  general insured match. Packet label for it: "TennCare / Medicaid".

### BillIn.lines (optional; the engine ignores it and reads bill["fields"] only)
- lines: {items, total_charges_cents, payments_cents, confirmed, read}
  - items: list of at most 40 of {date: YYYY-MM-DD | null, description: string of at most 120 chars,
    quantity: int 1..999 | null, amount_cents: int 0..10^9 | null}
  - total_charges_cents: int | null
  - payments_cents: int >= 0 | null (a minus sign or parentheses are stripped, so it is never negative)
  - confirmed: bool (the user ticked "These charges match my bill")
  - read: bool (true when the model returned a line_items key, false when the user typed the lines)
- lines may be null or absent. The vision step (S4, separate) is meant to fill lines with read true, confirmed false.

### POST /check (new; free)
- Request: {bill} (a BillIn, with lines). Response:
  {contract_version, flags: [{id, text_en, letter_en, amount_cents, line_indexes, citation}],
  total_to_ask_cents, lines_checked}
  - id: one of the flag ids below. text_en: the card line shown to the user. letter_en: the sentence used in
    the dispute letter. amount_cents: int | null. line_indexes: list of item indexes (may be empty).
    citation: {source, url} | null (only the medicaid flag has one).
  - total_to_ask_cents = min(sum of the flag amount_cents that are not null, amount_due_cents): you cannot
    ask about more than you owe, and lines_sum and due_mismatch can overlap.
  - lines_checked: bool, false when lines are null or items is empty (the line rules did not run).
- Free: no OCI call, no AI. NOT rate limited and not counted in the paid totals. The 64 KiB JSON body cap
  still applies (413 before parsing).
- 422 unless every bill field is confirmed and, when lines.read is true, lines.confirmed is also true.
  422 bodies keep the {"detail": [{loc, msg, type}]} shape.
- Works for a hospital with no policy and for a bill with no hospital name: errors do not depend on the
  assistance policy.

### POST /dispute (new; rate limited)
- Request: {bill, answers}. Response: an HTML page (the letter), like /packet. With ?format=json:
  {letter_en, letter_translated, translation_check}.
- The letter is a fixed English template, never AI-written. Translation uses OCI Language (Command A for
  hi); the hospital name and every flagged charge description stay English; the number lock covers the
  whole letter and a mismatch falls back to English only. No contact is invented. A bill with no hospital
  name gets the salutation "To the Billing Office:".
- 422 when the bill has no flags (same checks as /check, so the same 422 rules for unconfirmed input).
- Rate limited: it translates, so it counts as paid.
- The paid-routes set becomes {/extract, /explain, /packet, /dispute} (was {/extract, /explain, /packet});
  the 60 per 60 s per IP and 600 per hour limits in the 2026-10-17 addendum now count /dispute too.

### Flag ids and when each fires (no AI, fixed rules, in app/checks.py)
- duplicate: two or more items share the same (date, normalized description, amount_cents); normalized =
  lowercase, punctuation removed, whitespace collapsed; two null dates count as equal. amount_cents =
  item amount x (count - 1). Stays quiet for the same description on different dates, "first hour" vs
  "each additional hour", and the same description at different amounts. Needs lines.confirmed.
- lines_sum: every item amount is read, total_charges_cents is read, and sum(items) != total. amount_cents =
  total - sum when positive, else null (still flagged). Needs lines.confirmed.
- due_mismatch: total_charges_cents and payments_cents are both read and amount_due_cents != total -
  payments. amount_cents = amount_due - expected when positive, else null. Needs lines.confirmed.
- insurance_unpaid: insurance_status is "insured", lines.confirmed is true, payments_cents is exactly 0 (null does not count) and
  amount_due_cents > 0. amount_cents null. payments_cents null never fires it, so it needs payments in lines.
- medicaid: insurance_status is "medicaid" and amount_due_cents > 0. amount_cents null. Carries a citation
  {source: "42 CFR 438.106 (eCFR, current to 2026-10-15)", url:
  "https://www.ecfr.gov/current/title-42/chapter-IV/subchapter-C/part-438/subpart-C/section-438.106"}.
  Runs without lines: the insurance rules still run when lines are null or were not confirmed.
- There is no no_items flag; an empty or missing item list is reported only as lines_checked false.
- The line rules (duplicate, lines_sum, due_mismatch) run whenever lines.confirmed is true, whether the lines
  were read or typed; when lines are null or not confirmed they do not run.

## Addendum 2026-10-18 11:24 CDT - Phase 3 insurance check (EOB) (branch f13, not merged, not deployed)
Everything below is on branch f13 only. contract_version stays 1 (all changes are additive).

### POST /extract
- New multipart fields: kind ("bill" default | "eob") and date_of_service (YYYY-MM-DD, optional; it fills the
  EOB prompt). kind=eob returns an EOB object. A photo that is not an EOB -> 422 "This doesn't look like an
  insurance summary." Any other kind value -> 422. Still a paid, rate-limited route.

### EOB object
- {contract_version: 1, fields: {insurer_name, provider_name, date_of_service, claim_number, claim_status
  (paid | partially_paid | denied | pending | null), amount_billed_cents, plan_discount_cents,
  plan_paid_cents, patient_owes_cents, denial_reason, appeal_deadline, insurer_phone}, lines}
  - each field is {value, confidence, confirmed}. Unknown field names -> 422.
  - lines: {items: [{date, description, amount_billed_cents, patient_owes_cents}] (at most 40 items,
    description at most 120 chars), confirmed, read} | null.
- Never read or stored: member ID, group number, names.

### POST /check and POST /dispute
- Both accept eob and eob_not_yet (bool). eob must be confirmed (every field, and the lines when present),
  else 422.
- /check returns {flags, total_to_ask_cents, lines_checked, insurer_letter}. Each flag gains kind: "bill" |
  "insurance".
- Insurance flag ids: pending, different_visit, denied, charged_more, not_on_eob, totals_mismatch,
  credit_mismatch, billed_more.
- Run order: pending stops the insurance rules. A different visit (date, or provider name not matching after
  normalizing) stops them. denied (the bill asks the full amount) stops them. Then the line and total rules
  run for paid / partially_paid.
- Lines match by (date, amount), never by wording. A line with no date takes its document's date of service.

### Merging with Phase 2
- Phase 2's duplicate flag is dropped when charged_more covers the same lines. insurance_unpaid is dropped
  when the EOB is paid / partially_paid / denied (kept for pending / not yet).
- total_to_ask_cents: with a usable paid EOB, amount due - EOB patient owes when that is more than $1.00,
  else 0; otherwise Phase 2's total. Never counted twice.

### /dispute letter and stats
- The billing-office letter lists each flag that has a letter line. When the claim was denied the page also
  carries a fixed English letter to the insurer ("please reconsider"), translated beside it under the same
  number lock, with the deadline and phone exactly as printed on the summary.
- stats gains eobs_read.
