# Handoff

## Goal

**Mission (decided 2026-10-17 ~13:05 CDT; product name is a placeholder):**
[Name] turns a photo of a Nashville hospital bill into that hospital's
financial assistance packet - eligibility estimate against the hospital's own
published policy (every rule cited), pre-filled application fields, document
checklist, deadline and cover letter - explained in Arabic or Spanish for the
family member helping a parent. The AI reads and phrases; a rules engine
decides; the family submits; the hospital decides. Nothing is stored.

Why this and not the earlier Bill Decoder: the bill/EOB error-checker space
is crowded (research brief), uninsured families get no EOB, and the
unclaimed-help gap is documented (Dollar For's survey: 29% of patients with
unaffordable bills learned about, applied for and received charity care -
via the plan's ClearHealthCosts source, not re-read by Claude). Full plan:
`PRD_ROADMAP.md`, section "CURRENT DIRECTION (forked 2026-10-17)".

**Hard deadline: hacking finishes Sun 2026-10-18 1:00 PM CDT.** Venue closes
Sat 9:00 PM, reopens Sun 9:00 AM (`docs/Hackathon Schedule.txt`).

## Current state - Plan adopted, no code yet

**Last updated: 2026-10-17 ~13:05 CDT** - this file is the only live
snapshot; history lives in the record (Phase 0, Appendices A-O).

> **2026-10-17 - Pivot adopted (record Appendix M).** Evan adopted the draft
> "HackTN26 Health Access Plan" with a Python (FastAPI) + plain HTML/JS stack
> on the OCI VM. The Bill Decoder PRD is kept above the fork as SUPERSEDED.

| Item | Status | Source |
|---|---|---|
| Event / track | TNHacks26, Track 2 (`docs/#2 Health Access, Equity + Experience.txt`) | Evan |
| Agenda and deadline | Known: `docs/Hackathon Schedule.txt`; timeline.md | Evan |
| Judging | `docs/rubric.txt` (Communication, Social Impact, Credibility, Problem Validation, UX, works + uses OCI); no weights | Evan |
| Submission form / repo / video | **UNKNOWN** - ask organizers | - |
| Team roster and roles | **UNCONFIRMED** (plan assumes 4) | - |
| OCI account | Exists (tenancy root compartment); Chicago home region per kit guidance | console pastes |
| Starter kit stack `HackTN26-starterkit` | Apply job started (A1.Flex 2/12, HeatWave only); **result, VM IP, key not reported yet** | Evan |
| Budget alert | **UNCONFIRMED** | - |
| Generative AI access (Command A Vision) | **WORKS** in Playground: 6/6 fields on bill-01.png (n=1, clean image) | experiments.md |
| VUMC policy thresholds | **UNVERIFIED** - 3:00 PM Sat gate, else synthetic hospital | plan |
| Code | None | - |
| Old-plan artifacts | Synthea snapshot (`data/synthea/`, gitignored), JDK 17 + Synthea jar in `C:\Users\daruw\tools\` - optional now | record H |

## Architecture (PRD fork F2)
- FastAPI app on the OCI VM, endpoints `/extract`, `/evaluate`, `/explain`,
  `/packet`; stateless.
- OCI Generative AI: Cohere Command A Vision (read bill), Command A (phrase);
  OCI Language (translate + back-translate check); MySQL HeatWave policy
  registry (cut to JSON if short).
- Number lock on all generated text; printable HTML packet (no server PDF).

## Documentation
- `PRD_ROADMAP.md` - CURRENT DIRECTION fork at the end is the plan.
- `docs/Project Record - Full Chronological History.md` - append-only record;
  append with `node C:\Users\daruw\.claude\skills\project-memory\append-record-entry.js`.
- `docs/research/2026-10-17_bill-decoder-crowding.md` - competitor research.
- `.claude/project-memory/` - bins; `important.md` first, then `INDEX.md`.
- `.claude/pm-cadence.json`, `.claude/drift-check.stamp` - local, gitignored.

## BLOCKED-ON-EVAN
- Starter-kit apply result, VM public IP, SSH key saved at
  `C:\Users\daruw\.ssh\HackTN26.pem`; budget alert.
- First Generative AI call (Playground in the console, Chicago).
- Ask organizers: submission form, repo, video.
- Team roster and who owns which role.
- Any email to VUMC or Dollar For (outward-facing; Evan sends).

## Next actions (PRD fork F6 gates)
1. ~1:45 PM: one successful Command A Vision call on the synthetic bill
   (`spikes/synthetic-bill/`); agree the 4 JSON shapes.
2. 3:00 PM: VUMC rules from VUMC's own PDF, or the synthetic hospital.
3. 5:00 PM: bill photo -> cited eligibility result on the OCI server.
4. Validation V1 (general-AI test) in parallel, today.
