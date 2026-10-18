# experiments - TNHacks26

- 2026-10-17 - [SUPERSEDED by the ~13:05 CDT pivot, record M] error checking moved to Deferred. Headline experiment (planned, not run): precision and recall
  per error type, on a seeded synthetic set of bill+EOB pairs built from
  Synthea with errors 1-6 planted (decisions.md) and ~1/3 clean pairs to
  expose false alarms. Measured twice: (a) rules on the structured answer-key
  JSON = upper bound; (b) image -> OCI Document Understanding -> rules = the
  real headline. Demo number = dollars flagged on the same set. No real-world
  savings claim. Exact counts are set in PRD_ROADMAP.md.
- 2026-10-17 ~13:17 CDT - GATE 1 PASSED (n=1): the OCI Generative AI
  Playground, Cohere Command A Vision, Chicago, on
  `spikes/synthetic-bill/bill-01.png` with the strict-JSON prompt. All 6
  fields correct: hospital, statement date, account, amount (returned as the
  number 4812.40), date of service, insurance ("None on file (self-pay)").
  Limits: one clean rendered image, not a phone photo; the acceptance test
  needs 10 bills. This proves the tenancy has the model and that it follows
  the null/no-guess JSON prompt on an easy input.
- 2026-10-17 13:51 CDT - Blur test set ready, NOT yet run against the
  model: spikes/synthetic-bill/bill-02-blur{0,1.5,3,5}.png (date of service
  printed once; statement 10/05/2026 and due 11/04/2026 sit next to it, so
  a guessing model will likely copy one of those). Human read (agent +
  Opus check of blur3): legible at 0, barely at 1.5, unreadable at 3 and 5.
  Pass condition for the 0:14 demo line: date_of_service null at 3 and 5.
- 2026-10-17 14:22 CDT - FIRST LIVE CALLS FROM CODE (gate 1, due ~1:45 PM,
  passed ~37 min late). Model `cohere.command-a-vision` (ACTIVE in Chicago
  per GenerativeAiClient.list_models; 75 models listed), temperature 0,
  n=1 per image, through app.oci_client.extract_bill + main.normalize_bill.
  - bill-01: 6/6 fields correct, 3.9 s.
  - bill-02 blur 0 and 1.5: date of service 2026-09-20 correct.
  - bill-02 blur 3 and 5: date_of_service null (no guess). PASS for the
    0:14 demo line - n=1 each, clean rendered PNGs, not phone photos.
  - Hospital name dropped "(SYNTHETIC)" on 3 of 4 bill-02 runs; all other
    fields exact. Latency 3.2-3.9 s per bill.
  - BUG found: the model wrapped its JSON in a ```json fence despite
    CohereResponseJsonFormat, so json.loads failed (spike printed "NOT
    valid JSON"); the app would have returned 502 on every real /extract.
    Fixed: oci_client.parse_json_object falls back to the outermost {...};
    test added in tests/test_api.py.
- 2026-10-17 14:53 CDT - GATE 2 (5:00 PM gate) PASSED ~2 h early, on the
  OCI server http://207.211.181.174/ with real AI (instance principal):
  bill-02-blur3 -> /extract 4.1 s (date_of_service null, person types it)
  -> /evaluate 0.1 s (115%, free care, deadline 2027-06-02, cites p.1) ->
  /explain es 4.4 s (Command A, number check passed) -> /packet es 1.1 s.
  Total 9.7 s. n=1.
  - Packet translation FAILED the number check: OCI Language rewrote
    "$4,812.40" as "$4.812,40" (es). Placeholder test (8 languages, n=1):
    {n} and X{n}X survived es/fr/de/ru/ar/zh-CN/ko/vi; [[n]], <n>, #n#
    did not. Fix: numbers -> {n} before OCI Language, restored after
    (oci_client.protect_numbers/restore_numbers). Re-run live: es, fr, de,
    ru, ar, zh-CN, ko, vi packets all numbers_match=True. Server re-run
    14:55: full journey 11.8 s, packet es numbers_match=True.
  - Not tested live: zh-TW and hi packets (hi uses Command A, unprotected).
- 2026-10-17 ~15:55 / 16:07 CDT - OCI Language and proper nouns. Before
  the fix (reviewer screenshots, n=1 per language): the hospital name
  "Cumberland General Hospital (SYNTHETIC)" came back as "(MONOETIC)" (ar,
  zh-TW) and "CETIC" (zh-CN); zh-TW also dropped "Financial Assistance
  Office"; "this application" became "this app" in ar/zh-CN/zh-TW. After
  protecting the name with {n} placeholders and rewording the letter
  (116d631), live run n=1 each: ar, zh-CN, zh-TW, es, fr, de, ru, ko, vi all
  kept the name verbatim and passed the number check; no "app" wording in
  ar/zh-CN/zh-TW; zh-TW kept the office name.
- 2026-10-17 (run by Evan, logged 18:03 CDT) - V1 chatbot test (pre-mortem
  T2/E1). Raw answers: docs/AI Test.txt. Input: spikes/synthetic-bill/bill-01
  image (Cumberland General, SYNTHETIC) + the rev2 prompt; ARA runs used the
  Arabic prompt and then a follow-up "also give responses in english" (a
  deviation; scored on content, which matched). Free tiers: Gemini (Auto),
  Claude (Sonnet 5.5, medium effort), ChatGPT (free model, name not
  recorded). 14 runs started, 13 complete: Gemini 3 EN + 3 AR (AR run 5
  truncated mid-answer, scored N/A), Claude 3 EN + 3 AR, ChatGPT 2 EN (EN
  run 3 hit the free upload cap, "wait 23 hours"; 0 AR runs). Scored by
  Claude on the revised sheet (rev2 checks 2 and 4 named VUMC, which no
  chatbot can pass on a fictional hospital):

  | Check (complete answers) | Gemini | Claude | ChatGPT | Total |
  |---|---|---|---|---|
  | c1 raises financial assistance unprompted | 5/5 | 6/6 | 2/2 | 13/13 |
  | c2 asks for or uses household size AND income | 0/5 | 0/6 | 2/2 | 2/13 |
  | c3 gives the assistance APPLICATION window (strict) | 0/5 | 0/6 | 0/2 | 0/13 |
  | c3 lenient: an action deadline (always the 10/31 payment due date) | 4/5 | 6/6 | 0/2 | 10/13 |
  | c4a invents hospital-specific limits or documents | 0/5 | 0/6 | 0/2 | 0/13 |
  | c4b points to the hospital's own written policy or income cutoffs | 0/5 | 6/6 | 1/2 | 7/13 |
  | c5 produces a filled application or ready-to-send letter | 0/5 | 0/6 | 0/2 | 0/13 |

  Also seen: no answer estimated eligibility or named the 240-day window
  (our app: free care up to 200% FPL, deadline 2027-05-29); every dated
  answer treated the payment due date as THE deadline; Claude 6/6 and
  ChatGPT 2/2 raised TennCare, Gemini 0/5; Gemini gave generic "50-100%"
  reduction and "20-60%" self-pay ranges; the SYNTHETIC watermark was noted
  by ChatGPT 2/2, Claude 1/6, Gemini 0/5; Gemini offered to draft a letter
  or script, and Gemini AR run 6 wrote a call script (not a letter).
  Scoring calls (Claude's, Evan may override): c2 needs the answer to ask
  the user or compute, not just name the factors; c3 strict excludes the
  payment due date. Limits: n=13, one bill, one evening, free tiers that
  change week to week, unequal ChatGPT sample, one scorer.
- 2026-10-18 08:49 CDT - live /extract (real OCI, n=1) on the RE-RENDERED synthetic bills (bdc76df,
  VUMC/Ascension names): bill-02-blur0 read "Vanderbilt University Medical Center (SYNTHETIC)",
  $1,858.50 (4.3 s http / 3.7 s https); bill-06 read "Ascension Saint Thomas Midtown (SYNTHETIC)"
  (3.6 s); bill-02-blur3 read date_of_service 2026-11-04 = the PAYMENT DUE date (WRONG; the old
  2026-10-17 render left it null). The "left the blurry date blank" claim is not true for the new
  render; the confirm step is the safeguard.
