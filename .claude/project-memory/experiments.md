# experiments - TNHacks26

- 2026-10-17 - Headline experiment (planned, not run): precision and recall
  per error type, on a seeded synthetic set of bill+EOB pairs built from
  Synthea with errors 1-6 planted (decisions.md) and ~1/3 clean pairs to
  expose false alarms. Measured twice: (a) rules on the structured answer-key
  JSON = upper bound; (b) image -> OCI Document Understanding -> rules = the
  real headline. Demo number = dollars flagged on the same set. No real-world
  savings claim. Exact counts are set in PRD_ROADMAP.md.
