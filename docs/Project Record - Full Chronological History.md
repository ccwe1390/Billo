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
