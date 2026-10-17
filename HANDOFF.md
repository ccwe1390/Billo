# Handoff

## Goal

**Mission (internal north star, decided 2026-10-17; product name is a
placeholder):** [Name] helps immigrant and low-income patients, and the family
members who read medical bills for them, understand a hospital bill in their
own language and spot likely billing errors before they pay. It explains and
flags; the person decides what to do.

### Project intent

- **Problem:** hospital bills and insurer EOBs (explanation of benefits) are
  hard to read, and harder in a second language. Errors and duplicate charges
  go unchallenged when the patient cannot tell they are errors.
- **Users:** limited-English and low-income patients, plus the family member
  (often a grown child) who reads the bill for them.
- **What it does (committed scope):** reads a bill + EOB (photo or file),
  explains each line in plain words in the user's language, flags likely
  errors (duplicates, bill-vs-EOB mismatches) with deterministic rules, and
  drafts an appeal or itemized-bill request letter in English for the user to
  review and send themselves.
- **Add-on if time allows:** flag possible eligibility for a hospital's
  financial assistance (charity care) policy, modelled on one fictional
  hospital's policy.
- **Cut for this event:** No Surprises Act claims, negotiation/payment-plan
  letters, Discharge Companion, Med nudges.
- **Languages:** wave 1 = Spanish, Chinese (Simplified + Traditional),
  Arabic, Vietnamese. Hindi = additional option, OCI Generative AI only (not
  in OCI Language, so no back-translation check). Goal: top 10 US immigrant
  languages; ranks 7-10 not yet sourced.
- **How success is measured:** headline = precision and recall at catching
  errors we plant in a synthetic bill set (we write the bills, so ground truth
  is exact). Demo number = dollars of errors flagged on that same set. NO
  claim of real-world savings: there are no real users.
- **Must hold:** OCI for every AI part; synthetic data only; no diagnosis or
  treatment advice; no immigration status, SSN, or ID asked; nothing stored
  after a session; $500 OCI credits are the whole budget.

## Current state - Planned, not built: mission set, no code

**Last updated: 2026-10-17** - this file is the only live snapshot; history
lives in the record (Phase 0, Appendices A-C).

> **2026-10-17 - Mission and scope set (record Appendix B).** Bill Decoder is
> the one module. No code, no PRD yet. Repo: private
> `github.com/Evan-Daruwalla/TNHacks26`, branch `main`.

### What is known vs missing

| Item | Status | Source |
|---|---|---|
| Track | **Known**: Track 2, Health Access, Equity & Experience | Evan, chat 2026-10-17 |
| Event name | **Known**: TNHacks26 (the local folder is still named TNHacks27) | Evan, chat 2026-10-17 |
| Module, users, metric, languages | **Decided** (see Goal) | record Appendices A-B |
| Event dates / submission deadline | **MISSING** | - |
| Event rules, judging rubric, submission format | **MISSING** (only the track text exists) | - |
| Team roster and roles | **MISSING** | - |
| OCI | **Partly known**: mandatory; $500 credits; account, expiry, and service coverage MISSING | Evan, chat 2026-10-17 |
| Candidate OCI services | Document Understanding, Generative AI, Language - from Oracle docs, untested | services.md |
| Code, PRD | **None yet** | - |

### Track requirements (from the pasted text, 2026-10-17)

- Go deep on a clearly defined problem, user group, and measurable outcome.
- Use OCI Generative AI and privacy technologies; meaningful use of Oracle/OCI
  is a success criterion.
- Synthetic, public, or de-identified data only; NO autonomous diagnostic or
  treatment decisions; privacy, transparency, accessibility, bias mitigation,
  human oversight from the outset.

## Documentation
- `docs/Project Record - Full Chronological History.md` - append-only
  chronological record (no HTML twin). Append with
  `node C:\Users\daruw\.claude\skills\project-memory\append-record-entry.js`.
- `.claude/project-memory/` - binned memory; `important.md` first, then
  `INDEX.md`. DIRECTORY.md skipped (no source files yet).
- `.claude/pm-cadence.json` - local cadence-hook state, gitignored.
- No `PRD_ROADMAP.md` yet: next to write.

## BLOCKED-ON-EVAN
- Event dates, submission deadline, rules/judging
  link, team roster.
- OCI: whose account holds the $500, expiry, and whether Generative AI,
  Document Understanding, and Language are covered.

## Next actions
1. Write `PRD_ROADMAP.md` from the Goal above (grill any open design forks
   first: stack, hosting, synthetic-bill generator, error types to plant).
2. Evan supplies event facts and OCI account access.
3. First build task once OCI works: a tiny paid-call smoke test with a budget
   alert set first (important.md 5).
