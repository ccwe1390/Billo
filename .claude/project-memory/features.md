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
