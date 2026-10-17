# Pre-Mortem - TNHacks26 "Bill to Help" demo and submission

## Session Details

| Field | Value |
|-------|-------|
| **Product / Feature** | Bill to Help: live demo, pitch and submission |
| **Planned Launch Date** | 2026-10-18 (hacking ends 13:00 CDT; final pitches 15:30) |
| **Pre-Mortem Date** | 2026-10-17 14:59 CDT |
| **Facilitator** | Claude (Opus 5.5), solo draft |
| **Participants** | None besides Claude. Evan has not reviewed it yet. |

**Assumptions (no session was held):** The failure is pictured on Sun
2026-10-18 at 17:00, after the awards: "we did not place, or the demo broke."
Every risk below cites evidence from the repo or the session. The
urgency labels are redefined for a 22-hour horizon: Launch-Blocking = before
the Sat 23:00 freeze; Fast-Follow = before Sun 12:00; Track = watch,
act on a tripwire.

## Summary

| Metric | Count |
|--------|:-----:|
| **Total Risks Identified** | 18 |
| **Tigers** | 10 |
| -- Launch-Blocking | 5 |
| -- Fast-Follow | 3 |
| -- Track | 2 |
| **Paper Tigers** | 4 |
| **Elephants** | 4 |

(Counts from `risk_categorizer.py` on the input JSON.)

## Tigers (Real Risks)

### Launch-Blocking (before Sat 23:00)

| # | Risk | Evidence | Mitigation | Owner | Decide by |
|---|------|----------|-----------|-------|-----------|
| T1 | Submission requirements (form, repo, video) unknown | HANDOFF: UNKNOWN since the morning. The event page mentions judges "evaluating the video presentations" | Ask organizers in Slack now. If a video is required, record it Sun ~11:00 together with the backup | Evan | Sat 17:00 |
| T2 | Problem Validation has zero evidence | Rubric: "Have real customers provided input?" No V1-V3 results exist. The venue closes at 21:00 | Run V1 (the chatbot test, ~45 min, no people needed) next. Do interviews at dinner check-in (18:00) | Evan / team | Sat 21:00 |
| T3 | The journey has never run on a phone with a real camera photo | Every live run used rendered PNGs. Upload accepts only `image/png,image/jpeg` with an 8 MB cap (app.js:185, main.py) | Evan photographs a printed bill-02 on his phone against the live URL. If it is slow or rejected, Claude adds in-browser downscaling (~2000 px JPEG) before upload | Evan, then Claude | Sat 19:00 |
| T4 | DONE 15:06 (145c8af, live) - A "Content pending" placeholder showed on the result screen | app.js:57 / app.js:341 | Hide the card until sourced text exists; a sourced Tennessee summary is optional | Claude | Sat 18:00 |
| T5 | DONE 15:40 (c689291, live; checks in record W) - The redesign breaks the working demo | Design agent running; 11 languages + RTL; UI checks are manual | Redesign changes CSS and markup only, never the API calls. Deploy only after a scripted journey run plus a browser check in en/ar/zh-CN. Keep the last good commit to roll back to | Claude | Sat 23:00 |

### Fast-Follow (before Sun 12:00)

| # | Risk | Evidence | Plan | Owner | Target |
|---|------|----------|------|-------|--------|
| T6 | No recorded backup; the live demo depends on venue Wi-Fi, one VM and ~12 s of model calls | Server journey 11.8 s; single E5.Flex VM | Record the full journey Sun ~11:00 and label it "recorded this morning". Rehearse once on venue Wi-Fi | Evan | Sun 11:00 |
| T7 | Pitch statistics unverified (29%, 52%, $14B, 2,984, 95,000) | Rev-2 plan: "open each before putting its number on a slide" | Open every source; cut any number that can't be confirmed | Claude (research) + Evan | Sun 10:00 |
| T8 | MOSTLY DONE 16:01 (MySQL + HeatWave deleted, record X; budget alert still open) - The HeatWave cluster and the E5.Flex VM may bill; budget alert unconfirmed | operations.md: HeatWave.32GB Always-Free status UNVERIFIED; VM confirmed E5.Flex | Check Billing -> Cost analysis; set a budget alert; delete the HeatWave cluster if unused (the app stores nothing) | Evan | Sat 18:00 |

### Track

| # | Risk | Evidence | Metric | Tripwire |
|---|------|----------|--------|----------|
| T9 | AI-written es/ar/zh interface strings have errors | All marked TODO-REVIEW | Errors found by a fluent reviewer | Any error on a demo-path screen -> fix it before freeze |
| T10 | Plain HTTP shows "Not secure" on a page asking for income | Port 443 closed; no domain | A judge mentions it | If a judge asks: "a pilot runs inside the partner's login over HTTPS" |

## Paper Tigers

| # | Risk | Why it's a paper tiger | Becomes a Tiger if |
|---|------|------------------------|--------------------|
| P1 | OCI model outage during the demo | 3 OCI services (Command A Vision, Command A, Language) ran live; two bugs were found and fixed on the way (corrected 2026-10-17 16:57 CDT (audit, record Z/AA)); recording + FAKE_OCI switch are fallbacks | A live call fails during a rehearsal |
| P2 | Model costs exceed $500 | ~3 short calls per journey | Cost analysis shows more than $20/day |
| P3 | Server overload at the showcase | Stateless, 2 vCPU, a handful of users | Rehearsal latency exceeds 30 s |
| P4 | Judges call it a copy of CareRoute or B.A.R.S. | Prior art named in PRD F8, with answers prepared | A judge cites a feature we lack |

## Elephants

| # | Unspoken concern | Resolution | Reclassified to |
|---|------------------|-----------|-----------------|
| E1 | If V1 shows chatbots already raise financial assistance and list documents, the core claim collapses, and nobody has run it | Run V1 FIRST (T2). Whatever it shows goes on slide 3; narrow the pitch if needed | Tiger (launch-blocking, merged into T2) |
| E2 | Agents built most of the code; in Q&A the team may not be able to explain it | Evan walks the architecture tonight (engine -> number lock -> instance principal) and prepares an honest "how we built it" answer | Tiger (fast-follow) |
| E3 | The demo hospital is synthetic, so judges may see a toy rather than impact | The 3 PM VUMC gate is passing with nobody having opened VUMC's PDF. Either open it (download needs Evan's OK) or say plainly that VUMC is the next step, with the hospital's sign-off | Accepted unless Evan wants the PDF |
| E4 | Sunday 9:00-13:00 holds more than 4 hours of work | Move V1, interviews, stat checks and the slide draft to Saturday; Sunday = V3, recording, rehearsal, submit | Tiger (launch-blocking schedule) |

## Top 5 actions, in order

1. **Evan, now:** ask organizers in Slack what to submit (T1).
2. **Evan + team, now:** run V1 with the bill image on ChatGPT, Claude and Gemini, using the plan's exact prompt (T2/E1).
3. **Claude, now:** hide the placeholder card (T4); make the redesign safe to deploy (T5).
4. **Evan, before 19:00:** phone-photo test against http://207.211.181.174/ (T3).
5. **Evan, before 18:00:** check billing, set the budget alert, decide on the HeatWave cluster (T8).

## Updates

- 2026-10-17 16:57 CDT (audit, record Z/AA): T3's pointer `app.js:185` is stale; the upload limits now live in
  app/main.py (8 MB, PNG/JPEG signature check) and app.js shows a specific
  message for 413/415/429. T4's `app.js:57 / app.js:341` were removed in
  145c8af. T7's unverified-number list also needs: $7 billion bad debt,
  Tennessee 175% of cost, VUMC 24% of charges, 9.3% uninsured, 282,294
  renewals (docs/2026-10-17_pitch-corrections.md). The HHS 2026 poverty
  values were verified against the Federal Register notice. Counting note:
  E1 merged into T2 and E4 was reclassified after the summary table, so
  "5 launch-blocking" counts T1-T5 only. P4's "answers prepared" was false
  until the pitch-corrections sheet added a B.A.R.S. answer.
