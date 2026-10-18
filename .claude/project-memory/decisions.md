# decisions - TNHacks26

Standing decisions (what is decided NOW). History lives in the record.

- 2026-10-17 - Track 2, "Health Access, Equity & Experience", is the chosen track.
  Reason: not given. Decided by: the team, as relayed by Evan in chat; team
  membership unknown.
- 2026-10-17 - [SUPERSEDED by the ~13:05 CDT pivot, record M] No problem, user group, or measurable outcome is chosen yet. This is
  the next decision (HANDOFF.md, Next actions).
- 2026-10-17 - [SUPERSEDED by the ~13:05 CDT pivot, record M] Build ONE module: the Bill Decoder (photo or file of a hospital
  bill + EOB -> line-by-line plain explanation, flagged likely errors, drafted
  appeal or itemized-bill request). Discharge Companion and Med nudges are
  dropped for this event. Reason: only module with exact ground truth (we write
  the synthetic bills and inject the errors) and no clinical-risk surface; the
  track says go deep on one problem. Decided by: Evan, chat 2026-10-17.
  Still open: user group/equity hook, metric, scope, rules source.
- 2026-10-17 - Language scope: target the top 10 US immigrant languages; first
  wave Spanish, Chinese, Arabic (Evan). Hindi was in Evan's first wave; open
  question raised: Hindi is not top-ranked for LEP and is not in OCI Language's
  translation list (see languages.md). Ranks 7-10 not yet sourced.
  Decided by: Evan, chat 2026-10-17.
- 2026-10-17 - [PARTLY SUPERSEDED by the pivot, record M: the users and Hindi parts stand; the precision/recall metric and the Bill Decoder scope do not] Mission and scope set (Evan, answers to 6 questions):
  (1) mission is the internal north star first; pitch copy derived later.
  (2) users = limited-English/low-income patients AND the family member who
  reads the bill. (3) wave-1 languages = Spanish, Chinese, Arabic, Vietnamese;
  Hindi is an additional option (Generative AI only, no OCI Language check).
  Supersedes the Hindi-open part of the language entry above. (4) headline
  metric = precision/recall on planted errors in synthetic bills; demo number
  = dollars flagged on the same set; no real-world savings claim.
  (5) financial-assistance check = add-on if time allows. (6) product name =
  placeholder. Mission text lives in HANDOFF.md Goal.
- 2026-10-17 - [SUPERSEDED by the ~13:05 CDT pivot, record M] Two-step flow and sending (Evan picked A+C): step 1 = summary
  bill -> explanation + itemized-bill request letter; step 2 = itemized bill +
  EOB -> line-by-line error flags + appeal letter. The tool never creates an
  itemized bill (only the hospital can). The USER sends letters (mailto
  pre-fill or PDF); the app sends nothing in the product. The demo may "send"
  to a team-controlled fake hospital inbox, labelled as demo. Rejected: app
  sends by email via OCI (would route patient details through our servers,
  breaking "nothing stored"; no public hospital billing-contact directory
  known). Decided by: Evan, chat 2026-10-17.
- 2026-10-17 - The website is hosted on OCI, and translation uses OCI
  (Evan). Read as: OCI Language translates every language it supports (31,
  incl. all of wave 1); Hindi, which OCI Language lacks, falls back to OCI
  Generative AI, which is still OCI (Claude's reading, confirmed by Evan
  2026-10-17). Pipeline consequence: Generative AI writes the plain explanation
  in English, then OCI Language translates it, so the back-translation check
  uses the same service. Specific hosting service not chosen (PRD).
  Decided by: Evan, chat 2026-10-17.
- 2026-10-17 - [SUPERSEDED by the ~13:00 CDT Python entry below] Stack: TypeScript everywhere - Next.js + the OCI TypeScript
  SDK (Evan picked B). Claude recommended A (Python FastAPI + plain HTML/JS),
  reasons: shortest readable rules engine and accuracy test, fewer moving
  parts, easier for Evan to explain every line. Dissent recorded per Evan's
  disagreement protocol; Evan's call stands. Consequence: hosting must run a
  Node server. Decided by: Evan, chat 2026-10-17.
- 2026-10-17 - [PARTLY SUPERSEDED: one OCI VM stands; it runs FastAPI/uvicorn behind Apache, not Next.js] Hosting: one OCI Compute VM running the Next.js Node server
  behind a reverse proxy (Evan picked A, matching Claude's recommendation).
  Reasons: possibly $0 under Always Free (unverified), keeps credits for AI
  calls; instance principals may let the VM call AI services with no API key
  on disk (unverified). Rejected: Container Instances (hourly credit burn),
  OKE (overkill), static export + Functions (breaks Next.js server features).
  Decided by: Evan, chat 2026-10-17.
- 2026-10-17 - [SUPERSEDED by the ~13:05 CDT pivot, record M] Synthetic bills: Synthea as the source + our own bill/EOB
  printer and error planter (Evan picked B; Claude had recommended A, our own
  generator). Checked after the pick (Synthea CSV data dictionary): Synthea
  DOES export billing data - claims_transactions.csv has CHARGE / PAYMENT /
  ADJUSTMENT rows with amounts and payer, claims.csv has patient-owed
  (OutstandingP). That corrects Claude's pre-pick claim "its records are
  clinical, not billing" - B is stronger than Claude described. Gaps we fill:
  procedure codes are SNOMED-CT, not CPT/HCPCS, so we map a small code set
  ourselves; Synthea data is clean, so we still plant errors and write the
  answer key. Decided by: Evan, chat 2026-10-17.
- 2026-10-17 - [SUPERSEDED by the ~13:05 CDT pivot, record M] Errors to plant (Evan: "1-6 + 7 stretch", matching Claude's
  recommendation). Core: (1) duplicate charge; (2) bill patient balance >
  EOB patient responsibility; (3) billed for the contractual adjustment the
  EOB writes off; (4) insurer payment not credited; (5) charge dated outside
  the stay; (6) math error (unit x qty != line, or lines != total).
  Stretch: (7) units above CMS MUE per-code daily limit (MUE table public -
  unverified). Excluded: upcoding (needs clinical judgment, touches
  important.md 1) and unbundling (CPT-based code-pair tables, licensing
  unclear). Every planted error carries a dollar value. Decided by: Evan,
  chat 2026-10-17.
- 2026-10-17 ~13:00 CDT - Stack: Python (FastAPI) backend + plain HTML/JS
  pages, one process on the OCI VM (Evan picked A). SUPERSEDES the morning's
  Next.js + OCI TypeScript SDK decision. New facts since then: about 24 hours
  left; the starter-kit VM ships Python 3.9 (3.12 installable) and Node 16
  (Next.js needs Node >= 20.9); the kit and console GenAI samples are Python;
  the draft plan is written in Python. Arabic PDF risk: use a printable HTML
  page (the browser does RTL shaping), not server-side PDF. Decided by:
  Evan, chat 2026-10-17.
- 2026-10-17 13:36 CDT - Engine review (Agent A build, tests re-run by Opus:
  ALL PASS). Kept: deadline.date, contacts.payment_plan_phone, evaluate
  accepts bare or wrapped fields, every bill field must be confirmed (even
  ones /evaluate ignores). Changed: added tier.discount_percent, and the
  discount percent plus the 240-day window to locked_numbers, so explain text
  that repeats the tier label or deadline text is not flagged. Contacts never
  go through the model; dates in generated text must be YYYY-MM-DD. Decided
  by: Claude (review); open to Evan's override.
- 2026-10-17 ~13:44 CDT - App-shell review (Agent B build; all 3 test files
  re-run by Opus: ALL PASS; fake-mode server served / with 200). Found and
  fixed: /explain and /packet trusted the engine result sent back by the
  browser (a $999,000 income with a client-sent "10%, free care" result got a
  free-care packet). Both now recompute the result with the engine; the
  client's `result` is ignored. Regression test added to tests/test_api.py.
  Accepted from the agent: confidence is null when the model reports none (no
  invented scores); not-eligible gets no packet, only the payment-plan
  contact; model failure or number mismatch falls back to English. Open: OCI
  Language translate never run live; TN protections card has no sourced text;
  es/ar UI strings need a human reviewer. Decided by: Claude (review).
- 2026-10-17 ~13:47 CDT - Team plan rev 2 (mentor additions) adopted WITH
  FIXES; text saved at docs/2026-10-17_HackTN26_Health_Access_Plan_rev2.txt,
  fixes in PRD F9. docs/Hackathon Schedule.txt is ground truth for times
  (1:00 PM finish, 9:00 PM venue close), not rev 2's 12:00/8 PM. Fixes:
  storage wording, QR as "would print", engine-computed $X estimate,
  blur-test before claiming "left it blank", synthetic policy page for
  citations, home page via browser storage after the 5 PM gate, dashboard as
  slide mockup. Decided by: Evan ("adopt with fixes"), chat 2026-10-17.
- 2026-10-17 13:57 CDT - [TIERS REVISED ~14:06 CDT, entry below] Languages: two tiers (Evan chose option 1). Tier 1
  en/es/ar with a translated interface; tier 2 zh-CN, zh-TW, vi, hi with the
  explanation and cover letter in the language and the interface in English.
  Restores Evan's own Wave 1 (languages.md, 2026-10-17), which plan rev 2 had
  silently cut to es/ar - Claude missed that when listing rev 2's issues.
  Every non-English explanation is labeled as AI-written and number-checked;
  Hindi letters use Command A (no OCI Language support), so no back-check.
  Kurdish, Somali, Burmese, Amharic, Nepali: stated as a known gap. Decided
  by: Evan, chat 2026-10-17.
- 2026-10-17 ~14:50 CDT - VM auth to OCI: instance principal (Evan chose A
  over copying his API key). Dynamic group bill-to-help-vm (rule: instances
  in the root compartment) + policy bill-to-help-vm-ai: `use
  generative-ai-family` and `use ai-service-language-family` in tenancy.
  `use` proved enough for chat and batch translation (live 14:53). No
  credentials on the server. Code: OCI_AUTH=instance_principal in
  oci_client._auth(). Decided by: Evan, chat 2026-10-17.
- 2026-10-17 ~15:23 CDT - UI design: build "Paper Trail" (brief Direction 1)
  on the existing vanilla JS, not Dipayan's React branch. Tier rows come
  from the engine (option A, not a hard-coded copy in app.js, so a VUMC
  policy swap can never show another hospital's table). Assets vendored,
  never loaded from a CDN at runtime. 21:00 go/no-go; result: GO at 15:40.
  Dipayan's feature/frontend branch stays unmerged; only its ideas (named
  loading steps, hard UI rules) were ported. Decided by: Evan, chat
  2026-10-17.
- 2026-10-17 ~16:05 CDT - Translated letters: the hospital name is
  protected like numbers; if it does not survive translation the packet
  falls back to English (fail closed). Hindi is exempt from the name check
  (its Command A path has no placeholders, so the check would make every
  Hindi packet fall back) - proposed by the coding agent, accepted by Opus.
  Letter wording changed to "apply for financial assistance". Decided by:
  Evan (fix all six), details by Claude.
- 2026-10-17 ~13:05 CDT (entry added 16:50 by the audit fix) - PIVOT: the Bill
  Decoder is replaced by "Bill to Help" (bill photo -> that hospital's
  financial assistance packet). Decided by Evan (record M; PRD CURRENT
  DIRECTION). Entries above marked SUPERSEDED belong to the Bill Decoder.
- 2026-10-17 ~14:06 CDT (entry added 16:50) - Language tiers revised: tier 1
  (translated interface) en, es, ar, zh-CN, zh-TW; tier 2 (English interface,
  translated explanation and letter) vi, fr, ko, ru, de, hi. Commit c5f04a9,
  record T. Supersedes the tier lists in the 13:57 entry.
- 2026-10-17 16:50 CDT - Audit fixes (Evan: "fix all", record Z/AA). Claude's
  recommended options were applied: (A2) a bill naming another hospital gets
  the estimate WITH a "different hospital" warning and a "uses the policy of"
  line, not a refusal; (A3) text fields <= 200 chars, known field names only,
  income <= 10^12 cents, 40 paid requests per 60 s per client IP (429),
  generous so a shared venue IP is not blocked; the packet's `back_checked`
  flag is replaced by `translator` (no back-translation exists); Hindi uses
  the same {n} placeholders, so the hospital-name check now covers every
  language (supersedes the 16:05 Hindi exemption); uploads stay in memory
  (multipart spool limit above 8 MB). Not done: a project LICENSE (Evan's
  legal call), TLS (needs a domain), filling the pitch brackets (needs the V1
  results). Pitch fixes: docs/2026-10-17_pitch-corrections.md (draft).
- 2026-10-17 ~18:35 CDT - F10 approved by Evan (PRD F10): D1a (Dad's bills
  = seeded synthetic bills, nothing saved), D2b (live dashboard of in-memory
  counts, no personal data), HTTPS included (Let's Encrypt IP certificate,
  agreement accepted with no email, approved ~18:31), QR via the vendored
  qrcode-generator 2.0.4 (download approved), product renamed "BillScan".
  Built on branch f10; NOTHING deploys until Evan says go. Dipayan's React
  PR #1 is out of scope; which UI teammates demo is undecided (Evan).
- 2026-10-17 ~19:00 CDT - UI design (Evan, record AF): Dipayan's design
  system is ported into the vanilla app, not adopted as a React app. Hybrid
  theme: his dark palette = our dark theme, a matching light theme, the
  phone's setting picks (in-memory toggle, no storage). Atkinson Hyperlegible
  vendored (download approved). Web Awesome dropped from all pages (Claude's
  call; two cascades + a dark theme). PR #1 stays open; its fate is the
  team's call.
