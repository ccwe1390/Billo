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
- **What it does (committed scope), two steps:**
  1. Summary bill in (photo or file) -> explain what it can in the user's
     language -> draft a letter asking the hospital for the itemized bill.
     The tool cannot produce an itemized bill; only the hospital can.
  2. Itemized bill + EOB in -> explain each line, flag likely errors
     (duplicates, bill-vs-EOB mismatches) with deterministic rules -> draft an
     appeal letter if needed.
  Letters are in English. **The user sends them** (decided 2026-10-17): one
  tap opens their own email app with the letter filled in, or downloads a
  PDF to mail. The app never sends anything itself.
- **Demo only:** a "send" button that delivers to a fake hospital inbox the
  team controls, clearly labelled as a demo. Not a product feature.
- **Add-on if time allows:** flag possible eligibility for a hospital's
  financial assistance (charity care) policy, modelled on one fictional
  hospital's policy.
- **Cut for this event:** No Surprises Act claims, negotiation/payment-plan
  letters, Discharge Companion, Med nudges.
- **Languages:** wave 1 = Spanish, Chinese (Simplified + Traditional),
  Arabic, Vietnamese, all translated by OCI Language. Hindi = additional
  option, OCI Generative AI only (not
  in OCI Language, so no back-translation check). Goal: top 10 US immigrant
  languages; ranks 7-10 not yet sourced.
- **How success is measured:** headline = precision and recall at catching
  errors we plant in a synthetic bill set (we write the bills, so ground truth
  is exact). Demo number = dollars of errors flagged on that same set. NO
  claim of real-world savings: there are no real users.
- **Must hold:** OCI for every AI part, for translation (OCI Language), and for
  hosting the website; synthetic data only; no diagnosis or
  treatment advice; no immigration status, SSN, or ID asked; nothing stored
  after a session; $500 OCI credits are the whole budget.

## Current state - PRD written, no code

**Last updated: 2026-10-17** - this file is the only live snapshot; history
lives in the record (Phase 0, Appendices A-H).

> **2026-10-17 - PRD written (record Appendix G).** Stack Next.js + OCI
> TypeScript SDK; one OCI Compute VM; Synthea-based bills with planted errors
> 1-6. Next task: PRD M0. Repo: private
> `github.com/Evan-Daruwalla/TNHacks26`, branch `main`.

### What is known vs missing

| Item | Status | Source |
|---|---|---|
| Track | **Known**: Track 2, Health Access, Equity & Experience | Evan, chat 2026-10-17 |
| Event name | **Known**: TNHacks26 (the local folder is still named TNHacks27) | Evan, chat 2026-10-17 |
| Module, users, metric, languages, flow | **Decided** (see Goal) | record Appendices A, B, D |
| Event dates / submission deadline | **MISSING** | - |
| Event rules, judging rubric, submission format | **MISSING** (only the track text exists) | - |
| Team roster and roles | **MISSING** | - |
| OCI | **Partly known**: mandatory; $500 credits; account, expiry, and service coverage MISSING | Evan, chat 2026-10-17 |
| Candidate OCI services | Document Understanding, Generative AI, Language - from Oracle docs, untested | services.md |
| Stack, hosting, data, errors | **Decided** (PRD_ROADMAP.md section 4) | record Appendix G |
| Code | **None yet** | - |
| Java + Synthea | **Installed**: Temurin 17 + Synthea jar in `C:Usersdaruw	ools`; 10-patient snapshot in `data/synthea/` (gitignored) | record Appendix H |

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
- `PRD_ROADMAP.md` - the standing plan (M0-M7). Source of truth for what to
  build and in what order.

## BLOCKED-ON-EVAN
- Event dates, submission deadline, rules/judging
  link, team roster.
- OCI: whose account holds the $500, expiry, and whether Generative AI,
  Document Understanding, and Language are covered.

## Next actions
1. PRD M0: Evan confirms OCI account + sets a budget alert (M0.1); then the
   extraction spike (M0.3). M0.2 done 2026-10-17.
2. M1-M2 can start before M0.1-M0.2 clear: scaffold, code map, rules, eval.
3. Evan supplies event facts (dates, rules, team).
