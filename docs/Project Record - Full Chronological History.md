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
