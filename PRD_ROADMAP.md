# TNHacks26 - Bill Decoder PRD & Roadmap

> **SUPERSEDED by the 2026-10-17 fork.** The Bill Decoder plan below (GOAL through section 7) is kept for history. The current plan is the **CURRENT DIRECTION (forked 2026-10-17)** section at the end of this file.

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
2. **Synthea data.** **[x] DONE 2026-10-17 (record Appendix H): JDK route; canonical snapshot `data/synthea/s42-p10-r20261017-t1/`.** Was BLOCKED-ON-EVAN: approve either installing a JDK or
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
- ~~Java is not installed on Evan's machine (checked 2026-10-17).~~ (struck 2026-10-17: Temurin 17 installed portably at `C:\Users\daruw\toolsjdk-17.0.20.1+1`, not on PATH)
- Synthea MUST run with `--generate.thread_pool_size=1`, or the same seed gives different files (data.md).
- Synthea output has no contractual adjustments; error type 3 needs adjustments we generate in M1.3 (design open).
- OCI Language has no Hindi, Tagalog, or Haitian Creole.
- Document Understanding table extraction may be English-only (docs
  disagree) - fine for US bills, verify in M0.3.
- Every paid OCI call counts against $500; cache responses.
- ~~Event dates and deadline are unknown - do not invent a schedule.~~ (struck (2026-10-17 16:55 CDT, audit record Z/AA): dates are known, see F6)
- OCI starter kit (github.com/ScottStroz/oci-hackathon-starterkit, read 2026-10-17): home region MUST be US Midwest (Chicago) and is permanent; the kit's VM has Node 16, too old for Next.js (needs Node >= 20.9) - install a current Node LTS in M6.1; its default shape E5.Flex is paid; Free Trial Generative AI model is cohere.command-a-03-2025 (no Grok). See services.md.

---

## CURRENT DIRECTION (forked 2026-10-17 ~13:05 CDT): Bill to Help - bill photo to financial assistance packet

**Why forked:** the research brief
(`docs/research/2026-10-17_bill-decoder-crowding.md`) found the bill/EOB error
checker crowded, and uninsured families get no EOB. Evan adopted the draft
"HackTN26 Health Access Plan" (record Appendix L), with Python as the stack
and the agenda's deadline (decided by Evan, 2026-10-17). Everything above
this heading is SUPERSEDED. Error checking moves to Deferred.

**GOAL:** By **Sun 2026-10-18 1:00 PM CDT** (hacking finishes; showcase
1:05 PM), a web app running on our OCI VM turns a photo of a (synthetic)
Nashville hospital bill into that hospital's financial assistance packet:
- an eligibility estimate against the hospital's published policy and the
  2026 HHS poverty guidelines, with every rule showing source, page, and
  effective date;
- pre-filled application fields, a document checklist, the deadline, and a
  short English cover letter;
- all explained in Arabic or Spanish for the family member helping a parent.

The AI never decides: a vision model reads, a deterministic Python rules
engine decides, a language model only phrases, and every number is locked.
Nothing a user enters is stored. The family submits; the hospital decides.

**SCOPE GUARD (decided by Evan 2026-10-17):**
- Synthetic bills only, watermarked SYNTHETIC; no real patient data.
- No immigration status, SSN, or ID questions.
- No user data written anywhere.
- No claim of "first", "unique", "money saved", or "we apply for you".
- OCI only.
- No diagnosis or treatment content.
- If a task needs any of these broken, STOP and report.

### F1. Product (the one journey that must work live, in under 90 seconds)

Five screens:
1. **Start:** pick a language (~~Arabic / Spanish / English~~ ~~11 languages; tier 1 en/es/ar/zh-CN/zh-TW translated interface, (2026-10-17 16:55 CDT, audit record Z/AA))~~ 32 languages from a dropdown, every one with a translated interface (2026-10-17 20:13 CDT, Evan, record AI)) and "This bill is
   for: me / a family member". Show "Nothing you enter is saved. Demo uses
   synthetic bills only."
2. **Bill:** upload or photograph the bill. Extracted fields appear beside
   the image: hospital, statement date, account number, amount due, date of
   service, insurance status. Each field is editable and must be confirmed.
   Unreadable fields are left blank and asked for, never guessed.
3. **Three questions:** household size; yearly household income; "Do you
   file a tax return?" (changes the document list).
4. **Result** in the chosen language, with an English toggle: percent of the
   2026 poverty guideline, the policy tier with its citation (source, page,
   effective date), the deadline, three lines on what the bill is, and a
   ~~Tennessee uninsured-protections card~~ (hidden in 145c8af: no sourced text). Income over the policy's limits
   gives an honest "not eligible under this policy" plus the payment-plan
   contact.
5. **Packet:** pre-filled application fields, the policy's document
   checklist, an English cover letter with the Arabic/Spanish translation
   beside it, and where to send it. Delivered as a **printable HTML page**
   (Arabic shaping is handled by the browser; decided 2026-10-17). A server
   PDF is not built.

### F2. Architecture (all on OCI; stateless)
- Python (FastAPI) + plain HTML/JS, one process on the starter-kit VM
  (decided by Evan 2026-10-17; supersedes Next.js).
- Endpoints: `POST /extract` (image -> fields with per-field confidence;
  missing = null), `POST /evaluate` (fields + answers -> result with
  citations), `POST /explain` (result + language -> text), `POST /packet`
  (everything -> printable page).
- OCI Generative AI, **Cohere Command A Vision** (extraction) and **Command
  A** (phrasing), in US Midwest (Chicago). Listed on-demand in Chicago per
  Oracle's models-by-region page (via search). Free-trial availability is
  UNTESTED; confirm exact model IDs in the console.
- OCI Language: translates the cover letter~~, and back-translates generated
  Arabic/Spanish to check numbers~~. (Struck (2026-10-17 16:55 CDT, audit record Z/AA): no back-translation was
  built - cut-order item 4. The check is {n} placeholders for numbers and the
  hospital name, then the number lock.)
- Number lock: every number, date, and dollar amount in generated text must
  match the engine's output; any mismatch falls back to a fixed template.
- ~~MySQL HeatWave (from the kit): policy registry (hospital, rule, value,
  source, page, effective date, verifier). No patient data. Cut to a JSON
  file if time runs short.~~ (Struck (2026-10-17 16:55 CDT, audit record Z/AA): built as a JSON file,
  app/data/policy_cumberland_synthetic.json, with no verifier field; the kit's
  MySQL/HeatWave was never used and was deleted 16:01, record X.)

### F3. Data
- VUMC financial assistance policy, Appendix B, plain-language summary, and
  application (public PDFs). **Gate 3:00 PM Sat:** if VUMC's thresholds can't
  be confirmed from VUMC's own PDF, use a labeled synthetic hospital
  ("Cumberland General, synthetic") with the same rule structure.
- 2026 HHS poverty guidelines: $15,960 for 1 person, $33,000 for 4, +$5,680
  per extra person. Checked via search summaries (ASPE); re-read the source
  before it goes on a slide.
- 10 synthetic bills (SYNTHETIC watermark, fake names and accounts, no
  logos) and a 20-household answer key, both hand-computed. (Status (2026-10-17 16:55 CDT, audit record Z/AA):
  2 bills exist, bill-01 and bill-02 with 4 blur levels; no 20-household key -
  tests/test_engine.py has boundary cases instead.)

### F4. Acceptance criteria (the done-checks)
- [ ] (NOT MET: 2 bills, n=1 runs) On 10 synthetic bills, the 4 key fields (hospital, statement date,
      amount due, account number) are read correctly - report the real
      count.
- [x] (met: engine refuses unconfirmed fields, test_api) No field is used until the user confirms it; edits override the
      model.
- [ ] (NOT MET: no 20-household key; boundary tests only) Tier results match the hand-computed key on 20 test households.
- [x] (met: engine citations + footnotes, record W) Every rule on screen shows its source document, page, and effective
      date.
- [x] (met: RTL browser check record W; number lock on every translation) Arabic renders right to left; every number and date in the
      Arabic/Spanish text matches the English exactly.
- [x] (met in English; in other languages only after audit fix #2, record AA) Over-limit income gives an honest "not eligible under this policy"
      with the payment-plan contact.
- [x] (met: extra="forbid"; uploads kept in memory since audit fix #7, record AA) No screen asks for immigration status, SSN, or ID; no user data is
      written anywhere.
- [x] (met: 11.7 s live at 16:08, n=1) The full journey runs in under 90 seconds on the deployed OCI
      address.

**Cut order if short:**
1. ~~PDF~~ (already a printable page)
2. Database -> JSON file
3. Spanish (keep Arabic)
4. Back-translation check (keep the number lock)
5. Camera capture (keep upload)

**Never cut:** extraction, confirmation, the cited rule result, the packet.

### F5. Validation (rubric: "Have real customers provided input?")
- **V1 (first hour, no people needed):** give the synthetic bill to Claude,
  ChatGPT, and Gemini (free tiers), 3 runs each, in English and Arabic, with
  the prompt "My dad got this bill from the hospital. He doesn't have
  insurance. What should we do?" Score yes/no on 5 points:
  - mentions financial assistance unprompted;
  - states VUMC's limits correctly;
  - gives a deadline;
  - lists VUMC's documents;
  - produces a filled application or letter.
  This decides the pitch.
- **V2 (Sat afternoon + dinner check-in 6 PM):** 6-10 interviews with
  attendees who helped a family member with a medical bill. No names,
  amounts, or documents; quotes only with permission.
- **V3 (Sun 9:00-10:30 AM):** a timed task comparison with 6-8 attendees,
  current workaround vs our app, scored 0-4 against the answer key, order
  alternated.
- **Emails to VUMC financial assistance and Dollar For:** outward-facing.
  Evan sends them himself; draft for his review first.
- Report every number with its sample size. Never convert results to
  dollars saved.

### F6. Schedule (agenda: `docs/Hackathon Schedule.txt`; venue closes Sat 9:00 PM, reopens Sun 9:00 AM)

| By | Gate |
|---|---|
| Sat ~1:45 PM | One successful Command A Vision call. JSON shapes agreed (bill fields, household answers, engine result, packet). Ask organizers what to submit and where. |
| Sat 3:00 PM | VUMC rules confirmed from VUMC's PDF, or the synthetic hospital |
| Sat 5:00 PM | A bill photo becomes a cited eligibility result on the OCI server. If not, stop adding features and fix that |
| Sat 9:00 PM | Leave the venue; remote work only after this |
| Sat ~11:00 PM | Feature freeze |
| Sun 9:00-10:30 AM | V3 task comparison; rehearsal |
| Sun ~12:00 PM | Recorded backup of the demo journey (lunch is 12:00) |
| **Sun 1:00 PM** | **Hacking finishes** |
| Sun 1:05 PM | Showcase |
| Sun 3:30 PM | Final pitches |

### F7. Failure modes
| Failure | Early warning | Fallback |
|---|---|---|
| Generative AI unavailable, or bill reading unreliable | First call fails by ~1:45 PM, or fewer than 7/10 bills read correctly | Manual entry beside the bill image; everything else still runs on OCI. Say "photo reading off in this demo." |
| VUMC thresholds unconfirmed | 3:00 PM gate | Labeled synthetic hospital; VUMC is "next step with the hospital's sign-off" |
| Live demo fails on stage | Any rehearsal over 90 seconds | Recorded backup plus a local copy |

### F8. Open items
- **Prior art to name honestly in judge Q&A:** B.A.R.S. (hackUMBC 2026 Second
  Overall: bill photo -> financial-assistance application, policy
  extraction; Maryland) and CareRoute (paid, EN/ES).
- Submission form, repo, and video requirements: ask organizers.
- Team roster and roles: unconfirmed (the plan assumes 4).
- Superseded-plan leftovers that no longer apply: Synthea snapshot (optional
  for realistic line items), error types 1-6.

### F9. Amendments (2026-10-17 ~13:47 CDT): revised team plan adopted with fixes

Source: `docs/2026-10-17_HackTN26_Health_Access_Plan_rev2.txt` (rev 2 of the
team plan, with mentor-feedback additions). Evan: "docs/Hackathon
Schedule.txt is ground truth; adopt with fixes". Where rev 2 and this section
disagree, this section wins. F1-F8 above still stand except where changed
here.

**Times.** `docs/Hackathon Schedule.txt` is ground truth: hacking finishes
Sun 1:00 PM, venue closes Sat 9:00 PM. Rev 2's "12:00 pm" and "8 pm" are
rejected. F6 is unchanged.

**Wording fixes (pitch, demo, judge answers):**
1. Storage: "Nothing is stored on our server. If the family chooses to save,
   bills stay on their own phone." Replaces "nothing a family enters is
   stored" (pitch) and "no saved records" (judge answer 5).
2. QR: "In a pilot, the hospital would print this code on its statements."
   Present-tense "The hospital prints..." is false today and is cut
   everywhere (pitch, 0:00 narration, judge answer 9).
3. Estimate: "Up to $X could be reduced if the hospital approves" stays,
   but X is computed by the engine (sum over bills of balance x the tier's
   `discount_percent` / 100), goes into `locked_numbers`, and is rendered
   from data, never written by a model. Rev 2's rule "never turn any of it
   into dollars saved" becomes: no savings claims; only engine-computed
   estimates labeled "if the hospital approves".

**Demo-script conditions:**
- 0:14 "It left the blurry date blank instead of guessing" is said only if
  a test shows it. Build `bill-02` (date of service printed once) with blur
  variants; run Command A Vision on each. If the model guesses, the line
  becomes "it misread the date; she fixes it before anything is used".
- 0:56 "the policy opens at the cited page": the app serves a labeled
  SYNTHETIC policy page (`/policy-cumberland.html#page-1`, `#page-2`) so
  citations open on either branch of the 3 PM gate. If VUMC passes the gate,
  citations link VUMC's own PDF and page.
- 1:24 "One approval may cover all five bills" only if someone reads VUMC's
  Period of Eligibility in VUMC's own PDF. For the synthetic hospital: not
  said.

**New features, gated:**
- (NOT BUILT as of (2026-10-17 16:55 CDT, audit record Z/AA)) Home "Dad's bills": a page built from engine output over 5 seeded
  SYNTHETIC bills. Opt-in save uses the browser's own storage (the server
  stays stateless; no `saved_bills` table, no login). Start only after the
  5 PM gate passes.
- (NOT BUILT) Reminders: preview only (computed dates: deadline, day 30 follow-up).
- Partner dashboard: a labeled mockup on slide 7. Not built (it would need
  server-side event writes).
- (NOT BUILT: no QR on either synthetic bill, no `?hospital=` handling) QR entry: a link with `?hospital=cumberland_synthetic`, printed on the
  synthetic bill once the VM's public address exists.

**Unchanged and now also in scope from rev 2:** validation tasks 1-3, the
interview script, the pitch, the slide outline, and judge answers, with the
wording fixes above. Emails to VUMC and Dollar For stay Evan's to send.

**F9 addendum (2026-10-17 16:55 CDT, audit record Z/AA).** Wording fix 1 above is struck: ~~"If the family
chooses to save, bills stay on their own phone."~~ There is no save feature,
so that sentence would claim an unbuilt feature. Keep "Nothing is stored on
our server" until a save exists. Line-by-line pitch, demo and judge-answer
corrections: docs/2026-10-17_pitch-corrections.md (draft for Evan).

### F10. DRAFT (2026-10-17 18:12 CDT) - the five F9 features, specified

**Status: APPROVED by Evan 2026-10-17 ~18:35 CDT with D1a, D2b, HTTPS included,
QR via a vendored JS library, and the product renamed "BillScan". Building on
branch `f10`; nothing deploys until Evan says go (Dipayan's React PR #1 is out
of scope). Plan: ~/.claude/task-plans/tnhacks26-f10.md.** (was: DRAFT) Written by
Claude after the audit fixes went live (c4a28f0, record AB). Scope: the demo
app only; the presentation belongs to other team members. Where this section
and F9 disagree, F10 wins once Evan approves it.

**Two decisions for Evan (defaults are Claude's recommendations):**
- D1 Saving bills: **(a) default** - seeded synthetic bills plus the current
  bill kept in page memory only; nothing is saved. (b) opt-in browser storage
  (localStorage) - breaks ui.md hard rule 4 unless Evan approves it.
- D2 Dashboard: **(a) default** - a labeled slide mockup, made by teammates.
  (b) a live page of counts kept in server memory (no personal data, no disk,
  wiped on restart); the privacy line becomes "counts only".

**Rules for every F10 feature:**
- Synthetic only: every new bill, rule and page carries SYNTHETIC; nothing
  imitates a real hospital.
- The engine decides. Every number on a new screen comes from engine output
  and is in `locked_numbers` if generated text can repeat it.
- New UI strings get en/es/ar/zh-CN/zh-TW with `// TODO-REVIEW es+ar+zh`;
  English policy text stays left-to-right (`bdiEn`, `englishOnly`).
- Each feature is its own commit, its own deploy, and a live journey after
  it. Rollback target = the commit before it. Contract changes are additive
  and dated in docs/contracts.md.
- Feature freeze ~23:00 Sat (F6). A feature not passing its done-check by
  then is cut, not rushed.

#### F10.1 Home "Dad's bills" (rev2 beat 1:24) - size L, about 2 h

- **What the user sees:** after the Result screen, a "See all of Dad's bills"
  button opens a Home screen: 5 bills from one emergency visit, each row with
  hospital, statement date, amount due, deadline and tier, plus one headline:
  "Up to $X could be reduced if the hospital approves. Estimate. Synthetic
  bills. The hospital decides." Never the word "saved".
- **Data:** `app/data/demo_bills.json`, 5 SYNTHETIC Cumberland General bills,
  fields already confirmed. Two match the existing images: bill-01 ($4,812.40,
  statement 2026-10-01, service 2026-09-12) and bill-02 ($1,858.50, statement
  2026-10-05, service 2026-09-20). Three new fixtures (amounts are fiction):
  clinic follow-up $642.00 (statement 2026-10-09, service 2026-09-26), lab
  $318.75 (statement 2026-10-12, service 2026-09-26), imaging follow-up
  $1,206.00 (statement 2026-10-14, service 2026-10-02). Total $8,837.65.
- **Server:** `POST /household` with the household answers (and, under D1a,
  the user's current confirmed bill) returns, per bill, the engine result,
  plus `estimate_cents` = sum over bills of amount_due x tier
  `discount_percent` / 100, rounded down to the cent, and an
  `estimate_text_en`. The engine gains `evaluate_many(bills, answers, policy,
  fpl)`; `estimate_cents` formatted is added to `locked_numbers`. Not a paid
  endpoint (no model call), so no rate limit.
- **Saving:** D1a - the user's bill joins the list for this page session
  only, labeled "(your bill)". D1b - a "Save to this phone" button writes the
  confirmed fields only (never the photo) to localStorage, with a "Delete my
  saved bills" button; off until the user taps it.
- **Done-check:** a test_engine case for evaluate_many (free care at 115%:
  estimate = $8,837.65; not eligible: estimate = $0 and the headline says
  "not eligible under this policy"); a test_api case for /household; a
  browser check in en and ar at 375 px (no sideways scroll, rtl, the headline
  number equals the engine's); live journey passes.

#### F10.2 One approval covers several bills - size S, about 20 min

- **Policy (ours, synthetic):** add page 3 to policy-cumberland.html and a
  rule to the policy JSON: "An approved application covers every Cumberland
  General bill for services from 240 days before the application date
  through 180 days after the approval date." Cited like every other rule.
- **Engine:** `evaluate_many` takes `as_of` (the server's date, passed in so
  the engine stays pure) and reports `one_application_covers_all` = every
  bill's date of service is on or after as_of - 240 days.
- **What the user sees:** on Home, "One approval may cover all 5 bills" with
  its footnote, shown only when that flag is true.
- **Done-check:** test_engine: true for the 5 fixtures with as_of
  2026-10-17; false when one service date is 241 days before as_of;
  test_policy_page still passes and page 3 exists.

#### F10.3 Reminders - size S, about 30 min (after F10.1)

- **What the user sees:** a Reminders card on Home: "Apply by <earliest
  deadline>"; "30 days after you apply: if you have no decision, call
  <phone>"; "New bill from this hospital? Your answers are reused" (in page
  memory only).
- **Calendar file:** an "Add to my calendar" button builds an `.ics` file in
  the browser (two events: the deadline and today + 30 days) and downloads
  it. Nothing goes to the server. Event titles in the chosen ~~tier-1~~
  language (every language has a translated interface since record AI); dates and the phone number unchanged.
- **Done-check:** a node check that the generated .ics has 2 VEVENTs with
  DTSTART equal to the deadline and today + 30; browser check that the
  download fires; the button makes no network request.

#### F10.4 QR entry (rev2 beat 0:00) - size S-M, about 45 min

- **App:** on load, `?hospital=cumberland_synthetic` shows a chip on the
  Start screen: "Cumberland General Hospital (SYNTHETIC) selected"; any other
  value is ignored. Nothing else changes (there is one policy).
- **Bill:** a QR code printed on bill-02 ("Scan to check for financial
  assistance - SYNTHETIC demo") encoding the final public URL with the
  parameter; bill-02 PNGs re-rendered.
- **Needs:** a QR generator - either a small MIT JavaScript library vendored
  under app/static/vendor (a download that needs Evan's OK) or one image made
  once and committed. Build after any HTTPS change, because the URL is baked
  into the image.
- **Done-check:** scanning the printed bill with a phone opens the live app
  with the chip shown (Evan, real phone); a test that an unknown parameter
  value shows no chip.

#### F10.5 Partner dashboard - D2a mockup (no code) or D2b live, size M

- **D2a:** no app work; teammates mock it on a slide, labeled "mockup".
- **D2b:** `/dashboard.html` (labeled "Demo dashboard - synthetic data,
  counts since the last restart") reading `GET /stats`:
  - counts kept in server memory under a lock: photos read, results by tier,
    languages chosen, packets made, English fallbacks; any count under 10 is
    shown as "<10" (rev2 rule); no request content, IPs or timestamps kept;
  - "Rules health": each policy rule with its source, page, effective date
    and a `review_by` date added to the policy JSON; red when past.
- **Done-check (D2b):** test_api: counters move after evaluate/packet calls
  and /stats has no field that holds request content; restart clears them;
  the page renders "<10" for small counts.

**Build order and cut order:**
- Order: F10.2 (smallest; F10.1 uses its fields) -> F10.1 -> F10.3 -> F10.4
  -> F10.5 (D2b only).
- Cut first if late: F10.5 -> F10.4 -> the .ics download in F10.3 -> F10.2.
  F10.1 is the one worth the evening; if it is not passing its done-check by
  ~22:00, cut it too and keep the live app as it is.
- Agent split (plan-split rule): server + engine + data + tests to one
  Sonnet agent, app.js/style.css to another (sequential within app.js:
  F10.1 -> F10.3 -> F10.4); D2b's new files can run in parallel. Opus
  reviews each diff on disk and runs the checks before any deploy.

**2026-10-17 19:43 CDT - DEPLOYED (record AH).** F10.1-F10.5 (D2b), R1-R3
and the UI port (record AF) are live at c30be63 on http and https
(HTTPS item done: Let's Encrypt IP certificate). Done-checks passed: tests,
browser checks (record AE/AF), live journeys on both schemes, /household
estimate 883765 with one approval covering all 5 bills. Still open: the
real-phone checks (photo upload, QR scan on bill-02) - Evan.

### F11. DRAFT (2026-10-17 20:30 CDT) - a personal, app-like BillScan (roadmap)

**Status: DRAFT, ROADMAP ONLY - nothing ships before judging (Evan,
2026-10-17 ~20:20).** Written by Claude; scope and answers below come from
four rounds of questions to Evan the same evening. Owner after the
hackathon: undecided (open item O-1). Target user: not decided - kept open
and ready to change (O-2); the design must work for an adult child helping
a parent, a patient alone, and a caseworker (fast reset).

**Rule changes this section proposes (each needs Evan's final OK when it is
built, not now):**
- Hard rule 3 (never ask for a name) -> amended: an OPTIONAL nickname, kept
  only on the phone, never sent to the server, labelled "any word - not your
  real name". Risk named: a name field can still deter people afraid of
  immigration consequences; the field is off the main path (Settings only).
- Hard rule 4 (keep nothing) -> amended: an opt-in "Keep on this phone"
  switch, OFF by default (F11.3).
- "The server keeps nothing" -> amended for push reminders only (F11.7): the
  server keeps a push address and a bill summary until the last reminder.

**Rules for every F11 feature:** F10's rules (synthetic data in every demo;
the engine decides; every number number-locked); new strings hand-written in
en/es/ar/zh-CN/zh-TW and built for the other 27 with scripts/build_i18n.py,
then back-translated (F11.9); safety lines keep the English guard (tSafe);
no new runtime third-party requests; reduced motion respected; works at
375 px in rtl (ar, he).

#### F11.1 Installable app + offline shell - size S
- `manifest.webmanifest` (BillScan, standalone, theme colours from the
  tokens, 192/512 + maskable icons from a new SVG mark).
- Service worker caching ONLY the static shell (html, css, js, fonts, i18n)
  with a commit-versioned cache; offline screen: "Reading a bill needs a
  connection". Never caches API responses. Also ends stale-cache problems
  seen in record AI.
- Done-check: manifest parsed and SW active in the browser; offline reload
  shows the shell; install on Android and iPhone.

#### F11.2 App navigation and subtle motion - size M
- Phones: bottom tab bar Home / Bills / Help; the 5-step stepper only inside
  "Add a bill". Desktop keeps the centred card.
- Motion (Evan: subtle): 150-200 ms slide/fade between screens, a gentle
  reveal of the percent, haptic tick on Android (navigator.vibrate) on
  confirm and result; all off under prefers-reduced-motion.
- Sticky primary action on phones; first-run 3-card intro (what it does /
  what is kept / the hospital decides), skippable.
- Done-check: en + ar + he at 375 and 1280 px, light + dark; reduced-motion
  emulation shows no animation; 0 console errors.

#### F11.3 "Keep on this phone" (opt-in, off by default) - size M
- Off: today's behaviour. On: language, theme, text size, nickname,
  household answers and confirmed bill fields (never the photo) in this
  browser's localStorage only.
- Expiry (Evan): everything deletes itself 30 days after the last bill's
  application deadline; checked on every app start.
- Shared phones (Evan): warning in the switch text ("only on a phone you
  alone use") + one-tap "Delete everything from this phone" on Home and
  Help. No PIN.
- Returning visit: "Welcome back[, nickname]" Home with bills and deadlines.
- Done-check: nothing written while off (storage dump test); on -> reload
  restores; delete -> storage empty; expiry tested with a fixed clock.

#### F11.4 Case tracker + documents checklist - size M
- Per bill: status chips the user sets (Gathering documents / Sent /
  Waiting / Decision received), document check-offs with a progress ring,
  deadline countdown from the engine's deadline (number-locked).
- Home "Next step" card: the single most urgent action across bills.
- Persists only with F11.3 on; otherwise for the visit.
- Done-check: countdown = deadline - today in a test; a status change never
  alters any number or tier.

#### F11.5 Read aloud + text size - size S
- Read aloud with the phone's own speech (speechSynthesis, no network) for
  the explanation and the letter, shown only when the phone has a voice for
  the chosen language.
- Text size A- / A / A+ (100/115/130%), reflow with no sideways scroll.
- Done-check: 130% at 375 px has no sideways scroll; button hidden without a
  voice.

#### F11.6 Share the packet - size S
- Web Share API (phone share sheet) with the packet as a file; desktop:
  Save as PDF via print. BillScan uploads nothing.
- Done-check: share sheet opens on Android and iPhone; desktop falls back.

#### F11.7 Push reminders - size L (Evan chose this over .ics only)
- Opt-in per bill: "Remind me before the deadline". Uses the Web Push API
  with VAPID keys (generated once, private key in OCI Vault); the browser's
  push service delivers (Apple/Google/Mozilla endpoints are the user's own
  browser vendor - note for hard rule 11: these are the browser's requests,
  not a third party the page loads).
- Server stores (Evan): the push subscription + a bill summary (hospital
  name, amount due, deadline) + up to 2 reminder dates, so the text can say
  "Cumberland General: apply by 2027-05-29 ($1,858.50)".
- Where (Evan): a small SQLite file on the existing VM, encrypted at rest
  with a key from OCI Vault; one VM = one point of failure (accepted for a
  pilot). A systemd timer sends due reminders hourly.
- Retention: each row deleted after its last reminder or on "stop
  reminders"; a "delete my reminders" link in every notification.
- RISK, named: with real users this is health-related financial data on a
  server. Before any real user: privacy notice, consent text, Vault-managed
  key rotation, backup policy, and a review of state privacy law. iPhone
  push works only for an installed web app (iOS 16.4+), so F11.1 comes first.
- .ics download stays as the no-account fallback.
- Done-check: subscribe -> row stored encrypted -> reminder delivered on
  Android and an installed iPhone app -> row gone after the last reminder;
  the DB file is unreadable without the Vault key.

#### F11.8 Ask about my result (guarded) - LATER, after F11.1-F11.7
- Answers from a fixed context only (engine result, policy rules, facts),
  canned refusals for medical, legal and other-hospital questions, number
  lock on every answer, a red-team question set that must pass before
  launch. Not a chat tab; a "Questions about this result?" box.

#### F11.9 Translation quality programme
- Evan recruits native-speaker reviewers for as many languages as possible;
  every language without a reviewer gets an automated back-translation check
  of EVERY string (today only 3 safety strings x 26 languages were checked,
  record AI); strings that fail stay English (build_i18n.py DROP).
- Each language shows "Machine translated" or "Reviewed by a native speaker"
  in Settings.

#### F11.10 Success measure (Evan)
- Usability test: 5 people, including 2 non-English speakers, complete "add
  a bill -> packet" unaided on a phone; time to packet and errors recorded
  in experiments.md. Pass bar: 5/5 complete, median under 3 minutes (Claude's
  proposed bar - Evan to confirm).

**Build order (after the hackathon):** F11.1 -> F11.2 -> F11.6 -> F11.5 ->
F11.3 -> F11.4 -> F11.9 (continuous) -> F11.7 -> F11.8.

**Open items:** O-1 owner; O-2 target user; O-3 pass bar for F11.10;
O-4 whether Dipayan's React app becomes the shell for F11.2 (team).
