STATUS: pointer (2026-10-18 07:43 CDT) - Built: 5-screen journey (start, bill, three questions, result, packet), 32 languages LIVE since 2026-10-18 00:07 CDT (5af2f1f, record AR). Also built and LIVE (record AH): F10.1 Home/all bills, F10.2 coverage rule, F10.3 reminders + .ics, F10.4 QR chip + Start QR, F10.5 dashboard. Roadmap: PRD F11 (DRAFT).

- 2026-10-18 00:05 CDT - Roadmap evidence (agent briefs, record AQ; not
  cold-assessed): docs/research/2026-10-17_customer-features-brief.md ranks
  10 candidates (top: real Nashville policies, an over-income path,
  human-help handoff, collections protection) and argues to cut F11.7 push
  reminders (Evan dropped it, record AP). Real-policy encoding needs schema
  work first: residency lists, minimum balance, catastrophic rules, an
  uninsured-only flag and a "from service" window anchor
  (docs/research/2026-10-18_middle-tn-hospital-policies.md).
- 2026-10-18 10:23 CDT - built and live (e53d1ce, records AY, AZ): a bill with no hospital name gets
  the no-policy path everywhere (Result: warning, no estimate, /packet 422; Home: listed, not counted,
  no-name note); Home hides one-approval, reminders, calendar and the policy contact unless the user's
  bill matches. VUMC conditions start with "help is for uninsured/underinsured" (FAP p.4, p.6). NOT
  built: using insurance_status in the estimate (the engine ignores it), pending-insurance detection.
- 2026-10-18 10:34 CDT - built, NOT deployed (223013b, record BA): Apply by counts from the date of service when
  known and earlier than the statement (deadline.counted_from), so it can only be earlier than the policy deadline.
- 11:11 CDT - Phase 2 "Find errors" BUILT on f12, NOT live: charge lines read + confirmed, fixed-rule checks (duplicate,
  lines_sum, due_mismatch, insurance_unpaid, medicaid w/ 42 CFR 438.106), "Things to ask the hospital about" card, fixed
  English letter (/dispute). Product name is Billow (cbc815b, not deployed).
- 2026-10-18 11:56 CDT - LIVE ba6d1f0: Phase 3 insurance check (EOB photo or "Not yet"; pending, different visit, denied,
  charged more / not on EOB / totals / credit / billed more; insurer letter). Built, NOT live (a0684aa): Remove photo on the
  Bill screen; Sources in a dropdown closed by default (records BE, BF).
- 2026-10-18 12:14 CDT - LIVE 189163e: one "This is correct" box per screen (bill 6 fields, EOB 12 fields) instead of one
  per field; pending flag asks whether you can wait; dashboard counts checks_run, disputes, eobs_read (record BH).
- 2026-10-18 13:11 CDT: Start screen shows a second QR (>= 900 px) to /test-bills/: 17 synthetic bills + 5 bill/EOB pairs to download, SYNTHETIC banner (df69369, record BM).
- 2026-10-18 14:37 CDT: EOB screen button 'No Explanation of Benefits Available' (was 'Not yet'), never disabled; its pending card/letter say the person has no insurer summary yet; a real pending claim status keeps 'still processing' (8cd1d09, record BN).
- 2026-10-18 15:02 CDT: reader handles real-format bills/EOBs (allowed/deductible/copay/coinsurance, payment parts, codes, ledger rows dropped, date ranges, abbreviated provider names); EOB screen has 5 optional fields; QR page has real-format pairs 11 and 12 (041fe7e, NOT deployed; record BO).
