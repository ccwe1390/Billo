# decisions - TNHacks26

Standing decisions (what is decided NOW). History lives in the record.

- 2026-10-17 - Track 2, "Health Access, Equity & Experience", is the chosen track.
  Reason: not given. Decided by: the team, as relayed by Evan in chat; team
  membership unknown.
- 2026-10-17 - No problem, user group, or measurable outcome is chosen yet. This is
  the next decision (HANDOFF.md, Next actions).
- 2026-10-17 - Build ONE module: the Bill Decoder (photo or file of a hospital
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
- 2026-10-17 - Mission and scope set (Evan, answers to 6 questions):
  (1) mission is the internal north star first; pitch copy derived later.
  (2) users = limited-English/low-income patients AND the family member who
  reads the bill. (3) wave-1 languages = Spanish, Chinese, Arabic, Vietnamese;
  Hindi is an additional option (Generative AI only, no OCI Language check).
  Supersedes the Hindi-open part of the language entry above. (4) headline
  metric = precision/recall on planted errors in synthetic bills; demo number
  = dollars flagged on the same set; no real-world savings claim.
  (5) financial-assistance check = add-on if time allows. (6) product name =
  placeholder. Mission text lives in HANDOFF.md Goal.
- 2026-10-17 - Two-step flow and sending (Evan picked A+C): step 1 = summary
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
- 2026-10-17 - Stack: TypeScript everywhere - Next.js + the OCI TypeScript
  SDK (Evan picked B). Claude recommended A (Python FastAPI + plain HTML/JS),
  reasons: shortest readable rules engine and accuracy test, fewer moving
  parts, easier for Evan to explain every line. Dissent recorded per Evan's
  disagreement protocol; Evan's call stands. Consequence: hosting must run a
  Node server. Decided by: Evan, chat 2026-10-17.
- 2026-10-17 - Hosting: one OCI Compute VM running the Next.js Node server
  behind a reverse proxy (Evan picked A, matching Claude's recommendation).
  Reasons: possibly $0 under Always Free (unverified), keeps credits for AI
  calls; instance principals may let the VM call AI services with no API key
  on disk (unverified). Rejected: Container Instances (hourly credit burn),
  OKE (overkill), static export + Functions (breaks Next.js server features).
  Decided by: Evan, chat 2026-10-17.
- 2026-10-17 - Synthetic bills: Synthea as the source + our own bill/EOB
  printer and error planter (Evan picked B; Claude had recommended A, our own
  generator). Checked after the pick (Synthea CSV data dictionary): Synthea
  DOES export billing data - claims_transactions.csv has CHARGE / PAYMENT /
  ADJUSTMENT rows with amounts and payer, claims.csv has patient-owed
  (OutstandingP). That corrects Claude's pre-pick claim "its records are
  clinical, not billing" - B is stronger than Claude described. Gaps we fill:
  procedure codes are SNOMED-CT, not CPT/HCPCS, so we map a small code set
  ourselves; Synthea data is clean, so we still plant errors and write the
  answer key. Decided by: Evan, chat 2026-10-17.
- 2026-10-17 - Errors to plant (Evan: "1-6 + 7 stretch", matching Claude's
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
