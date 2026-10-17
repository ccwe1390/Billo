# TNHacks26 - Bill Decoder PRD & Roadmap

**Written 2026-10-17 by Claude (Opus 5.5) from the planning grill with Evan
(record Appendices A-F + the PRD grill entry). Standing document - the
executing model works through TASK BREAKDOWN top to bottom, one task at a
time, and checks off SUCCESS CRITERIA.**

**GOAL:** A working web app, hosted on one OCI Compute VM, that takes a
hospital bill and an insurer EOB (photo or file), explains every line in the
user's language (Spanish, Chinese, Arabic, Vietnamese; Hindi optional), flags
billing errors 1-6 with fixed rules, and drafts an English letter the user
sends themselves - plus a measured result: per-error-type precision and
recall on a seeded synthetic test set built from Synthea with planted errors.
Everything runs on OCI and synthetic data; nothing is stored after a session.

**SCOPE GUARD (decided by Evan 2026-10-17): no real patient data anywhere; no
diagnosis, treatment, or triage output; the app never sends anything itself
(the demo-only send goes to a team-controlled fake inbox); nothing about a
user or their bill is stored or logged after the request; no AI provider
other than OCI without Evan's OK. If a task seems to require breaking one of
these, STOP and report.**

---

## 1. OBJECTIVE

Limited-English and low-income patients, and the family members who read
bills for them, can't tell when a hospital bill is wrong. The app explains
the bill in their language and points out charges that fixed rules show are
likely errors. It never decides for them. Step 1: a summary bill gets an
explanation and a letter asking the hospital for the itemized bill. Step 2:
the itemized bill + EOB get a line-by-line check and, if needed, an appeal
letter.

## 2. CONTEXT

### What exists (verified 2026-10-17)
- Docs only: `HANDOFF.md`, `docs/Project Record - Full Chronological
  History.md`, `.claude/project-memory/` (bins; read `important.md` first).
- No code, no OCI account access yet, no Java, no Synthea data on disk.
- Repo: private `github.com/Evan-Daruwalla/TNHacks26`, branch `main`.

### Must not break
- Synthetic data only: every file under `data/` is generated or comes from
  Synthea, and says so in `data/README.md`.
- The rules engine is deterministic: same input JSON -> same flags, byte for
  byte (`determinism-guard` can prove it).
- Dataset builds are seeded: two runs with the same seed produce identical
  files.
- No uploaded content in logs: a grep of server logs after a test upload
  finds none of the test bill's text.
- Explanations contain no diagnosis or treatment advice (banned-phrase test).

## 3. SUCCESS CRITERIA

- [ ] `npm run build` and `npm test` pass on a clean checkout.
- [ ] `npm run dataset -- --seed 42` builds the synthetic set; a second run is
      byte-identical.
- [ ] `npm run eval` prints per-error-type precision/recall and dollars
      flagged for (a) structured JSON and (b) image -> OCI extraction.
- [ ] The web app on the OCI VM completes step 1 and step 2 for a synthetic
      bill in each wave-1 language, with Arabic laid out right-to-left.
- [ ] Letters download as PDF and open the user's email app pre-filled.
- [ ] Dated accessibility audit output saved in `docs/design/`.
- [ ] OCI budget alert set below $500 before the first paid call.

## 4. CONSTRAINTS

- Stack (decided by Evan 2026-10-17): Next.js + TypeScript everywhere, OCI
  TypeScript SDK per-service packages (`oci-aidocument`,
  `oci-generativeaiinference`, `oci-ailanguage`; 2.143.0 seen 2026-10-17).
- Hosting (Evan 2026-10-17): one OCI Compute VM, Node behind a reverse proxy;
  instance principals for AI calls if they work (verify), else an API key
  stored outside the repo.
- Translation (Evan 2026-10-17): OCI Language for es, zh-CN, zh-TW, ar, vi;
  Hindi via OCI Generative AI, marked "not back-translation-checked".
- Letters are filled from fixed templates (deterministic); the LLM does not
  write legal text.
- Budget: $500 OCI credits total; estimate cost before any batch run; cache
  OCI responses during development.
- Codes: Synthea gives SNOMED-CT; we keep our own SNOMED -> CPT/HCPCS map with
  descriptions in our own words (CPT descriptor licensing unverified).
- Out of scope - do not start these even if convenient: upcoding,
  unbundling, No Surprises Act letters, negotiation/payment-plan letters,
  accounts/logins, storing bills, Discharge Companion, Med nudges.
- Environment: Windows 11, PowerShell 5.1 + Git Bash. Never rewrite JSON with
  PowerShell (UTF-8 damage); avoid `node -e` with quotes. All `.md` ASCII-only.

## 5. MILESTONES

| # | Milestone | Goal |
|---|---|---|
| M0 | Access + risk spikes | OCI works, budget alert set, Synthea data on disk, extraction tested on one bill |
| M1 | Synthetic data pipeline | Seeded bill+EOB set with planted errors and an answer key |
| M2 | Rules engine + eval | Rules 1-6 and the precision/recall script on structured JSON |
| M3 | OCI extraction | Image -> Document Understanding -> JSON; end-to-end headline metric |
| M4 | Explain, translate, letters | Plain-language lines in 5 languages; template letters |
| M5 | Web app | Step 1 + step 2 flows, RTL, accessible, nothing stored |
| M6 | Deploy on OCI | The app live on the VM; demo-only send |
| M7 | Stretch | Error 7 (MUE units), financial-assistance add-on, Hindi |

Order is riskiest-first: M0 tests the two things most likely to sink the
plan (OCI access/cost and whether Document Understanding can read a bill
table) before any pipeline is built. M1-M2 need no OCI calls, so they can run
while M0's blocked items wait on Evan.

## 6. TASK BREAKDOWN

### M0 - Access + risk spikes

1. **OCI access and budget alert.** BLOCKED-ON-EVAN: confirm which account
   holds the $500, its expiry, and set a budget alert (e.g. at $100 and
   $300) in the OCI console. Done: Evan confirms; values recorded in
   `budget.md` and `services.md` (names only, no secrets).
2. **Synthea data.** BLOCKED-ON-EVAN: approve either installing a JDK or
   downloading a prebuilt Synthea CSV sample. Then place CSVs in
   `data/synthea/` (gitignored if large). Done: row counts of
   `claims_transactions.csv`, `claims.csv`, `encounters.csv` recorded in
   `data.md`.
3. **Extraction spike.** Hand-make one bill page (HTML -> PDF and PNG) with
   ~10 lines, send it to Document Understanding table extraction, compare to
   the known lines. Files: `spikes/extract-one/`. Done: printed field-level
   match rate and the per-page cost, recorded in `experiments.md`.
4. **Explain + translate spike.** One bill line -> Generative AI plain
   English -> OCI Language to es and ar -> back to English. Files:
   `spikes/translate-one/`. Done: outputs and cost recorded in
   `experiments.md`; amounts survive the round trip unchanged.

### M1 - Synthetic data pipeline

1. **Scaffold.** Next.js + TypeScript app, vitest, eslint, `.gitignore`
   (`data/synthea/`, `.env*`). Done: `npm run build` and `npm test` pass.
2. **Code map.** `src/codes/map.ts`: SNOMED -> CPT/HCPCS + our own short
   description, for every procedure code in the Synthea sample. Done: test
   lists 0 unmapped codes, or an explicit "unmapped" list reviewed by Evan.
3. **Bill/EOB model + Synthea loader.** `src/model/`, `src/synthea/load.ts`:
   one encounter -> `Bill` + `Eob` objects. Done: tests; on clean data the
   bill patient balance equals the EOB patient responsibility for every
   encounter.
4. **Error planter.** `src/plant/`: one function per error type 1-6; each
   mutates a clean pair and appends an answer-key entry with type, line, and
   dollar value. Done: one test per type; seeded (passes `seed-control`).
5. **Dataset builder.** `scripts/build-dataset.ts`: ~60 pairs, ~1/3 clean,
   writes `data/synthetic/<id>/{bill,eob,answer}.json`. Done: two runs with
   `--seed 42` are byte-identical.
6. **Renderer.** `src/render/`: bill and EOB to PDF and a "phone photo" PNG
   (slight rotation, blur, shadow) in 3 layouts. Done: files exist for every
   pair; Evan eyeballs 3 samples.

### M2 - Rules engine + eval

1. **Rules 1-6.** `src/rules/`: pure functions over `Bill` + `Eob`, each
   returning flags with reason and dollar amount. Done: one test per rule;
   clean pairs produce zero flags.
2. **Eval script.** `scripts/eval.ts`: precision, recall, and dollars flagged
   per type versus the answer key. Done: prints the table on structured JSON
   (the upper bound); result recorded in `experiments.md`.

### M3 - OCI extraction

1. **Extraction client.** `src/oci/extract.ts`: image/PDF -> Document
   Understanding -> `Bill`/`Eob` JSON, with an on-disk response cache for dev.
   Done: field-level accuracy on 10 rendered pairs printed.
2. **End-to-end eval.** Cost estimate for the full set FIRST (important.md
   5), then image -> extract -> rules -> eval. Done: headline table recorded
   in `experiments.md` beside the structured upper bound.

### M4 - Explain, translate, letters

1. **Line explainer.** `src/oci/explain.ts`: Generative AI writes one plain
   English sentence per line, grounded only in the line's fields and our code
   map. Done: snapshot tests on fixed inputs; banned-phrase test (diagnosis,
   treatment, "you should take") passes.
2. **Translation.** `src/oci/translate.ts`: OCI Language for es, zh-CN,
   zh-TW, ar, vi; back-translation check that every number and dollar amount
   survives. Done: 100% of amounts preserved on the test set.
3. **Letters.** `src/letters/`: itemized-bill request and appeal templates
   filled from flags; PDF output; mailto link builder. Done: tests on 3
   flagged pairs.

### M5 - Web app

1. **Upload flow.** Step 1 (summary bill) and step 2 (itemized + EOB),
   language picker. Done: works locally on synthetic files.
2. **Results view.** Explanations, flags with dollar amount and reason, the
   line "This is not medical or legal advice; you decide." Arabic RTL. Done:
   manual check in each wave-1 language.
3. **Nothing stored.** Process in memory; no request-body logging. Done: log
   grep after a test upload finds no bill text.
4. **Accessibility.** Run an automated audit (e.g. axe). Done: output saved
   dated in `docs/design/`.

### M6 - Deploy on OCI

1. **VM.** BLOCKED-ON-EVAN for console steps (shape, network, Always Free
   check). Then reverse proxy + HTTPS + process manager, scripted. Done: the
   public URL completes step 2 on a synthetic pair.
2. **Demo-only send.** Design is open (which fake inbox, which service) -
   decide with Evan before building. Done: labeled demo send works.

### M7 - Stretch (only after M0-M6)

1. Error 7: units above CMS MUE limits (verify the table is public first).
2. Financial-assistance add-on against one fictional hospital policy.
3. Hindi via Generative AI, labeled not back-translation-checked.

## 7. HANDOFF NOTES

**Read first, in order:** `.claude/project-memory/important.md` ->
`HANDOFF.md` -> this file -> record front-matter.
**Work order:** M0 -> M7. M1-M2 may proceed while M0 tasks 1-2 wait on Evan.
One task per sitting; finish (done-check + tests + record entry) before the
next. **Commits: only when Evan asks; never push without his instruction**
(per-task commits not yet authorized).
**Gotchas that will bite you:**
- Synthea procedure codes are SNOMED-CT, not CPT/HCPCS - bills need our map.
- Java is not installed on Evan's machine (checked 2026-10-17).
- OCI Language has no Hindi, Tagalog, or Haitian Creole.
- Document Understanding table extraction may be English-only (docs
  disagree) - fine for US bills, verify in M0.3.
- Every paid OCI call counts against $500; cache responses.
- Event dates and deadline are unknown - do not invent a schedule.
