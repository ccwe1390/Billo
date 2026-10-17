# Project Record - Full Chronological History

Written 2026-10-17. Every entry is grounded in one of:
- Evan's chat messages in the bootstrap session (2026-10-17), including the
  pasted Track 2 text.
- Direct inspection of the project folder on 2026-10-17 (empty at that time).

No git history exists. Sections where a timestamp can't be precisely verified
are explicitly marked. No fabricated metrics, dates, or file names.

---

# How this document is organized

This record has two parts plus this navigation front-matter:

- **Part I - Phases** (`##` headings): the original consolidation, written in
  one pass from real history at bootstrap time.
- **Part II - Appendices A-...** (`#` headings): chronological addenda appended
  one session at a time. **Append-only** - prior appendices are never edited.

The two heading levels encode that distinction (Phases are sections of the
original record; Appendices are top-level addenda). Sub-sections use the
`Letter.Number` convention (e.g. `B.7`, `Q.2`).

The sections below are reading aids. The authoritative detail always lives in
the dated entry, not the digest.

---

# Table of Contents

**Part I - Original record (2026-10-17)**
- [Phase 0 - Bootstrap and track selection](#phase-0---bootstrap-and-track-selection) (10-17)

**Part II - Appendices (chronological)**
- [A - Planning grill - Bill Decoder chosen, OCI mandatory, languages, credits](#appendix-a---planning-grill---bill-decoder-chosen-oci-mandatory-languages-credits-2026-10-17-1030-1055-cdt) (10-17)
- [B - Mission statement and intent set; HANDOFF rewritten](#appendix-b---mission-statement-and-intent-set-handoff-rewritten-2026-10-17-1056-cdt) (10-17)
- [C - Correction - event name is TNHacks26](#appendix-c---correction---event-name-is-tnhacks26-2026-10-17-1057-cdt) (10-17)
- [D - Two-step flow (request itemized bill first); user sends letters, demo-only send](#appendix-d---two-step-flow-request-itemized-bill-first-user-sends-letters-demo-only-send-2026-10-17-1105-cdt) (10-17)
- [E - Website hosted on OCI, OCI Language translates; website profile applied](#appendix-e---website-hosted-on-oci-oci-language-translates-website-profile-applied-2026-10-17-1113-cdt) (10-17)
- [F - Hindi fallback to OCI Generative AI confirmed](#appendix-f---hindi-fallback-to-oci-generative-ai-confirmed-2026-10-17-1114-cdt) (10-17)
- [G - PRD grill (stack, hosting, data, errors) and PRD_ROADMAP.md written](#appendix-g---prd-grill-stack-hosting-data-errors-and-prd_roadmapmd-written-2026-10-17-1130-cdt) (10-17)
- [H - M0.2 done - JDK 17 + Synthea installed; single-thread needed for determinism](#appendix-h---m02-done---jdk-17--synthea-installed-single-thread-needed-for-determinism-2026-10-17-1136-cdt) (10-17)
- [I - Read OCI starter kit README and Hacker Toolkit PDF; Chicago region, Node 16, pitch gap](#appendix-i---read-oci-starter-kit-readme-and-hacker-toolkit-pdf-chicago-region-node-16-pitch-gap-2026-10-17-1145-cdt) (10-17)
- [J - OCI stack created; Node 20.9 fix; research brief - space is crowded, accuracy edge not unique](#appendix-j---oci-stack-created-node-209-fix-research-brief---space-is-crowded-accuracy-edge-not-unique-2026-10-17-1233-cdt) (10-17)
- [K - Option B facts verified; B.A.R.S. already built option B (prize winner)](#appendix-k---option-b-facts-verified-bars-already-built-option-b-prize-winner-2026-10-17-1239-cdt) (10-17)
- [L - Event facts, rubric, and draft pivot plan (bill to financial assistance packet) received](#appendix-l---event-facts-rubric-and-draft-pivot-plan-bill-to-financial-assistance-packet-received-2026-10-17-1256-cdt) (10-17)
- [M - Pivot adopted - bill to financial assistance packet; Python stack; deadline Sun 1:00 PM; PRD forked](#appendix-m---pivot-adopted---bill-to-financial-assistance-packet-python-stack-deadline-sun-100-pm-prd-forked-2026-10-17-1310-cdt) (10-17)
- [N - Starter-kit apply failed (A1 out of capacity); E5 fallback; synthetic test bill](#appendix-n---starter-kit-apply-failed-a1-out-of-capacity-e5-fallback-synthetic-test-bill-2026-10-17-1314-cdt) (10-17)
- [O - Gate 1 passed in Playground; contracts drafted; vision extract spike written (not run)](#appendix-o---gate-1-passed-in-playground-contracts-drafted-vision-extract-spike-written-not-run-2026-10-17-1324-cdt) (10-17)
- [P - Rules engine built and reviewed; revised plan received](#appendix-p---rules-engine-built-and-reviewed-revised-plan-received-2026-10-17-1339-cdt) (10-17)
- [Q - App shell built, reviewed, tamper flaw fixed, pushed](#appendix-q---app-shell-built-reviewed-tamper-flaw-fixed-pushed-2026-10-17-1346-cdt) (10-17)
- [R - Team plan rev 2 adopted with fixes (PRD F9)](#appendix-r---team-plan-rev-2-adopted-with-fixes-prd-f9-2026-10-17-1351-cdt) (10-17)
- [S - Blur test set and synthetic policy page; citations linked](#appendix-s---blur-test-set-and-synthetic-policy-page-citations-linked-2026-10-17-1352-cdt) (10-17)
- [T - Language tiers built and reviewed; null-render bug fixed](#appendix-t---language-tiers-built-and-reviewed-null-render-bug-fixed-2026-10-17-1406-cdt) (10-17)
- [U - Gate 1 passed from code; blur test passed; JSON-fence bug fixed](#appendix-u---gate-1-passed-from-code-blur-test-passed-json-fence-bug-fixed-2026-10-17-1424-cdt) (10-17)
- [V - Deployed to OCI VM; 5 PM gate passed; number-safe translation](#appendix-v---deployed-to-oci-vm-5-pm-gate-passed-number-safe-translation-2026-10-17-1511-cdt) (10-17)
- [W - Paper Trail design built and deployed (GO at 15:40)](#appendix-w---paper-trail-design-built-and-deployed-go-at-1540-2026-10-17-1541-cdt) (10-17)
- [X - MySQL deleted; reviewer screenshots; axe audit; 6 bugs found](#appendix-x---mysql-deleted-reviewer-screenshots-axe-audit-6-bugs-found-2026-10-17-1602-cdt) (10-17)
- [Y - Six reviewer-screenshot bugs fixed and deployed](#appendix-y---six-reviewer-screenshot-bugs-fixed-and-deployed-2026-10-17-1609-cdt) (10-17)
- [Z - Full audit: 5 highs, mostly claims that outlived the code](#appendix-z---full-audit-5-highs-mostly-claims-that-outlived-the-code-2026-10-17-1643-cdt) (10-17)

---

## Phase 0 - Bootstrap and track selection

**2026-10-17, ~10:15-10:30 CDT.**

- The project folder `C:\ClaudeCode\TNHacks27` was empty: no files, no git, no
  `.claude/`. No earlier notes about it exist in the workspace or memory.
- Evan ran `/project-memory`. A first reply from Evan ("Bootstrap now. Brief:")
  arrived with nothing after "Brief:", so nothing was created from it.
- Evan then reported the team chose a hackathon track and pasted its text:
  Track 2, "Health Access, Equity & Experience" (challenge, OCI/Oracle
  opportunity, responsible-innovation rules, success criteria). Summarized in
  `HANDOFF.md`; the binding rules are in
  `.claude/project-memory/important.md`.
- The name "TNHacks27" is inferred from the folder name only.
- The memory system was bootstrapped from that text alone: HANDOFF, this
  record, the full bin set (mostly stubs), and `.claude/pm-cadence.json`.

**HONEST OPEN ITEM (not fixed):** event dates, submission deadline, rules,
team roster, OCI access, and the actual problem to solve are all unknown.
Nothing was invented to fill them.

# Appendix A - Planning grill - Bill Decoder chosen, OCI mandatory, languages, credits (2026-10-17, ~10:30-10:55 CDT)
**WHAT:** First planning grill, plus the decisions that came out of it. All
of them are also in the bins (`.claude/project-memory/`).

- **Module chosen (Evan):** Bill Decoder only. The user gives a bill and an
  EOB; the tool explains each line, flags likely errors, and drafts an appeal
  or itemized-bill request. An AI-generated three-module idea list (Bill
  Decoder, Discharge Companion, Med nudges), pasted by Evan, was narrowed to
  one. Reason: the track says go deep on one problem; this is the only module
  with exact ground truth (we write the synthetic bills and plant the errors)
  and no clinical-risk surface.
- **User and equity angle (Evan's idea, Claude's scoping):** immigrants with
  limited English, plus low-income patients. Committed scope: error and
  duplicate detection, plus a translated explanation. The appeal letter stays
  in English. A financial-assistance check is a stretch goal. No Surprises Act
  and negotiation letters are cut. The tool asks for no immigration status,
  SSN, or ID.
- **OCI is mandatory (Evan).** Candidate services found in Oracle docs:
  Document Understanding (OCR/tables), Generative AI (chat models), and
  Language (translation). Nothing tested yet.
- **Languages (Evan):** aim for the top 10 US immigrant languages; the first
  wave is Spanish, Chinese, and Arabic. Evan proposed Hindi as the fourth. Claude
  pushed back: Hindi is not in the sourced top-6 LEP ranking (MPI/ACS 2010,
  2018) and is not in OCI Language's 31-language list. Vietnamese was offered
  instead (57% limited-English share, supported). OPEN - Evan has not decided.
  Ranks 7-10 are unsourced.
- **Evan's pasted OCI language list** had 29 entries. Oracle's docs page and
  the OCI CLI reference both list 31, including Vietnamese and Slovenian.
  Recorded in languages.md.
- **Money (Evan):** the team has $500 in OCI credits. Evan's personal ceiling
  beyond that is $0. Credit expiry, account owner, and service coverage are
  unknown.

**HOW:** One question at a time, each with a recommended answer. The ranking
and service facts were checked against Census, MPI, and Oracle pages; nothing
came from memory alone. Two of Evan's replies arrived empty after a prefilled
button ("Brief:", "change:"), so nothing was assumed from them.

**HONEST OPEN ITEM (not fixed):** the 6 mission-statement questions
(audience, primary user, fourth language, headline metric, financial
assistance, name) are unanswered, and there is no mission statement yet.
Event dates, rules, and team are still MISSING. The repo is named TNHacks26
while the folder is TNHacks27, so the event name is unresolved.

# Appendix B - Mission statement and intent set; HANDOFF rewritten (2026-10-17, ~10:56 CDT)
**WHAT:** Evan answered the 6 mission questions from Appendix A, and the
mission statement and intent summary were written into `HANDOFF.md` (Goal).
HANDOFF was rewritten to match: state "Planned, not built", event-name
mismatch added, problem-decision blocker removed.

Answers (Evan, 2026-10-17): (1) audience = internal north star first, as
recommended; (2) users include the family member who reads the bill, as
recommended; (3) fourth wave-1 language = Vietnamese, as recommended, with
Hindi kept as an additional option (this is Evan's change to the
recommendation); (4) headline = precision/recall on planted errors, demo
number = dollars flagged, as recommended; (5) financial-assistance check
phrased as an add-on if time allows (Evan's wording; Claude had recommended
leaving it out of the mission); (6) placeholder name, as recommended.

**WHY:** the track asks for one clearly defined problem, user group, and
measurable outcome; these answers fix all three, which unblocks the PRD.

**Process note:** between Appendix A and this entry, the bootstrap commit
`65be0e2` was pushed to `github.com/Evan-Daruwalla/TNHacks26` (private,
`main`) at Evan's request. `.claude/pm-cadence.json` is gitignored because it
is a per-machine prompt counter.

**HONEST OPEN ITEM (not fixed):** event name (TNHacks26 vs TNHacks27), dates,
rules, team, and OCI account details are still MISSING. Hindi output will
have no automatic translation check. Language ranks 7-10 are unsourced.

# Appendix C - Correction - event name is TNHacks26 (2026-10-17, ~10:57 CDT)
**Correction (Evan, 2026-10-17):** the event's real name is **TNHacks26**.
Phase 0, Appendix A, and Appendix B call it "TNHacks27", which was inferred
from the local folder name `C:\ClaudeCode\TNHacks27` and is wrong. Those
entries stay as written (append-only); this entry supersedes them on the name.
The GitHub repo `Evan-Daruwalla/TNHacks26` already had the right name.

**WHAT changed:** the bin headers, the HANDOFF event-name row and blocker list,
and the auto-memory file now say TNHacks26.

**HONEST OPEN ITEM (not fixed):** the local folder is still named
`TNHacks27`, and so is the Claude memory directory keyed to it. Renaming the
folder changes the session's working path and that memory path, so it was not
done mid-session.

# Appendix D - Two-step flow (request itemized bill first); user sends letters, demo-only send (2026-10-17, ~11:05 CDT)
**WHAT:** Evan asked about a feature that "gives you an itemized bill and
allows you to send it to the hospital." Scope was updated in `HANDOFF.md`
(Goal, "What it does") and `decisions.md`.

**Logical flaw flagged, then resolved:** the tool cannot produce an itemized
bill, because only the hospital holds the line-level charges. It can request
one. That splits the product into two steps:
(1) summary bill -> explanation + itemized-bill request letter;
(2) itemized bill + EOB -> line-by-line error flags + appeal letter.
Claude's view is that the duplicate-charge errors the tool hunts for mostly
show up only on itemized bills. That is inferred and unverified; check it on
a sample bill.

**Sending, three options weighed:** A) the user sends the letter (mailto
pre-fill or PDF); B) the app sends it by email through OCI; C) a demo-only
send to a fake hospital inbox the team controls. Evan picked A+C, matching
Claude's recommendation. B was rejected: it would route patient names and
account numbers through our servers (breaking "nothing stored after a
session"), and Claude knows of no public directory of hospital billing
contacts.

**HONEST OPEN ITEM (not fixed):** the demo inbox for C (address, OCI service
or not) is undesigned. That belongs in the PRD.

# Appendix E - Website hosted on OCI, OCI Language translates; website profile applied (2026-10-17, ~11:13 CDT)
**WHAT:** Evan decided that the website is hosted on OCI and that
translation uses OCI. Logged in `decisions.md`, `services.md`, and
`operations.md`, and in HANDOFF (Goal: "Must hold", "Languages").

**Interpretation, stated rather than assumed silently:** OCI Language
translates every language it supports, which covers all of wave 1. Hindi,
which OCI Language lacks, falls back to OCI Generative AI, which is still
OCI. Evan has not confirmed this reading. Consequence for the pipeline:
Generative AI writes the plain-language explanation in English, and OCI
Language translates it, so the back-translation check runs on the same
service.

**Website profile applied:** the project now ships a website, so
project-memory `profiles/website.md` was read and its rows filed. Applicable:
dated wireframes/mockups and a licensed asset inventory in `docs/design/`, a
dated accessibility audit output at demo time, and dated snapshots of any
privacy notice (`ui.md`, `disclosure.md`). N/A: redirect map, maintenance
evidence, consent capture (`operations.md`, `disclosure.md`).

**Correction to Appendix D:** its heading says "~11:05 CDT". The `date` call
made in the same command printed 11:11:05 CDT, so the time was guessed before
the clock was read. Appendix D stays as written (append-only); the true write
time was ~11:11 CDT.

**HONEST OPEN ITEM (not fixed):** the specific OCI hosting service is not
chosen. The Hindi fallback reading is unconfirmed.

# Appendix F - Hindi fallback to OCI Generative AI confirmed (2026-10-17, ~11:14 CDT)
Evan confirmed the Hindi reading from Appendix E: Hindi falls back to OCI
Generative AI. Every other language goes through OCI Language. This closes the
Appendix E open item "Hindi fallback reading is unconfirmed". The choice of
hosting service is still open.

# Appendix G - PRD grill (stack, hosting, data, errors) and PRD_ROADMAP.md written (2026-10-17, ~11:30 CDT)
**WHAT:** PRD grill, four questions, one at a time, each with a recommended
answer. Then `PRD_ROADMAP.md` was written (M0-M7, GOAL block, SCOPE GUARD).
HANDOFF, decisions.md, data.md, dependencies.md, operations.md, and
experiments.md were updated.

| # | Question | Claude recommended | Evan picked |
|---|---|---|---|
| 1 | Stack | A: Python FastAPI + plain HTML/JS | **B: Next.js + OCI TypeScript SDK** |
| 2 | Hosting | A: one OCI Compute VM | **A** |
| 3 | Synthetic bills | A: own TypeScript generator | **B: Synthea + our printer/planter** |
| 4 | Errors to plant | 1-6 core, 7 stretch | **1-6 + 7 stretch** |

**Dissent recorded (Evan's disagreement protocol):** on Q1 Claude favored
Python, for the shortest readable rules engine and eval, fewer moving parts,
and an easier line-by-line explanation in judging. Evan's call stands.

**Fact checks made during the grill:**
- `npm view` shows OCI TypeScript packages for all three services
  (`oci-aidocument`, `oci-generativeaiinference`, `oci-ailanguage`), each at
  2.143.0 on 2026-10-17.
- Synthea's CSV data dictionary shows billing data (`claims_transactions.csv`
  CHARGE/PAYMENT/ADJUSTMENT rows; `claims.csv` OutstandingP). That
  **corrects** Claude's pre-pick claim on Q3 that Synthea is "clinical, not
  billing". Its procedure codes are SNOMED-CT, so a SNOMED -> CPT/HCPCS map
  is needed.
- `java -version` returned "command not found": no JDK is installed, so
  Synthea cannot run yet.

**PRD shape:** riskiest-first. M0 tests OCI access, the budget alert,
Synthea data, and whether Document Understanding can read a bill table,
before any pipeline work. M1-M2 need no OCI calls and can run while M0's
blocked items wait.

**HONEST OPEN ITEM (not fixed):** M0.1 (OCI account + budget alert) and M0.2
(JDK install or Synthea sample download) are BLOCKED-ON-EVAN. The demo-only
send design (M6.2) is open. Per-task commits are not authorized in the PRD;
commits stay on request. Unverified: Always Free VM coverage, instance
principals for the AI services, the public MUE table, CPT descriptor
licensing.

# Appendix H - M0.2 done - JDK 17 + Synthea installed; single-thread needed for determinism (2026-10-17, ~11:36 CDT)
**WHAT:** PRD M0.2 is done. Evan approved downloading two files into
`C:\Users\daruw\tools\`:
- Eclipse Temurin JDK 17.0.20.1+1, Windows x64 ZIP from
  github.com/adoptium/temurin17-binaries. 190,817,615 bytes; the sha256
  e53a79c3...affc7cb0 matched Adoptium's API checksum. Extracted portably
  (no installer, no PATH change). `java -version` prints Temurin-17.0.20.1+1.
- `synthea-with-dependencies.jar` from Synthea's `master-branch-latest`
  release (published 2026-08-18). 197,025,542 bytes, matching the GitHub API
  size. No upstream checksum exists; our sha256 is 018ad7f0...fae224ac.

Synthea's README requires JDK 17 or newer and recommends LTS 17 or 25.

**Run:** 10 patients, `-s 42 -cs 42 -r 20261017`, CSV only. Exit 0, about
21 s. Output: 11 patients (10 alive + 1 dead), claims_transactions 7400 rows
(CHARGE 2242, PAYMENT 2906, TRANSFERIN 1126, TRANSFEROUT 1126), claims 686,
encounters 515, payers 10, procedures 1386.

**Bug found (symptom -> root cause -> fix):** two runs with identical seeds
produced different file hashes on every CSV. After sorting rows, 16 of 18
files matched, but `claims_transactions.csv` (9798 differing lines,
including different IDs) and `payers.csv` (different revenue totals, e.g.
Humana 274284.00 vs 274968.00) still differed. Root cause (inferred,
unverified): Synthea's default multithreading makes ordering and shared
payer state depend on thread timing. Fix: `--generate.thread_pool_size=1`.
Two runs with it were byte-identical on every CSV. That run is the canonical
snapshot `data/synthea/s42-p10-r20261017-t1/`; per-file hashes are in the
`.sha256` beside it. The other test runs (made this session) were deleted.
`data/synthea/` is gitignored.

**Finding that affects M1.3:** the snapshot has zero rows with a nonzero
ADJUSTMENTS amount. Synthea provides no contractual adjustments, so error
type 3 needs adjustments we generate. That design is open.

**HONEST OPEN ITEM (not fixed):** the jar comes from a moving release tag, so
a re-download may differ; keep the hashed copy. The adjustment design for
error 3 is undecided. M0.1 (OCI access, budget alert) is still
BLOCKED-ON-EVAN.

# Appendix I - Read OCI starter kit README and Hacker Toolkit PDF; Chicago region, Node 16, pitch gap (2026-10-17, ~11:45 CDT)
**WHAT:** Evan shared two sources, and both were read.

1. **OCI hackathon starter kit README** (github.com/ScottStroz/oci-hackathon-starterkit,
   third-party, not confirmed as TNHacks26-official). Facts filed in
   `important.md` entry 6, `services.md`, `budget.md`, and the PRD gotchas:
   - The home region must be US Midwest (Chicago) and is permanent.
   - Sign up with the promo-credit email.
   - The kit's VM ships Node 16, too old for Next.js, so a current Node LTS
     goes on in M6.1.
   - The default E5.Flex shape is paid.
   - The Free Trial Generative AI model is cohere.command-a-03-2025, and Grok
     is not available.
   - Auth is through an API signing key in `~/.oci/config`.
   - Per its FAQ, paid usage bills only after an explicit account upgrade.
2. **"The Hacker Toolkit" PDF** (Hackathons International, (c) 2020, 13
   pages). It is a set of worksheet templates: Hacker Mindset, Rapid
   Ideation, Hacker's Canvas, Business Model CPR, and Pitch Like A Pro. The
   Read tool failed (pdftoppm not installed), so the text was pulled with a
   zero-dependency Node script that decodes each font's ToUnicode map. The
   example pages yielded only their labels; their filled-in content is
   likely images and was not read. No event-specific facts are in it.

**Gap Claude flagged:** the toolkit's pitch structure covers persona,
problem, purpose, customer benefits, competitive landscape, core team,
revenue streams, and roadmap. Our docs cover none of competitive landscape,
revenue/scale path, or a concrete persona. The track also lists "credible
path to scale" as a success criterion. Claude offered a pitch-prep PRD
milestone; **Evan chose to skip it for now** (chat 2026-10-17).

**HONEST OPEN ITEM (not fixed):** no pitch prep is planned. The billing
behavior is per a third-party README and unverified with Oracle.

# Appendix J - OCI stack created; Node 20.9 fix; research brief - space is crowded, accuracy edge not unique (2026-10-17, ~12:33 CDT)
**WHAT:**

1. **OCI setup (Evan, in the console).** The OCI account exists. Evan created
   the Resource Manager stack `HackTN26-starterkit` from the starter kit,
   configured as Claude advised after reading the kit's Terraform via gh api:
   - shape VM.Standard.A1.Flex, 2 OCPU / 12 GB;
   - Databases = MySQL HeatWave only (Always Free default);
   - tag `project=HackTN26`.

   Its apply job was still running at the time of this entry. Facts are in
   `services.md`: the image is chosen by shape; the installer is cloud-init
   with no set -e; the installer pins `dev.mysql.com` in /etc/hosts. Whether
   the budget alert was set before apply is NOT confirmed.
2. **Corrections and gotchas.**
   - Next.js needs Node >= 20.9 (context7 Next.js docs). This replaces the
     earlier guess of "18.18+" in `services.md` and the PRD.
   - `gotchas.md`: PowerShell 5.1 key permissions via icacls; VM commands run
     inside SSH. The key file is to be saved as
     `C:\Users\daruw\.ssh\HackTN26.pem` (Evan named it).
   - Claude's slip: it first gave the icacls step before the key existed.
3. **Research brief** `docs/research/2026-10-17_bill-decoder-crowding.md`
   (Evan ran /research-brief).
   - Method: hypotheses fixed first; 3 parallel agents; Claude re-read the
     load-bearing pages in a browser; a fresh-agent cold assessment; one
     extra collection round.
   - Result: very crowded. Commercial: Mediloop already checks bills against
     the EOB for our error types. About 51 core Devpost projects were seen by
     one search route.
   - Overlapping competitors: MedVoice (8 languages incl. zh/vi/ar), Footnote
     (bill + EOB, 30 languages), and **GiveMeMyMoneyBack** (OwlHacks 2026:
     bill vs EOB; "code decides, AI explains"; number-validated Spanish; and
     "caught 19 / 19 planted errors, 0 false alarms").
   - **The cold assessment flipped the brief's own recommendation.** Our
     "measured accuracy" edge is not unique. What remains: end-to-end
     photo->OCI->rules accuracy per error type, plus integrity-checked
     translation in 5 languages including RTL.
   - The "80% of bills have errors" figure traces to an advocacy firm's
     founder: do not use it.
   - Revised options: A' keep and pitch the narrow delta; B re-center on
     financial assistance for LEP patients; C pivot.
   - Design lesson for the PRD: errors planted by the same team that wrote
     the rules pass by construction, so add an independent edge-case set.

**HONEST OPEN ITEM (not fixed):**
- The direction decision (A'/B/C) is Evan's and pending; the PRD is
  unchanged until then.
- The event rubric is MISSING, so any pitch strategy is an assumption.
- The deploy job outcome, VM IP, and budget alert status are unconfirmed.
- Cadence: two PM-CADENCE record-entry reminders (prompts #49, #52) were
  served by this single entry, written after the research finished.

# Appendix K - Option B facts verified; B.A.R.S. already built option B (prize winner) (2026-10-17, ~12:39 CDT)
**WHAT:** Evan asked Claude to verify the unverified facts behind option B
(re-center on charity care for LEP patients). Claude read each source's own
page text. The full table is in the addendum of
`docs/research/2026-10-17_bill-decoder-crowding.md`.

- **Verified verbatim:**
  - IRS 501(r): a written FAP is required for tax-exempt hospitals; web
    publication and a notice on billing statements are required; the LEP
    translation threshold is "the lesser of 1,000 individuals or 5
    percent".
  - CMS: "Nonprofit hospitals must give financial assistance"; "pause
    collections".
  - AJMC 2026: 213 hospitals (61.0%) offered a posted FAP in a non-English
    language.
  - Washington 2017: 28% of Spanish calls got no information vs 90% for
    English.
- **Corrected:** California's 400% FPL is eligibility to apply for "discount
  payment or charity care", and only if uninsured OR high medical costs. It
  is not a flat charity-care cutoff, as Claude had phrased it.
- **Agent error caught:** the hackathon agent reported B.A.R.S. as "languages:
  none stated". Its page says the screening is "in their preferred
  language".
- **Decisive:** B.A.R.S. (hackUMBC 2026, Second Overall winner) already
  builds option B, including extracting hospital policy rules from published
  PDFs with page citations. That falsifies Claude's previous-message claim
  that policy extraction was "unclaimed". That claim came from a search that
  never looked for it. Claude had marked it unverified, but still
  recommended B on it.

**WHY it matters:** both remaining directions (A' and B) now have
prize-winning or near-identical hackathon precedents. Novelty cannot be the
pitch; execution and measured results have to be.

**HONEST OPEN ITEM (not fixed):** the direction decision is still Evan's. The
Tennessee FAP sample was not done.

# Appendix L - Event facts, rubric, and draft pivot plan (bill to financial assistance packet) received (2026-10-17, ~12:56 CDT)
**WHAT:** Evan supplied the event facts and a draft plan (marked "not
final").

- **Deadline:** Evan says "tomorrow at 1:30 PM local". The draft plan says
  hacking ends Sunday 2026-10-18 at 12:00 pm, with 4-minute presentations
  (2 min pitch + 2 min demo) during a 1-5 pm showcase. A Humanitix listing
  (search result, not opened) says the event runs Sat 9am - Sun 5pm CDT.
  **Conflict unresolved: 12:00 pm vs 1:30 pm.**
- **Rubric:** `docs/rubric.txt` (Evan) lists Communication, Social Impact,
  Credibility, Problem Validation ("Have real customers provided input?"),
  User Experience, and "Does the prototype actually work and leverage Oracle
  Cloud Infrastructure capabilities?". No weights.
- **Challenge text:** `docs/#2 Health Access, Equity + Experience.txt`.
- **Draft plan ("HackTN26 Health Access Plan", Oct 17, 2026):** pivots to
  "bill to help". A photo of a Nashville (VUMC) bill becomes a pre-filled
  financial assistance packet, checked against the hospital's published
  policy with citations and explained in Arabic or Spanish for the family
  reader.
  - Architecture: Cohere Command A Vision reads; a deterministic Python
    rules engine decides; Command A phrases; OCI Language checks
    translation; MySQL HeatWave holds the policy registry.
  - Validation: a general-AI test, attendee interviews, and a timed task
    comparison.
  - Gate: VUMC thresholds confirmed from VUMC's own PDF by 3 pm, else a
    labeled synthetic hospital.
- **Checks Claude ran on the plan's facts (search summaries,
  CLOSE-PARAPHRASE at best):**
  - 2026 HHS poverty guidelines: $15,960 for 1 person, $33,000 for 4, +$5,680
    per person (ASPE via search).
  - Cohere Command A Vision is listed on-demand in US Midwest (Chicago) on
    Oracle's models-by-region page (via search). Availability on the Free
    Trial is untested.

**HONEST OPEN ITEM (not fixed):**
- Deadline conflict.
- Stack conflict: the plan says Python; PRD decision 2026-10-17 says
  Next.js.
- The plan omits B.A.R.S. (Appendix K) as prior art.
- PRD and HANDOFF still describe the Bill Decoder; no fork until Evan calls
  the plan final.

# Appendix M - Pivot adopted - bill to financial assistance packet; Python stack; deadline Sun 1:00 PM; PRD forked (2026-10-17, ~13:10 CDT)
**WHAT:** Evan adopted the draft "HackTN26 Health Access Plan" (record Appendix L) with two changes: the stack is Python (FastAPI) + plain HTML/JS on the OCI VM, replacing the morning Next.js decision because of the 24-hour clock, the kit VM shipping Node 16 against Next.js needing >= 20.9, and the kit and console samples being Python; and the deadline comes from `docs/Hackathon Schedule.txt`: hacking finishes Sun 2026-10-18 1:00 PM CDT, the venue closes Sat 9:00 PM.

- `PRD_ROADMAP.md` forked: a SUPERSEDED banner on the Bill Decoder plan, plus a new "CURRENT DIRECTION (forked 2026-10-17)" section (F1-F8) carrying the product, architecture, data, acceptance criteria, validation, schedule gates, failure modes, and open items. B.A.R.S. is added as prior art to name honestly in judge Q&A (the draft plan omitted it).
- HANDOFF rewritten for the new mission. This also fixes a garbled path (`C:Usersdaruw<TAB>ools`) that an earlier node edit produced from unescaped backslashes.
- Bins: decisions.md (stack), timeline.md (agenda), and important.md entry 3, updated in place to the real deadline with the original kept under it.

**HONEST OPEN ITEM (not fixed):** Generative AI access is untested, VUMC thresholds are unverified, and the starter-kit result, VM IP, budget alert, team roster, and submission requirements are all unknown.

# Appendix N - Starter-kit apply failed (A1 out of capacity); E5 fallback; synthetic test bill (2026-10-17, ~13:14 CDT)
**WHAT:**

- **Starter-kit apply failed.** Job ormjob20261017165954 failed at 17:27:34 UTC (12:27 CDT) with "Out of host capacity" for VM.Standard.A1.Flex (2 OCPU/12 GB) in US-CHICAGO-1-AD-1. Already created and kept in state: the network, MySQL DB system "Hackathon MySQL HeatWave" (MySQL.8, 50 GB), and a HeatWave.32GB cluster. Whether these are Always Free is UNVERIFIED.
- **Fallback chosen (planned):** edit the stack to VM.Standard.E5.Flex 1 OCPU / 4 GB (paid, uses credits) and re-apply. Evan could not find "Edit" on the stack page; Claude pointed to the Variables tab or a top-right Actions menu. Result: pending. The details are in `operations.md`.
- **Synthetic test bill made:** `spikes/synthetic-bill/bill-01.html` and its PNG, rendered by headless Edge. Fictional "Cumberland General Hospital (SYNTHETIC)", watermarked; line items sum to $4,812.40 (checked). It is for the first Command A Vision Playground call (gate ~1:45 PM).
- `docs/The_Hacker_Toolkit_TEMPLATE_AND_EXAMPLES_ONLY.pdf` is gitignored: it is a copyrighted 4.7 MB worksheet set, not needed in the repo.

**HONEST OPEN ITEM (not fixed):** no VM yet; the Generative AI call is untested; the budget alert is unconfirmed.

# Appendix O - Gate 1 passed in Playground; contracts drafted; vision extract spike written (not run) (2026-10-17, ~13:24 CDT)
**WHAT:**

- **Gate 1 passed** (~13:17 CDT, n=1). In the OCI Playground, Cohere Command A Vision read `spikes/synthetic-bill/bill-01.png` with all 6 fields correct, in strict JSON (experiments.md).
- **Contracts drafted:** `docs/contracts.md` for team agreement - money in integer cents, dates as YYYY-MM-DD, eligibility comparing cents rather than rounded percents, a locked-numbers list.
- **Playground "View code" is text-only:** Evan pasted it; it uses the v1 CohereChatRequest with no image. Claude checked the oracle/oci-python-sdk source (gh api) for the vision request classes - CohereChatRequestV2, CohereUserMessageV2, CohereTextContentV2, CohereImageContentV2, CohereImageUrlV2, CohereResponseJsonFormat; api_format COHEREV2; response at chat_response.message.content - and wrote `spikes/extract/extract_bill.py`.

**HONEST OPEN ITEM (not fixed):**
- `extract_bill.py` has NOT been run: no Python on this laptop, and no VM yet. Whether OCI accepts a base64 data URI for the image is unverified.
- The model ID was not shown ("---" in the pasted code).
- The E5 re-apply result is unknown.

# Appendix P - Rules engine built and reviewed; revised plan received (2026-10-17 13:39 CDT)
**What happened:** First code. Under the plan-split rule, two Sonnet agents
were dispatched at ~13:35 CDT on disjoint files (plan in
`~/.claude/task-plans/tnhacks26-build.md`). Agent A built the rules engine:
`app/engine.py`, `app/data/fpl_2026.json`,
`app/data/policy_cumberland_synthetic.json`, `tests/test_engine.py`. Agent B
(FastAPI app, OCI client with FAKE_OCI mode, number lock, static screens) was
still running at the time of this entry.

**Review (Opus re-ran the check, did not trust the report):**
`py tests/test_engine.py` -> ALL PASS, exit 0 (13:36 CDT). The tests cover FPL
sizes 1/4/8, the five size-4 tier boundaries (6,600,000 cents = exactly 200%
stays free care; 6,600,100 drops to 75%), the demo case (115%, free care),
deadline 2026-10-01 -> 2027-05-29, the tax-return document rule, and refusal
of unconfirmed fields.

**Change made in review:** `locked_numbers` lacked the discount percent and
the 240-day window, which appear in the tier label and deadline text. Any
generated explanation repeating them would have been flagged and replaced by
the English template. Added both, plus `tier.discount_percent`. Tests re-run:
ALL PASS. `docs/contracts.md` example updated (still a draft, no version
bump). Agent B told: dates in generated text as YYYY-MM-DD, no phone numbers
or emails through the model.

**Also on 2026-10-17 ~13:38 CDT:** Evan pasted a revised plan with mentor
additions (home "Dad's bills", reminders, partner dashboard, QR entry, pitch,
demo script). Not adopted yet; review of conflicts given in chat.

**Status:** engine done and verified on synthetic policy only. Nothing
committed. OCI extraction still not run from code (waiting on Evan's API key
config and model ID).

# Appendix Q - App shell built, reviewed, tamper flaw fixed, pushed (2026-10-17 13:46 CDT)
**What happened:** Agent B finished the app shell: `app/main.py` (FastAPI,
/extract /evaluate /explain /packet, stateless), `app/oci_client.py`
(Command A Vision, Command A, OCI Language; FAKE_OCI=1 mode),
`app/numlock.py`, `app/static/` (five screens, en/es/ar, RTL), tests.

**Review (Opus re-ran checks):** `py tests/test_engine.py`,
`tests/test_numlock.py`, `tests/test_api.py` all printed ALL PASS; a
FAKE_OCI uvicorn server returned 200 for GET / and normalized bill-01 on
POST /extract; `node --check app/static/app.js` OK.

**Flaw found and fixed:** /explain and /packet used the engine result sent
back by the browser. A test request with $999,000 income and a hand-written
"10%, free care" result got a free-care packet. Both endpoints now recompute
the result with the engine; the client's result is ignored. Regression test
added. Lesson: in a stateless design, anything the client echoes back must
be recomputed, not trusted.

**Accepted from the agent:** confidence is null when the model gives none
(no invented scores); not-eligible gets the payment-plan contact, no packet;
model failure or number mismatch falls back to English.

**Still open:** OCI Language translate never run live; the Tennessee
uninsured-protections card has no sourced text (placeholder); es/ar UI
strings need a human reviewer; live OCI needs Evan's API key config and
model ID.

**Correction:** the decisions.md and contracts.md notes for this review were
first stamped "~13:55 CDT", a guessed time; `date` showed 13:45. Fixed to
~13:44.

**Commits:** 69755ed (engine, contracts, spike, docs) and 11d7aaf (app
shell), pushed to origin main at 13:45 CDT on Evan's "push".

# Appendix R - Team plan rev 2 adopted with fixes (PRD F9) (2026-10-17 13:51 CDT)
**What happened:** Evan pasted rev 2 of the team plan (mentor additions:
home "Dad's bills", reminders, partner dashboard, QR entry, pitch, demo
script, judge answers). Claude listed seven issues; Evan ruled
"docs/Hackathon Schedule.txt is ground truth; adopt with fixes".

**Recorded:** rev 2 text saved verbatim at
`docs/2026-10-17_HackTN26_Health_Access_Plan_rev2.txt` (with a header saying
PRD F9 wins on conflict). PRD amended by appending F9 (not a fork: same
product). important.md entry 3 notes the ruling on times.

**Issues and their resolution (detail in PRD F9):**
1. Times: rev 2 said 12:00 PM finish / 8 PM close; schedule file says
   1:00 PM / 9:00 PM. Schedule wins (Evan).
2. "Nothing stored" vs "Save to Dad's bills": opt-in saves stay in the
   phone's browser storage; server stays stateless; wording fixed.
3. "The hospital prints a code" (false today) -> "would print".
4. "$X could be reduced" vs the plan's own no-dollars rule: kept, but
   engine-computed, number-locked, labeled.
5. "Left the blurry date blank" is untested -> bill-02 blur set to test it.
6. Cited page must open on the synthetic branch -> synthetic policy page.
7. Five bills + dashboard -> home page after the 5 PM gate; dashboard as a
   slide mockup.

**Next:** Agent C (Sonnet) dispatched ~13:50 CDT for bill-02 + blur PNGs +
`app/static/policy-cumberland.html`. Live OCI still blocked on Evan's API key
config and model ID.

# Appendix S - Blur test set and synthetic policy page; citations linked (2026-10-17 13:52 CDT)
**What happened:** Agent C (Sonnet) built the blur test set and the
synthetic policy page per PRD F9.
- `spikes/synthetic-bill/bill-02.html` + `bill-02-blur{0,1.5,3,5}.png`: date
  of service printed once; only that value is blurred (CSS filter via URL
  hash). The statement date (10/05/2026) and due date (11/04/2026) sit right
  next to it, so a guessing model will likely copy one of them.
- `app/static/policy-cumberland.html`: labeled SYNTHETIC, `#page-1` tiers,
  `#page-2` window/documents/contacts, values copied from the policy JSON.
- `tests/test_policy_page.py`.

**Review (Opus):** `py tests/test_policy_page.py` -> ALL PASS. Opened
blur3.png: date unreadable, rest sharp (agent: legible at 0, barely at 1.5,
unreadable at 3 and 5). Page has no script and no external links.

**Wired by Opus:** the 9 citation `url` fields in
`app/data/policy_cumberland_synthetic.json` now point at
`/policy-cumberland.html#page-1` / `#page-2`; `cite()` in
`app/static/app.js` renders a link when a url exists. All 4 test files
ALL PASS; `node --check` OK; fake-mode server returned 200 for the page.

**Not done:** the blur set has NOT been run against Command A Vision
(blocked on Evan's `~/.oci/config` + model ID). Pass condition for the 0:14
demo line: `date_of_service` null at blur 3 and 5.

**Correction to Appendix R:** its heading says 13:51 CDT; `date` showed
13:49 when it was written, and Agent C was dispatched ~13:48, not ~13:50.
Both were guessed instead of read. Appendix R stays as written.

# Appendix T - Language tiers built and reviewed; null-render bug fixed (2026-10-17 14:06 CDT)
**What happened:** Language tiers built (Agent D, Sonnet; spec changed
twice mid-run by Evan's decisions).
- Tier 1, translated interface: en, es, ar, zh-CN, zh-TW.
- Tier 2, explanation and cover letter only, English interface: vi, fr, ko,
  ru, de, hi. Hindi's letter uses Command A (`translate_genai_many`)
  because OCI Language has no Hindi; the packet marks it
  `back_checked: false`.
- Every non-English explanation carries a note: written by AI from the
  English facts, numbers checked automatically, the English counts.
- `numlock` normalizes Devanagari digits. `/explain` returns `ai_written`.
- Gap: Tagalog (#3 on Evan's US list) - neither OCI Language nor Command A
  supports it (vendor pages read 2026-10-17; languages.md).

**Review (Opus):** all 4 test files ALL PASS, `node --check` OK, Python
diff read. Browser run (fake mode) through Simplified Chinese, Korean and
Arabic.

**Bug found in the browser, not by tests:** the result screen showed the
word "null" twice. Symptom -> two stray "null" lines. Root cause ->
`Element.replaceChildren()` renders a null argument as the text "null";
the `el()` helper skips nulls but the six `replaceChildren` callers did
not. This predates the language work (any null slot, e.g. the toggle for
English users). Fix -> one `fill()` helper that filters nulls; all six
callers use it; `tests/test_api.py` asserts `.replaceChildren(` appears
only inside `fill()`. Re-run in the browser: no "null" for zh-CN or ko;
Arabic still `dir=rtl`.

**Also:** added Spanish and Arabic text for the AI note (marked
TODO-REVIEW like all es/ar/zh strings). `.claude/launch.json` added to run
the fake-mode server in the browser pane.

**Not verified:** real OCI paths for every new language; the
number-format risk (machine translation may write "4.812,40") is untested.

# Appendix U - Gate 1 passed from code; blur test passed; JSON-fence bug fixed (2026-10-17 14:24 CDT)
**What happened:** Gate 1 passed from code at 14:22 CDT (due ~1:45 PM).
- Evan created the API key and `~/.oci/config`. Two naming slips blocked
  the SDK (`config.txt`; key saved without `.pem`); Claude renamed both and
  validated the config, printing only the region.
- `GenerativeAiClient.list_models` (Chicago) listed 75 models;
  `cohere.command-a-vision` is ACTIVE with CHAT capability.
- Live extraction through the app's own code path
  (`oci_client.extract_bill` + `main.normalize_bill`), temperature 0, n=1
  per image:

| Image | date_of_service | Other fields | Time |
|---|---|---|---|
| bill-01 | 2026-09-12 (correct) | 6/6 correct | 3.9 s |
| bill-02 blur 0 | 2026-09-20 (correct) | correct* | 3.5 s |
| bill-02 blur 1.5 | 2026-09-20 (correct) | correct* | 3.5 s |
| bill-02 blur 3 | null (no guess) | correct | 3.3 s |
| bill-02 blur 5 | null (no guess) | correct* | 3.2 s |

*hospital name returned without "(SYNTHETIC)" on 3 of 4 bill-02 runs.

**Bug found by the live run:** Command A Vision wrapped its JSON in a
json fence even with CohereResponseJsonFormat. Symptom: the spike
printed "NOT valid JSON". Root cause: `json.loads` on fenced text; the app
used the same call, so every real /extract would have returned 502 - the
fake mode could never show this. Fix: `oci_client.parse_json_object`
falls back to the outermost {...}; regression test in tests/test_api.py.
All 4 test files ALL PASS.

**Meaning for the demo:** the 0:14 line "it left the blurry date blank
instead of guessing" is supported (n=1 per level, clean rendered PNGs, not
phone photos - say so if asked).

**Still blocked:** VM deploy needs the stack's public IP and SSH key from
Evan. Not yet run live: Command A phrasing, OCI Language translation.

# Appendix V - Deployed to OCI VM; 5 PM gate passed; number-safe translation (2026-10-17 15:11 CDT)
**What happened:** Deployed to the OCI VM and passed the 5:00 PM gate at
14:53 CDT (about 2 h early).

**Deploy (14:35-14:42):** the stack output `ssh_private_key` is marked
sensitive (console shows a lock), so Evan downloaded the job's Terraform
state and Claude extracted only the key to
`C:\Users\daruw\.ssh\HackTN26.pem` (icacls-locked; fingerprint
SHA256:QA3BKoVf7B7Ub+BRjZ2U5/P9fi44/2Bc6uSMPcEfhp4). VM: opc, Oracle Linux
9.8, x86_64 E5.Flex 1 OCPU (paid), Python 3.9 stock -> python3.12 installed.
App in /opt/bill-to-help (SELinux blocks services running from home
dirs), systemd uvicorn on 127.0.0.1:8000 with --no-access-log, existing
Apache on :80 as reverse proxy. Fake mode first: / 200, /extract 200.

**Auth decision (Evan: option A):** instance principal instead of copying
Evan's API key - no credentials on the server, least privilege, nothing to
rotate. Dynamic group bill-to-help-vm + policy with `use
generative-ai-family` and `use ai-service-language-family`; `use` proved
enough. Code: `OCI_AUTH=instance_principal` -> `oci_client._auth()`
(cached signer).

**Gate run on the server (real AI, n=1):**

| Step | Result | Time |
|---|---|---|
| /extract (bill-02 blur 3) | date_of_service null; others correct | 4.1 s |
| /evaluate | 115%, free care, deadline 2027-06-02, cites p.1 | 0.1 s |
| /explain es | Command A text passed the number check | 4.4 s |
| /packet es | FAILED number check -> English-only fallback | 1.1 s |

**Bug -> root cause -> fix:** OCI Language localized "$4,812.40" to
"$4.812,40" (predicted in languages.md at ~14:00). Placeholder test across
8 languages: `{n}` survived all; `[[n]]`, `<n>`, `#n#` broke in some.
Fix: `protect_numbers`/`restore_numbers` around OCI Language; a lost
placeholder fails the number check (fails closed). Live re-run: es, fr, de,
ru, ar, zh-CN, ko, vi packets all `numbers_match: true`; server journey
11.8 s with the Spanish packet passing. Tests ALL PASS (4 files).

**Not verified:** zh-TW and hi packets live; phone photos (all tests used
rendered PNGs). The server runs the working tree, not a commit.

**Slips:** HANDOFF path lost its backslashes again via a node script
(fixed with the Edit tool); one HANDOFF stamp said 14:56 vs real 14:55
(fixed).

**Correction to Appendix U (made with Evan's explicit OK, 2026-10-17
~15:08 CDT):** Appendix U line 682 began with three backticks ("```json
fence ..."), which opened a Markdown code block that never closed. The
append script skips fenced lines, so it could not see any later heading
and refused this entry ("TOC lines (22) != appendix headings (21)", file
not modified); GitHub also rendered the end of U as code. The fix (Evan, by
hand, ~15:10 CDT) removed the three backticks, so the line now starts
"json fence even with CohereResponseJsonFormat."; no other character in the
record changed (git diff: 1 line). This breaks the append-only rule once,
because a correction appended after U would itself have been inside the
open code block. The record-guard hook blocked Claude from making the edit
directly, so Evan made the one-line edit himself in his editor. Lesson: no
line in an entry body may start with three backticks.

**Also since:** pre-mortem written (docs/2026-10-17_pre-mortem.md, 18
risks, 5 launch-blocking); placeholder Tennessee card removed (145c8af)
and redeployed from the commit at 15:06 CDT.

# Appendix W - Paper Trail design built and deployed (GO at 15:40) (2026-10-17 15:41 CDT)
**What happened:** The "Paper Trail" design (docs/research/2026-10-17_design-
system-brief.md, Direction 1) was built, reviewed and deployed in about 20
minutes of wall clock (15:22-15:40 CDT), far ahead of the 21:00 go/no-go.
Evan chose option A and approved the asset downloads.

**Steps and commits (all pushed):**

| Commit | What | Who |
|---|---|---|
| eb520a9 | Finished brief: cold assessment overturned "Plex is distinctive" (it is an AI-prompt default); CJK uses system fonts | research agent |
| c2ed698 | Engine returns the full tier table (`tiers`, `current` by position); contracts.md; 11 hard UI rules in ui.md (adapted from Dipayan's frontend/CLAUDE.md) | Agent E (Sonnet) + Opus |
| 35bfe4d | Vendored assets: Web Awesome 3.14.0 CSS, IBM Plex (Latin/Viet/Cyrillic, Arabic, Devanagari), 6 Phosphor icons; fonts.css maps 12 faces to 'BillPlex'; license inventory | Opus |
| c689291 | Restyle: answer-first Result, policy table with your row highlighted, footnotes, step bar, named loading steps, "estimate / hospital decides" line, not-affiliated footer | Agent F (Sonnet) + Opus fixes |

**Bug caught in review:** the brief said Web Awesome needs 7 CSS files.
Following the @import graph found 13 (color/variants.css and 5 variant
files). With 7, every page load would 404. All 13 were hash-verified.

**Opus review fixes on Agent F's work:** removed the now-dead cite();
added the Result-screen line "This is an estimate. The hospital makes the
final decision." (ui.md rule 1 was unmet - also missing before the
restyle).

**Verification:**
- Asset download: 36 files, every sha256 and size matched jsDelivr's
  listing.
- 4 test files ALL PASS. The four API calls are byte-identical to before.
- Browser (fake mode): en/ar/zh-CN/zh-TW at 375px and en/ar/zh-CN at 320px.
  No horizontal scroll on any of the 5 screens; exactly one aria-current
  row; no "null"; nothing under 44px; 0 off-site requests; 0 console
  errors; the packet iframe loads; Arabic mirrors correctly.
- Live: deployed from c689291; assets 200; real-AI journey 11.4 s with the
  Spanish packet passing the number check.

**Not done / open:** no axe or Lighthouse audit (neither installed - the
brief's done-check wants one saved); no real-phone check (pre-mortem T3);
Traditional Chinese labels render in a lighter system
face; Devanagari and Arabic fonts load for every visitor because the
language buttons show those scripts (~120 KB); all new es/ar/zh strings are
AI drafts (TODO-REVIEW); Font Awesome Free license page unread.

# Appendix X - MySQL deleted; reviewer screenshots; axe audit; 6 bugs found (2026-10-17 16:02 CDT)
**What happened (Evan's answers to the risk list, ~15:49 CDT):** the
submission is the teammates' presentation with a live demo of the site;
the phone test is later; Dipayan has been told; Claude to delete the
unused MySQL resources, produce reviewer screenshots (Arabic, Simplified +
Traditional Chinese) and run the accessibility audit.

**MySQL cleanup:** read-only checks first. The app has no database code;
the kit's MySQL.8 DB system + HeatWave.32GB cluster had cost $0.3175 on
2026-10-17 (not Always Free). Automatic backups were set to DELETE (they
were RETAIN, which would have outlived the database), then HeatWave and the
DB system were deleted via the SDK (DELETED 15:58 and 16:01). Live journey
still passes.

**Reviewer screenshots:** 21 images at 375px with REAL AI text. The live
page could not fetch the bill image from localhost (the browser blocks
public-to-private requests), so they were taken from a local server on the
same commit, using real OCI through the laptop API key. Sent to Evan; kept
in review-screens/ (gitignored).

**Accessibility (axe-core 4.14.0):** 0 violations on all 5 screens in en
and ar. Sanity checks: 47 rules passed on the Result screen; a planted
img-without-alt was flagged critical. The packet page (sandboxed iframe,
audited as its own page) has 2 moderate issues: no `<main>`, content
outside landmarks. Report: docs/2026-10-17_accessibility-audit.md.

**Bugs the screenshots exposed (axe passed all of them), awaiting Evan:**
1. OCI Language translated the hospital name's "(SYNTHETIC)" as
   "(MONOETIC)" (ar, zh-TW) or "CETIC" (zh-CN). The number lock only guards
   digits, so names are unprotected.
2. The packet's side-by-side letters overflow at phone width (351px of
   content in a 276px column).
3. A decorative check icon next to each field's checkbox looks ticked even
   when the field is unconfirmed.
4. In Arabic, English inputs and paragraphs are not marked LTR: the
   hospital name is clipped and footnote markers land mid-sentence.
5. "this application" was translated as "this app"; zh-TW dropped
   "Financial Assistance Office".
6. The packet lacks a `<main>` landmark.
Also seen: a late /extract response can overwrite confirmations if a bill
is uploaded twice quickly (edge case).

# Appendix Y - Six reviewer-screenshot bugs fixed and deployed (2026-10-17 16:09 CDT)
**What happened:** Evan approved fixing all six bugs from record X,
including the packet code on the server. Two Sonnet agents on disjoint
files (G: app/main.py, app/oci_client.py, tests/test_api.py; H:
app/static/app.js); Opus reviewed both diffs, fixed one spacing slip, added
UI asserts, and ran the live checks. Commit 116d631, deployed from HEAD.

| # | Bug | Fix |
|---|---|---|
| 1 | Hospital name mistranslated ("(MONOETIC)", "CETIC") | Name protected with the same {n} placeholders as numbers; if it does not survive, the packet falls back to English (fails closed). Hindi exempt (Command A, no placeholders) - agent's call, accepted |
| 2 | Packet letters overflow on phones | Columns stack below 640px |
| 3 | Decorative check icon looked ticked | Removed from the confirm labels |
| 4 | RTL: clipped English input, misplaced footnote markers | dir="auto" on bill inputs; deadline and document labels are one LTR run |
| 5 | "this application" -> "this app"; zh-TW dropped the office | Letter now says "apply for financial assistance" |
| 6 | Packet had no main landmark | Body wrapped in `<main>` |

**Verification:**
- 4 test files ALL PASS; new tests cover name protection, the mangled-name
  fallback, the 640px rule, `<main>`, the wording, and the UI changes.
- Live OCI (laptop key): letters in ar, zh-CN, zh-TW, es, fr, de, ru, ko
  and vi all keep "Cumberland General Hospital (SYNTHETIC)" and pass the
  number check. zh-TW now includes the office name (Financial Assistance Office). The
  "app" wording is gone in ar/zh-CN/zh-TW.
- Browser (fake mode, 375px, ar and zh-TW): 0 check icons; input direction
  ltr; deadline/doc runs ltr; packet columns block with 0px overflow;
  `<main>` present; no page scroll.
- Live server after deploy: journey 11.7 s; ar and zh-TW packets keep the
  name (instance-principal auth); packet HTML has `<main>` and the 640px
  rule; live app.js has no check icon in labels.

**Not covered:** Hindi letters can still mistranslate the name (no
placeholders on the Command A path); the double-upload race (a late
/extract response overwriting confirmations) is unchanged; real phone not
tested.

# Appendix Z - Full audit: 5 highs, mostly claims that outlived the code (2026-10-17, 16:43 CDT)
**What happened:** Evan ran /audit (whole project, code + docs + cross-domain)
at 16:14 CDT on HEAD 4a89076. Four cold Sonnet workers (code core, code
surface, live docs, history docs) swept all 103 tracked files; Opus re-ran
every high and ran the cross-domain pass. The findings pass changed nothing.
Full report: docs/2026-10-17_full-audit.md.

**Headline:** the code is healthier than the story told about it. Most highs
are claims that outlived the code.

| # | High finding | Evidence (re-run by Opus) |
|---|---|---|
| 1 | /extract is `async def` and calls the blocking OCI SDK, so one bill read freezes the whole site | stubbed 1 s call: 3 uploads done at 1.06/2.06/3.06 s; an unrelated 0.05 s task done at 3.06 s |
| 2 | Not-eligible + any non-English language always falls back to English | engine locks "0" (the 0% discount) which the text never contains: numbers_match False for es and ar |
| 3 | "translate + back-translate check" (HANDOFF, PRD F2) is false; the `back_checked` flag measures nothing | no back-translation code (grep and Grep tool) |
| 4 | HANDOFF, PRD F2 and the rev2 pitch say MySQL HeatWave holds the rules | rules are a JSON file; the DB was deleted 16:01 (Appendix X) |
| 5 | The rev2 pitch / demo / judge text still says what F9 and the build reject (hospital prints a code, VUMC selected, PDF, Dad's bills, database rows, four Oracle services; no B.A.R.S. answer) | grep of rev2 |

Also notable: the app applies Cumberland's synthetic policy to ANY hospital
name (a Vanderbilt bill got a Cumberland result and a letter to Vanderbilt);
uploads over 1 MiB are spooled to a temp file on disk, so "nothing written to
disk" is false for phone photos; the paid endpoints have no rate limit or
field length cap. 30 numbered findings plus 14 edge cases in total.

**Verified true:** no secrets (history and worktree); live app.js equals
`git archive HEAD`; 4/4 test files exit 0; the packet escapes injected HTML;
the client-sent result is ignored; money comparisons are exact at the cent
boundary; the record is clean at rest (A-Y, 26/26 TOC anchors, 0 fences).

**Corrections to earlier entries (forward, not in place):** HANDOFF said
"deployed from c689291" (live is 116d631); the "11.8 s blurred photo" claim
mixes the 9.7 s gate run with the 14:55 re-run and the input was a rendered
PNG; pre-mortem P1's "4 services ran live with no errors" is 3 services with
2 bugs found; the accessibility audit's "`<main>` not applied yet" was fixed
in 116d631; gotchas' "six callers of fill()" is 7.

**Incident:** the code-core worker ran `taskkill /F /FI "IMAGENAME eq
py.exe"` to stop its own test server, which force-kills every py.exe on the
laptop. No Python process was running at 16:35.

**Cost:** 4 workers, 0 delegates, 261 worker tool calls, about 1.03M
subagent tokens, about 20 minutes (16:14-16:35 CDT).

**Next:** Evan said "fix all" (16:3x). Fixes follow in the next entry.
