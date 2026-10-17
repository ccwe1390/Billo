# experiments - TNHacks26

- 2026-10-17 - Headline experiment (planned, not run): precision and recall
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
