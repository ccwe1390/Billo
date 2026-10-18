# Handoff

## Goal

**Mission (decided 2026-10-17 ~13:05 CDT; product name is a placeholder):**
[Name] turns a photo of a Nashville hospital bill into that hospital's
financial assistance packet - eligibility estimate against the hospital's own
published policy (every rule cited), pre-filled application fields, document
checklist, deadline and cover letter - explained in 11 languages [2026-10-17 20:13: now 32 languages (all 31 Oracle Translate codes = 29 languages, plus Hindi via Command A; every one with a translated interface, record AI)] (Arabic, Spanish and Chinese with a translated
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

## Current state - LIVE on OCI at http:// and https://207.211.181.174/ (gates 1 and 2 passed)

**Last updated: 2026-10-18 08:52 CDT** - this file is the only live
snapshot; history lives in the record (Phase 0, Appendices A-AV).

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
| Code | Engine (+ full tier table) + FastAPI app + 5-screen "Paper Trail" UI + synthetic policy page + blur test bills + languages (32 codes from app/data/languages.json, dropdown; live since 00:07); 6 test files ALL PASS; live with real OCI since 14:53; the live server runs 5af2f1f (deployed by Evan 2026-10-18 00:07 CDT, record AR; 32 languages live) | record P-W |
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
- Limits (on f10 since record AL): field values are text or numbers only,
  control characters removed, <= 200 chars; 60 paid requests (/extract,
  /explain, /packet) per 60 s per client IP (last X-Forwarded-For entry) AND
  600 paid requests per hour in total; an /extract body over 8 MiB + 64 KiB
  is refused (413) before it is read when Content-Length is declared (a chunked upload
  without it is parsed first; audit 3 finding 17).

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

## STATUS (2026-10-18 08:52 CDT) - read this first
- **LIVE: bdc76df on http AND https://207.211.181.174/** (deployed by Claude 08:48 CDT at Evan's
  request; live checks 08:49 pass; record AV). The demo now uses the REAL published policies of
  Vanderbilt University Medical Center and Ascension Saint Thomas (app/data/policy_vumc.json,
  policy_ascension_saint_thomas.json, page-cited, verified by a fresh agent); every bill stays
  SYNTHETIC. Other hospitals get no estimate. Rollback: `deploy.ps1 -Commit bdc76df -Rollback`
  (restores 984a537).
- Deploy command (any folder): `powershell -ExecutionPolicy Bypass -File
  C:ClaudeCodeTNHacks27deploydeploy.ps1 -Commit <c>`; after a dropped link re-run with
  -Watch (exit 2 = network dropped, remote keeps running). One "curl: (7)" line is normal.
- Presenters: docs/2026-10-17_pitch-corrections.md (08:51 banner) - real policy, synthetic bill,
  NO endorsement; do NOT say "left the blurry date blank" (new render misread it, 08:49). Reprint
  bill-02 (its QR now opens ?hospital=vumc).
- Audit 3 (docs/2026-10-18_audit-3.md, record AS): 4 high / 12 med / 21 low,
  3 policy questions for Evan (A1 number lock is set-based; A2 "nothing is
  stored" vs the Apache access log; A3 sheet). Fixed so far: 1, 2, 3, 4, 8, 11,
  12, 13, 14. The rest is listed in its section 7.
- HTTPS: Let's Encrypt IP certificate (lineage billscan-ip, expires
  2026-10-24 15:39 GMT, NO auto-renewal); certbot 5.8.0 in /opt/certbot;
  Apache conf.d bill-to-help-acme.conf and bill-to-help-ssl.conf; no redirect
  from http (both work).
- Deploys are run by Evan in PowerShell 5.1 (the auto-mode classifier refuses
  Claude's live restarts, record AG): deploy.ps1 -Commit <c>; deploy.ps1
  -Commit <c> -Rollback restores ~/backup-before-<c>.tar. Scripts in deploy/
  (.sh kept LF by .gitattributes). Re-running the same -Commit overwrites its
  backup (audit 3 finding 10, open).
- Git: origin/f10 = 9fd784a, origin/main = 984a537; local f10 and main (= bdc76df) are ahead, not
  pushed (Evan: no push until told).
- Open: Evan's phone checks (photo upload, https padlock, QR scan on bill-02);
  the rollback was not rehearsed live; spikes/synthetic-bill/
  phone-photo-bill-02.png is not a faithful photo (table rows offset; audit 3
  finding 34) - do not use it as phone-test evidence.
- PRD F11 (personal app) is a DRAFT, roadmap only; 23:59 (record AP): F11.7
  push reminders DROPPED; nickname and F11.8 kept; no F11 code.
- Research: docs/research/ (stats, features, sustainability, Middle TN
  policies) + docs/research/2026-10-18_cold-assessments.md. The policies brief
  still has 3 factual errors the assessment found (not corrected).
- Older status lines (19:43 to 00:37) are in the record, Appendices AH-AS.

## BLOCKED-ON-EVAN
- Give docs/2026-10-17_pitch-corrections.md (rewritten 2026-10-18 07:40 to
  match the live app) to the presenters.
- Interview / task-comparison results ([N], [x], [y] in the pitch); V1 is done
  (record AC: 13/13 raise assistance, 0/13 give the window or a letter).
- Project LICENSE (legal call). TLS is DONE (record AH: IP certificate, expires 2026-10-24, no auto-renewal).
- Budget alert: still UNCONFIRMED (the VM is E5.Flex, a paid shape).
- Confirm the Terraform state JSON is deleted (not found in Downloads, depth 2,
  at 00:30; audit 3 finding 36).
- Ask organizers: submission form, repo, video.
- Team roster and who owns which role.
- Any email to VUMC or Dollar For (outward-facing; Evan sends).

## Next actions (PRD F6 gates + F9 amendments)
0. Plan rev 2 adopted with fixes 2026-10-17 ~13:47 (PRD F9; text in
   `docs/2026-10-17_HackTN26_Health_Access_Plan_rev2.txt`). Times: schedule
   file wins (1:00 PM finish, 9:00 PM venue close).
1. DONE: gate 1 (14:22) and the 5:00 PM gate (14:53) - a blurred bill photo
   -> cited result -> Spanish explanation + packet on the OCI server, 9.7 s (gate run; 11.8 s re-run, record Z).
2. DONE 15:40: "Paper Trail" design live (record W, commit c689291).
3. 3:00 PM VUMC gate passed with nobody opening VUMC's PDF: synthetic
   hospital stands unless Evan says otherwise.
4. Submission = teammates' presentation with a LIVE demo of the site (Evan,
   ~15:49). Keep the live URL stable; record a backup video before it.
5. DONE 18:03: T2 V1 chatbot test (record AC). Open:
   T3 real-phone test (Evan, later), budget alert. Done: MySQL/HeatWave
   deleted (record X), axe audit clean on the OLD Paper Trail UI only (c689291; not re-run on the ported UI - audit 2 #20),
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
