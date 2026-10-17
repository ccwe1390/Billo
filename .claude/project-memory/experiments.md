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
