# Handoff

## Goal

**Mission (decided 2026-10-17 ~13:05 CDT; product name is a placeholder):**
[Name] turns a photo of a Nashville hospital bill into that hospital's
financial assistance packet - eligibility estimate against the hospital's own
published policy (every rule cited), pre-filled application fields, document
checklist, deadline and cover letter - explained in 11 languages (Arabic, Spanish and Chinese with a translated
interface) for the family member helping a parent. The AI reads and phrases; a rules engine
decides; the family submits; the hospital decides. Nothing is stored.

Why this and not the earlier Bill Decoder: the bill/EOB error-checker space
is crowded (research brief), uninsured families get no EOB, and the
unclaimed-help gap is documented (Dollar For's survey: 29% of patients with
unaffordable bills learned about, applied for and received charity care -
via the plan's ClearHealthCosts source, not re-read by Claude). Full plan:
`PRD_ROADMAP.md`, section "CURRENT DIRECTION (forked 2026-10-17)".

**Hard deadline: hacking finishes Sun 2026-10-18 1:00 PM CDT.** Venue closes
Sat 9:00 PM, reopens Sun 9:00 AM (`docs/Hackathon Schedule.txt`).

## Current state - LIVE on OCI at http://207.211.181.174/ (gates 1 and 2 passed)

**Last updated: 2026-10-17 18:04 CDT** - this file is the only live
snapshot; history lives in the record (Phase 0, Appendices A-Y).

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
| Starter kit stack / VM | Re-apply succeeded 13:15 CDT. VM 207.211.181.174, E5.Flex 1 OCPU (paid), Oracle Linux 9.8, Python 3.12 venv in /opt/bill-to-help, systemd + Apache proxy on :80. SSH key at `C:\Users\daruw\.ssh\HackTN26.pem`. Auth to OCI = instance principal. | operations.md |
| Budget alert | **UNCONFIRMED** | - |
| Generative AI access (Command A Vision) | **WORKS FROM CODE** 2026-10-17 14:22: `cohere.command-a-vision`, bill-01 6/6, blur test passed (null at blur 3 and 5), n=1 each | experiments.md |
| VUMC policy thresholds | **UNVERIFIED** - 3:00 PM Sat gate, else synthetic hospital | plan |
| Code | Engine (+ full tier table) + FastAPI app + 5-screen "Paper Trail" UI + synthetic policy page + blur test bills + language tiers (tier 1 en/es/ar/zh-CN/zh-TW; tier 2 vi/fr/ko/ru/de/hi); 4 test files ALL PASS; live with real OCI since 14:53; the live server runs c4a28f0 (audit fixes, deployed 16:58 CDT, live journey 10.7 s; operations.md) | record P-W |
| Old-plan artifacts | Synthea snapshot (`data/synthea/`, gitignored), JDK 17 + Synthea jar in `C:\Users\daruw\tools\` - optional now | record H |

## Architecture (PRD fork F2)
- FastAPI app on the OCI VM, endpoints `/extract`, `/evaluate`, `/explain`,
  `/packet`; stateless.
- OCI Generative AI: Cohere Command A Vision (read bill), Command A (phrase);
  OCI Language (translate). No back-translation: numbers and the hospital
  name are swapped for {n} placeholders, then the number lock checks the
  result (Hindi: Command A with the same placeholders). Policy rules are a
  JSON file (app/data/policy_cumberland_synthetic.json); no database
  (MySQL/HeatWave was never used and is deleted).
- Number lock on all generated text; printable HTML packet (no server PDF).
- Limits: text fields <= 200 chars; 40 paid requests (/extract, /explain,
  /packet) per 60 s per client IP (last X-Forwarded-For entry; if Apache does
  not add it, the 40/min cap is shared by everyone); uploads stay in memory.

## Documentation
- `PRD_ROADMAP.md` - CURRENT DIRECTION fork at the end is the plan.
- `docs/Project Record - Full Chronological History.md` - append-only record;
  append with `node C:\Users\daruw\.claude\skills\project-memory\append-record-entry.js`.
- `docs/research/2026-10-17_bill-decoder-crowding.md` - competitor research.
- `docs/2026-10-17_pre-mortem.md` - 18 risks; 5 launch-blocking before the
  Sat 23:00 freeze (submission rules, validation, phone test, placeholder
  card, redesign safety).
- `.claude/project-memory/` - bins; `important.md` first, then `INDEX.md`.
- `.claude/pm-cadence.json`, `.claude/drift-check.stamp` - local, gitignored.

## BLOCKED-ON-EVAN
- Review docs/2026-10-17_pitch-corrections.md and give it to the presenters
  (rev2's pitch still says QR, VUMC, PDF, Dad's bills, a database).
- Interview / task-comparison results ([N], [x], [y] in the pitch); V1 is done
  (record AC: 13/13 raise assistance, 0/13 give the window or a letter).
- Project LICENSE (legal call); TLS needs a domain.
- Budget alert: still UNCONFIRMED (the VM is E5.Flex, a paid shape).
- Delete the downloaded Terraform state JSON from Downloads (it holds the SSH key).
- Ask organizers: submission form, repo, video.
- Team roster and who owns which role.
- Any email to VUMC or Dollar For (outward-facing; Evan sends).

## Next actions (PRD F6 gates + F9 amendments)
0. Plan rev 2 adopted with fixes 2026-10-17 ~13:47 (PRD F9; text in
   `docs/2026-10-17_HackTN26_Health_Access_Plan_rev2.txt`). Times: schedule
   file wins (1:00 PM finish, 9:00 PM venue close).
1. DONE: gate 1 (14:22) and the 5:00 PM gate (14:53) - a blurred bill photo
   -> cited result -> Spanish explanation + packet on the OCI server, 11.8 s.
2. DONE 15:40: "Paper Trail" design live (record W, commit c689291).
3. 3:00 PM VUMC gate passed with nobody opening VUMC's PDF: synthetic
   hospital stands unless Evan says otherwise.
4. Submission = teammates' presentation with a LIVE demo of the site (Evan,
   ~15:49). Keep the live URL stable; record a backup video before it.
5. DONE 18:03: T2 V1 chatbot test (record AC). Open:
   T3 real-phone test (Evan, later), budget alert. Done: MySQL/HeatWave
   deleted (record X), axe audit clean (docs/2026-10-17_accessibility-audit.md),
   reviewer screenshots sent (ar, zh-CN, zh-TW).
6. DONE 16:08: the 6 bugs from record X fixed and live (commit 116d631,
   record Y).
7. DONE 16:43: full audit (docs/2026-10-17_full-audit.md, record Z): 5
   highs, mostly claims that outlived the code.
8. DONE 16:55, deployed 16:58 (c4a28f0): every audit fix (record AA) -
   /extract no longer freezes the site; not-eligible works in every language;
   Hindi keeps the hospital name; double-upload race fixed; different-hospital
   warning; rate limit and field caps; uploads in memory; docs corrected.
   Live OCI check from the laptop: es/ar not-eligible explanations and hi/ar
   packets all pass (n=1). Open: pitch sheet review (Evan).

## Handoff prompt

```
Project: TNHacks26 (folder C:\ClaudeCode\TNHacks27). Read in order:
HANDOFF.md, .claude/project-memory/important.md, PRD_ROADMAP.md (CURRENT
DIRECTION fork + F9 amendments), then the record's last 3 appendices and
.claude/project-memory/operations.md (VM details).

State (2026-10-17 17:00 CDT): "Bill to Help" - bill photo -> hospital
financial-assistance packet, explained in 11 languages (tier 1 en/es/ar/
zh-CN/zh-TW). Python FastAPI + plain HTML/JS. LIVE with real OCI at
http://207.211.181.174/ (E5.Flex VM, /opt/bill-to-help, systemd + Apache,
instance-principal auth, no keys on the server). Gate 1 and the 5:00 PM
gate passed (blurred photo -> cited result -> Spanish packet, 11.8 s).
4 test files ALL PASS. SSH: ssh -i C:\Users\daruw\.ssh\HackTN26.pem
opc@207.211.181.174. UI: "Paper Trail" design (policy table with your row
highlighted, footnoted citations; vendored Web Awesome CSS + IBM Plex;
brief in docs/research/2026-10-17_design-system-brief.md). Record is
current through Appendix AA. Audit: docs/2026-10-17_full-audit.md. Pre-mortem: docs/2026-10-17_pre-mortem.md
(T4, T5 done; T8 mostly done - MySQL deleted, budget alert open; T2, T3
open). Translated letters keep the hospital name verbatim (protected like
numbers, Hindi included since the audit fixes) and fall back to English if
it is lost. The audit fixes are live since 16:58 (c4a28f0).

Hard constraints: hacking ends Sun 2026-10-18 1:00 PM CDT (schedule file is
ground truth); venue closes Sat 9:00 PM. Synthetic data only. No diagnosis.
OCI only. $500 credits, $0 beyond. Commit only when asked; push only when
told; no Co-Authored-By lines.

Next, in order: (1) presenters adopt docs/2026-10-17_pitch-corrections.md;
(2) pre-mortem T1/T3/T8 (Evan: organizers, phone test, budget alert); V1
done (record AC); (3) fluent review of es/ar/zh strings
(TODO-REVIEW in app.js); feature freeze ~23:00 Sat.
```
