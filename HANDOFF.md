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

## Current state - LIVE on OCI at https://207.211.181.174/ (HTTPS only since 2026-10-18 12:31 CDT; http 308-redirects; gates 1 and 2 passed)

**Last updated: 2026-10-18 14:37 CDT** - this file is the only live
snapshot; history lives in the record (Phase 0, Appendices A-BN).

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
| Starter kit stack / VM | Re-apply succeeded 13:15 CDT. VM 207.211.181.174, E5.Flex 1 OCPU (paid), Oracle Linux 9.8, Python 3.12 venv in /opt/bill-to-help, systemd + Apache proxy on :443 (:80 only redirects to https since 2026-10-18 12:31). SSH key at `C:\Users\daruw\.ssh\HackTN26.pem`. Auth to OCI = instance principal. | operations.md |
| Budget alert | **UNCONFIRMED** | - |
| Generative AI access (Command A Vision) | **WORKS FROM CODE** 2026-10-17 14:22: `cohere.command-a-vision`, bill-01 6/6, blur test passed (null at blur 3 and 5), n=1 each - OLD render only (2026-10-17); the re-rendered blur-3 bill misread the date (2026-10-18 08:49, experiments.md); blur 5 not re-run | experiments.md |
| VUMC + Ascension policy | **REAL, VERIFIED** 2026-10-18: read from their PDFs, page-cited, re-checked by a second AI pass and against freshly downloaded PDFs (audit 4: 0 defects); live since 08:48 | record AV, audit 4 |
| Code | Engine (+ full tier table) + FastAPI app + 5-screen "Paper Trail" UI + synthetic policy page + blur test bills + languages (32 codes from app/data/languages.json, dropdown; live since 00:07); 9 test files ALL PASS (2026-10-18 12:45: checks 21, eob_checks 25, dispute 21, app_js 78); live with real OCI since 14:53; the live server runs 2e74b20 (see the LIVE bullet under Status; the e53d1ce text that follows is history) (e53d1ce deployed 2026-10-18 10:20 CDT, record AZ; real policies) | record P-W |
| Old-plan artifacts | Synthea snapshot (`data/synthea/`, gitignored), JDK 17 + Synthea jar in `C:\Users\daruw\tools\` - optional now | record H |

## Architecture (PRD fork F2)
- FastAPI app on the OCI VM, endpoints `/extract`, `/evaluate`, `/explain`,
  `/packet`; stateless.
- OCI Generative AI: Cohere Command A Vision (read bill), Command A (phrase);
  OCI Language (translate). No back-translation: numbers and the hospital
  name are swapped for {n} placeholders, then the number lock checks the
  result (Hindi: Command A with the same placeholders). Policy rules are 3
  JSON files in app/data/ (policy_vumc + policy_ascension_saint_thomas = real, policy_cumberland_synthetic
  = fictional), picked by the bill's hospital name (engine.select_policy); no database
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

## STATUS (2026-10-18 10:22 CDT) - read this first
- **10:02 CDT (record AX):** audit 4 (docs/2026-10-18_audit-4.md) - crit 1 and highs 2-8 fixed (fc21a7d, 8f1a449, a4d2fc1, f6b6f05); open: 9, 11, 13, 15, 16, 24-36, B3.
- **10:22 CDT (records AY, AZ):** landing check FIX FIRST -> fixed (f2c2135, e53d1ce): a bill with no hospital name is listed
  but not counted on Home; Home hides this policy's contact unless the user's bill matches; JS harness fails a run that stops early
  (50 tests). VUMC condition 1 = help is for uninsured/underinsured (FAP p.4, p.6): do NOT tell insured VUMC families "free care".
  Still open from audit 4: #10 global-bucket half, #12 Ascension mailing address.
- **10:29 CDT (record BA):** 223013b committed, NOT deployed: Apply by counts from the date of service when known (feature review
  flaw 2; bill-01 now 2027-05-10). Deploy waits for the optimization + security audits (Evan).
- **14:37 CDT: LIVE = 8cd1d09** (always-clickable "No Explanation of Benefits Available" button + no-summary card/letter, record BN; rollback -Commit 8cd1d09 -Rollback restores df69369). Before: LIVE = df69369 (second QR -> /test-bills/ synthetic test bills page, record BM; rollback -Commit df69369 -Rollback restores 790eb38). Before: LIVE = 790eb38 (audit 5 fixes, record BK; rollback -Commit 790eb38 -Rollback restores 2e74b20; also at https://billow.duckdns.org). Before: LIVE = 2e74b20 (8 swarm UI fixes, record BI; rollback -Commit 2e74b20 -Rollback restores 02e3d18; open: 54 untranslated keys in 26 languages, Hebrew letter "Billing Office"). Before: LIVE = 02e3d18 (same app as 189163e, redeployed at the end of the docs sync; rollback -Commit 02e3d18 -Rollback restores 189163e). Before: LIVE = 189163e (one confirm box per screen, pending wording, dashboard counters; record BH; rollback restores af1d5f6). Before: LIVE = af1d5f6 (Phase 3 review fixes, record BG; rollback -Commit af1d5f6 -Rollback restores deeebda). Presenter kit: https://claude.ai/artifact/MLf6h32yyfNT4o5mXRnBSX (v9). Swarm open items: record BG. Before: LIVE = deeebda (Remove photo + closed Sources dropdown on top of Phase 3; rollback -Commit deeebda -Rollback restores ba6d1f0). Before: LIVE = ba6d1f0 (Phase 3 EOB check merged + deployed 11:42, live checks pass, record BE; rollback -Commit ba6d1f0 -Rollback restores 99d4851; the f13 Opus cold review had not reported at merge). Earlier: LIVE = 99d4851 (Phase 2 "Find errors" + Billow rename, deployed 11:16 by Claude at Evan's word; live checks pass
  on http + https, record BC). Rollback: deploy.ps1 -Commit 99d4851 -Rollback (restores 08265fa). Demo error flags ONLY on
  bills 11-14 (fictional Cumberland). Open O2 items #4-#13 (record BC). Pitch: the DO NOT SAY line is lifted (Phase 2 live by 12:40).
  KEEP until after the pitches (Evan 11:23): worktree C:/ClaudeCode/TNHacks27-f12 and ~/.claude/task-plans/tnhacks26-errorcheck.md.
  Phase 2 files frozen at 79f1c07 for the Phase 3 fork (f13); nothing merges without Evan.
- **[SUPERSEDED 2026-10-18 12:27: LIVE is 2e74b20, https only] Earlier LIVE: e53d1ce on http AND https://207.211.181.174/** (deployed by Claude 10:20 CDT at Evan's
  word; live checks 10:21 pass; record AZ). Real published VUMC + Ascension Saint Thomas policies,
  synthetic bills; audit-4 fixes + landing-check fixes + the VUMC uninsured/underinsured condition
  (record AY) live. Rollback:
  `powershell -ExecutionPolicy Bypass -File C:\ClaudeCode\TNHacks27\deploy\deploy.ps1 -Commit e53d1ce -Rollback` (restores f6b6f05).
- Deploy command (any folder): `powershell -ExecutionPolicy Bypass -File
  C:\ClaudeCode\TNHacks27\deploy\deploy.ps1 -Commit <c>`; after a dropped link re-run with
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
  Apache conf.d bill-to-help-acme.conf and bill-to-help-ssl.conf. HTTPS ONLY since
  2026-10-18 12:31 CDT (record BJ): bill-to-help-https-only.conf sends every http request a 308
  to the same https URL, except /.well-known/acme-challenge/ (renewal needs it on :80).
  Undo: sudo rm /etc/httpd/conf.d/bill-to-help-https-only.conf && sudo apachectl graceful.
- Deploys: Claude ran bdc76df (08:48), f6b6f05 (09:59) and e53d1ce (10:20), each at Evan's explicit request (records AV, AX, AZ); without that say-so,
  or if the auto-mode classifier refuses (record AG), Evan runs it in PowerShell 5.1:
  `powershell -ExecutionPolicy Bypass -File C:\ClaudeCode\TNHacks27\deploy\deploy.ps1 -Commit <c>`; add -Rollback to restore
  ~/backup-before-<c>.tar. Re-running a commit keeps its first backup (e5d5b80); use a new commit
  hash for every fix (audit 4 #15: a reused name can leave a stale backup). .sh kept LF by .gitattributes.
- Git: pushed 2026-10-18 08:54 CDT (origin/f10 = a959f2b, origin/main = bdc76df); later commits are
  local until Evan says push.
- Open: Evan's phone checks (photo upload, https padlock, QR scan on bill-02);
  the rollback was not rehearsed live; spikes/synthetic-bill/
  phone-photo-bill-02.png is not a faithful photo (table rows offset; audit 3
  finding 34) - do not use it as phone-test evidence.
- PRD F11 (personal app) is a DRAFT, roadmap only; 23:59 (record AP): F11.7
  push reminders DROPPED; nickname and F11.8 kept; no F11 code.
- Research: docs/research/ (stats, features, sustainability, Middle TN
  policies) + docs/research/2026-10-18_cold-assessments.md. The policies brief
  has all 5 assessment fixes applied (08:31, 6dd65a1).
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
3. ~~3:00 PM VUMC gate passed with nobody opening VUMC's PDF: synthetic
   hospital stands unless Evan says otherwise.~~ SUPERSEDED 2026-10-18 08:00 (Evan): real VUMC +
   Ascension policies (important.md 7).
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

## Handoff prompt

```
Project: TNHacks26 Billow (C:/ClaudeCode/TNHacks27, branch f10). Read HANDOFF.md first, then the last 3 record
appendices (docs/Project Record - Full Chronological History.md, BE-BJ). Live: 2e74b20, HTTPS only (http redirects), at https://207.211.181.174/
(Phase 1 eligibility + packet, Phase 2 Find errors, Phase 3 EOB check, Remove photo, Sources dropdown). Hacking ended
13:00 CDT 2026-10-18; showcase 13:05, finals 15:30 - do NOT deploy during them. Hard rules: synthetic bills only; never
imply hospital endorsement; deploy only on Evan's word (deploy.ps1 -Commit <c>, rollback -Rollback); commit only when
asked, push only when told; ASCII in .md. Open: swarm findings in record BG (pending-flag wording, dashboard counters,
insured-VUMC caveat, EOB appeal phone read, 640-720 px EOB row, aria-live, 54 untranslated keys). Keep until after
the pitches: worktree C:/ClaudeCode/TNHacks27-f12 and ~/.claude/task-plans/tnhacks26-errorcheck.md.
```
