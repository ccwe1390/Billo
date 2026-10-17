# Research brief - Is the medical bill / EOB decoder space crowded?

> **Status 2026-10-17 16:57 CDT (audit, record Z/AA):** point-in-time brief. Its recommendation fed the
> pivot to "Bill to Help" (record M); the Bill Decoder it evaluates is
> superseded. The "61.0%" figure counts hospitals that post a policy, not
> all 426.

**Date:** 2026-10-17 (12:20-12:32 CDT)
**Question:** Is the space for medical bill / EOB explainer-and-error-checker
tools crowded, and is TNHacks26 Bill Decoder's differentiation (multilingual
for limited-English and low-income patients + family readers; deterministic
bill-vs-EOB error rules; user-sent letters; OCI) real or illusory?
**For:** Evan and team, deciding (a) whether to keep the Bill Decoder idea and
(b) what to claim as differentiation in the pitch.

## TL;DR (revised after the 10.5 cold assessment - see the end of this file)

**Very crowded, and almost every planned feature is already duplicated on
paper.** That includes the measured-accuracy edge we were counting on:
GiveMeMyMoneyBack already reports "caught 19 / 19 planted errors, 0 false
alarms". Source-interest caveat: competitor capabilities come from their own
marketing and Devpost pages, which shows that the claims exist, not that the
features work. The 51 count comes from one platform, and of the prize claims
only ChargeLens's was read.

**What is left for us is narrow:**
- An end-to-end measurement: photo, then OCI extraction, then rules, then
  per-error-type precision/recall. GiveMeMyMoneyBack measured its rules on
  structured cases.
- An integrity-checked translation across 5 languages, including
  right-to-left Arabic. GiveMeMyMoneyBack does Spanish only.

The text below this point is the pre-assessment draft, kept for the record.

**Original TL;DR: Very crowded, and most of our planned differentiation is illusory.**
H2 (hackathon saturation) survived strongly: one search route found 51
patient-facing bill/EOB projects on Devpost, many started Sep-Oct 2026, and
several won prizes (live-corpus reading, 2026-10-17). H0 (differentiation
illusory) mostly survived: every planned feature already exists somewhere.
- Bill-vs-EOB rule checks for our exact error types: Mediloop (commercial),
  plus ChargeLens, Footnote, and GiveMeMyMoneyBack (hackathons).
- Chinese/Vietnamese/Arabic explanations: MedVoice, Footnote (30 languages),
  Care Compass, TL;DR Mail.
- A number-preserving translation check: GiveMeMyMoneyBack, Spanish only.
- User-sent dispute letters: nearly all of them.

H1 survives only narrowly: no production (non-hackathon) tool was found in
Chinese, Vietnamese, or Arabic.

What still looks like ours:
- A published, reproducible accuracy measurement (per-error-type precision
  and recall on seeded planted errors). None of the pages read reported one.
- An integrity-checked translation across 5 languages including
  right-to-left Arabic.

**Recommendation:** keep the idea only if the pitch leads with measured rigor,
not features. Otherwise narrow to the less-crowded financial-assistance-for-LEP
niche (option B below).

## Stage 3 - hypotheses (written 2026-10-17 12:20 CDT, before collection)

- **H1 (expected):** Crowded for English-language consumer bill review,
  but thin for a tool that is (a) multilingual, (b) aimed at limited-English
  / low-income patients, and (c) checks the bill against the EOB with fixed
  rules.
  - *Would be refuted by:* live tools that already do this for zh/ar/vi.
  - **Verdict:** survives only for PRODUCTION tools. At least 4 hackathon
    projects already do (a), and several do (c).
- **H0 (rival):** The differentiation is illusory; our only real edge is
  measured accuracy on planted errors.
  - **Verdict:** mostly SURVIVED (see TL;DR).
- **H2 (hackathon saturation):** "AI medical bill explainer" is a common
  hackathon project.
  - *Would be refuted by:* few projects found by two routes.
  - **Verdict:** SURVIVED strongly. Devpost search and general web search
    both found many.

## Method

Desk research only. Three parallel sub-agents covered (1) commercial and AI
tools, (2) nonprofit/government resources and evidence on the problem, and
(3) prior hackathon and GitHub projects. Claude then re-read the
load-bearing sources' own page text in a browser (`get_page_text` /
in-page JS), not through a summarizing fetch tool.

Limitations:
- No user interviews or surveys. Whether LEP patients would use this is
  untested.
- The event's own rubric and other teams are unknown.
- Many sites returned 403 to the agents.
- Language support was read from product pages. "No language info found"
  does not prove English-only.

Phase effects (2026-10-17):
- 8.5 verify: no verdict flipped. It ADDED one load-bearing competitor
  (MedVoice, 8 languages). The agents had it only as an unverified 403 lead;
  a browser read confirmed it. Re-reading also confirmed that Mediloop's
  error categories match ours.
- 10.5 assess: see the end of this file.

## Findings

### 1. Commercial products overlap our feature set (English, mostly paid)
- **Mediloop:** checks each line "against the bill's own totals, your
  insurer's explanation of benefits". Its example findings are charges dated
  before arrival, a bill higher than the EOB's patient share, arithmetic,
  and duplicates. Those are our error types 5, 2, 6, and 1. A human
  specialist negotiates; $129 per bill. No language info found.
  https://mediloop.ai (read 2026-10-17)
- **Barely Legible (iOS):** explains "hospital itemized statements,
  Explanations of Benefits", verifies totals and adjustments, flags
  duplicates, writes a dispute letter the user sends, and is "AVAILABLE IN
  SPANISH". Only 3 ratings. https://apps.apple.com/app/id6761785810
- **Hedical:** "Any bill or EOB" in; Medicare price comparison and drafted
  letters out. https://www.hedical.online
- Others found by the agents, not re-read by Claude:
  - Appeals and negotiation services: Granted, Sheer Health, Goodbill,
    Resolve, CareRoute, Counterforce, Fight Health Insurance, Claimable.
  - Portal assistants inside hospital and insurer systems: Epic MyChart
    "Emmie", UnitedHealthcare "Avery", Cedar.
- General chatbots: per OpenAI data relayed by Fortune (2026-01-07),
  "1.5 to 2 million health insurance-related messages each week". That is
  vendor-reported and not re-read by Claude.

### 2. Free/nonprofit help is human, not software, and mostly EN/ES
- Dollar For prepares charity-care applications (EN/ES).
- Community Health Advocates (NY) is human, in 8 languages including
  Cantonese and Mandarin.
- CMS's help desk covers "350 other languages" by phone.
- The agents found no free software tool for zh/vi/ar. These items are
  agent-reported and not re-read by Claude.

### 3. Hackathon saturation (the decisive finding)
- One agent route (Devpost JSON search, 13 queries) saw 161 unique results:
  **51 core** bill/EOB projects plus 24 adjacent ones. Claude re-ran one
  query ("medical bill", pages 1-3, 2026-10-17 17:28 UTC): 18 items, about
  12 of them core. That is consistent with the agent's count.
- Read by Claude:
  - **Footnote** (Hack Knight Fall 2026): "reads a US medical bill and its
    insurance EOB with you, checks coded charges against Medicare's national
    rates, and explains them aloud in 30 languages."
  - **GiveMeMyMoneyBack** (OwlHacks 2026): checks the bill "against your
    insurance statement". Its Spanish translation is validated so that
    "every dollar amount, date, code, ID and name is unchanged".
  - **ChargeLens** (IBM x UNSA Hackathon, WINNER Healthcare Track): "PDF
    parsing, deterministic billing rules", plus an IBM Granite explanation.
  - **MedVoice:** bill breakdown, red flags, and an appeal letter in "8
    languages - English, Spanish, Chinese, Vietnamese, Korean, Filipino,
    Arabic, and French".
- Agent-reported, not re-read: Care Compass (5 languages, including zh/ar;
  letters stay in English), TL;DR Mail (EN/ES/VI/ZH/AR), Bill Saathi
  (Hindi/Marathi), and several prize winners (BillClarity, B.A.R.S.,
  ClearClaim, Amyna).

### 4. The problem is real; the famous statistic is not
- KFF (2022 survey): "a majority (53%) of adults with health care debt, and
  43% of all adults, say they have received a medical or dental bill they
  thought contained an error." This is self-report, not audited errors.
  https://www.kff.org/health-costs/could-consumer-assistance-be-helpful-to-people-facing-medical-debt/
- The "80% of bills have errors" figure traces to an advocate, not a study:
  "Pat Palmer, founder of Medical Billing Advocates of America ... contends
  that up to 80 percent of medical bills contain errors." **Do not use it in
  the pitch.**
  https://democracyjournal.org/magazine/40/the-bill-is-too-damn-high/
- Agent-reported, not re-read:
  - AJMC 2026 (426 hospitals): of hospitals posting a financial assistance
    policy, 61.0% translated it into at least one non-English language.
  - Washington test calls (2017): 28% of Spanish-language calls got no
    financial-assistance information; English callers got it 90% of the time.

## Options ranked

| # | Option | Cost | What it buys | Where it breaks |
|---|---|---|---|---|
| A | **Keep Bill Decoder; pitch measured rigor.** Lead with the per-error-type precision/recall table on planted errors, integrity-checked translation in 5 languages including RTL, and store-nothing. | No replanning | Keeps today's PRD; matches the track's "measurable outcome" | Judges may still see "the 52nd bill explainer"; the rigor edge only counts if the rubric values it (rubric MISSING) |
| B | **Narrow to financial assistance (charity care) for LEP patients.** Screen eligibility and prepare the application in zh/vi/ar. | Partial PRD rewrite; needs a fictional hospital policy and income data | A less crowded niche (agent-found competitors are EN/ES only or human-run) | Still several hackathon FA projects (B.A.R.S., MoreTime, BillChill), mostly English |
| C | Pivot to a different Track 2 problem | Lose today's planning | Possibly an uncrowded field | Restarts the grill with unknown dates |

**Recommendation: A.** The track explicitly rewards a "measurable outcome",
and no competitor page read reported one. Make the accuracy table the
headline of the demo, not a footnote. Keep B's financial-assistance check as
the already-planned add-on.

## Verification table (stage 8.5)

| Load-bearing claim | Source | Verdict |
|---|---|---|
| Mediloop checks bill vs EOB, with matching error categories | mediloop.ai | VERIFIED-VERBATIM (browser text) |
| Barely Legible: EOBs, letters, Spanish | App Store listing | VERIFIED-VERBATIM |
| Hedical: "Any bill or EOB" | hedical.online | VERIFIED-VERBATIM |
| MedVoice: 8 languages incl. zh/vi/ar | Devpost | VERIFIED-VERBATIM |
| Footnote: bill + EOB, 30 languages | Devpost | VERIFIED-VERBATIM |
| GiveMeMyMoneyBack: bill vs EOB; number-checked Spanish | Devpost | VERIFIED-VERBATIM |
| ChargeLens: deterministic rules; won Healthcare Track | Devpost | VERIFIED-VERBATIM |
| 51 core Devpost projects | Devpost JSON search (agent) | CLOSE-PARAPHRASE: Claude's partial re-run is consistent (12/18 on 3 pages); full count not re-run |
| KFF 43% / 53% | kff.org | VERIFIED-VERBATIM |
| 80% figure is an advocate claim | Democracy Journal | VERIFIED-VERBATIM |
| No production zh/vi/ar bill tool exists | agent searches + 2 Claude searches (Chinese-language query; English "Vietnamese OR Chinese OR Arabic" query) | NEGATIVE, two routes; both found only hackathon/student projects |

## Numbers register

| Number | Claims | Source | Date | Interest class | Verdict |
|---|---|---|---|---|---|
| 43% / 53% | adults who think they got an erroneous bill (all / with debt) | KFF | 2022-07-14 | INDEPENDENT | VERIFIED-VERBATIM |
| up to 80% | bills with errors | Pat Palmer via Democracy Journal | 2016 | VENDOR-SELF-REPORTED (advocacy firm) | VERIFIED attribution; credibility low |
| 51 core / 161 seen | Devpost bill/EOB projects | agent Devpost search | 2026-10-17 | INDEPENDENT (count); live corpus | CLOSE-PARAPHRASE |
| $378,000+ | Mediloop savings | mediloop.ai | 2026-10-17 | VENDOR-SELF-REPORTED | read on page |
| 8 / 30 | languages (MedVoice / Footnote) | Devpost pages | 2026 | VENDOR-SELF-REPORTED (project claims) | VERIFIED-VERBATIM |
| 1.5-2M/week | insurance-related ChatGPT messages | OpenAI via Fortune | 2026-01-07 | VENDOR-SELF-REPORTED | not re-read |
| 61.0% | hospitals translating their FAP | AJMC (agent) | 2026-06-03 | INDEPENDENT | not re-read |
| 28% vs 90% | Spanish vs English calls getting FA info | The Stranger (agent) | 2017-08-30 | INDEPENDENT (advocacy test) | not re-read |

Structural checks:
- **Interest concentration:** competitor feature claims are self-reported by
  definition; the problem-size numbers are independent.
- **Same-source dependency:** the saturation verdict rests on Devpost only.
  The general-web route agreed, but with fewer hits.

## Thin / missing

- The event's judging rubric and the other TNHacks26 teams: unknown (MISSING).
- Whether any competitor publishes measured accuracy: not seen on the pages
  read, but not checked across all 51. A GitHub repo
  (nmecklenburg/medical-billing-error-detection) is an LLM benchmark for
  disputable bills, agent-reported and unread.
- Evidence that LEP patients have higher billing-error or debt rates: none
  found by language. Proxies only: race/ethnicity, income, and
  immigrant-heavy ZIP codes in one state.
- No peer-reviewed prevalence study of bill errors was found (agent search
  "peer-reviewed study prevalence of billing errors ...").

## What would change this conclusion

- A rubric that does not value measured accuracy -> option A loses its edge.
- Finding that several competitors already publish precision/recall -> no
  remaining differentiation; consider B or C.
- User interviews showing LEP patients would not upload bills to any app
  (trust) -> the whole category weakens for our users.

## Sources (all read 2026-10-17)

mediloop.ai; apps.apple.com/app/id6761785810; hedical.online;
devpost.com/software/medvoice-wzvaj8; devpost.com/software/footnote-hxp1dy;
devpost.com/software/givememymoneyback; devpost.com/software/chargelens;
devpost.com/software/search?query=medical%20bill (pages 1-3);
kff.org (could-consumer-assistance-be-helpful-to-people-facing-medical-debt);
democracyjournal.org/magazine/40/the-bill-is-too-damn-high/. Agent-reported
sources are listed in the agents' reports (not reproduced) and are marked
"not re-read" above.

## Stage 10.5 - cold assessment and the one extra collection round (2026-10-17 ~12:30 CDT)

A fresh agent read only this file. Its main points:
1. **H0 was never given a chance to die.** Nobody checked whether
   competitors publish accuracy metrics, yet the recommendation rested on
   that edge.
2. **Source interest is not disclosed up front.** Competitor claims are
   their own copy; "every feature exists" overstates what 4-7 page reads
   establish. Prize wins other than ChargeLens were not read.
3. **The event rubric is MISSING,** so "pitch rigor" is an assumption, not
   evidence.
4. **Expert gaps:** uninsured and Medicaid patients often have no EOB at all;
   the brief does not address trust or uploading PHI; hackathon judges also
   weigh demo polish and user validation.

**Collection round (fix 1):** Claude fetched 18 Devpost project pages,
covering the prize winners and the closest competitors, with curl and read
their page text. It grepped for precision / recall / F1 / accuracy / test set
/ benchmark / false positive, and also read the
nmecklenburg/medical-billing-error-detection README.

| Source | What it says | Verdict |
|---|---|---|
| devpost.com/software/givememymoneyback | "The rules engine has two independent test sets: Generated cases: caught 19 / 19 planted errors, 0 false alarms, owed amount correct on 18 / 18. Hand-written edge cases ... [8 / 8] correct." Also: "My first test set was generated from the same rules the engine was built on, so of course it passed" | VERIFIED-VERBATIM (page HTML text) |
| devpost.com/software/footnote-hxp1dy | "Measure accuracy on a labeled set of synthetic documents" is listed under "What's next" - planned, not done | VERIFIED-VERBATIM |
| github.com/nmecklenburg/medical-billing-error-detection | Research codebase: clean synthetic bills, planted errors with a "perturbation manifest that is the grading key", models evaluated against it | VERIFIED-VERBATIM (README via gh api) |
| The other 15 pages (BillClarity, B.A.R.S., ClearClaim, Amyna, Guardian, MediAudit, OpenHealth, EquiClaim, ChargeLens, MedVoice, BillBuddy x2, BillChill, Not My Debt, Care Compass, TL;DR Mail) | No precision/recall or planted-error result; "benchmark" hits were price benchmarks | grep, page text |

**Consequences:**
- **H0's remaining edge died.** Measured accuracy on planted errors is not
  unique: one hackathon project already reports it, and a research codebase
  uses the same method.
- **What survives is narrower.** GiveMeMyMoneyBack measured its rules on
  structured inputs, not photo -> OCR -> rules end to end, and checks
  translation for Spanish only. Our planned end-to-end metric across 6 error
  types, with integrity-checked translation in 5 languages including RTL, is
  still not seen elsewhere. That is not proven absent; only these pages were
  read.
- **A design lesson for our own PRD.** Their note is the same trap our plan
  has: test errors planted by the same team that wrote the rules will pass by
  construction. **Add a hand-written edge-case set that the rules author did
  not write.**

**Revised options (supersede the table above):**

| # | Option | Cost | What it buys | Where it breaks |
|---|---|---|---|---|
| A' | Keep Bill Decoder; pitch only the narrow delta: end-to-end photo->OCI->rules accuracy per error type, 5-language integrity-checked translation incl. RTL, store-nothing, LEP focus | No replanning; add an independent edge-case set | Keeps the PRD, Synthea pipeline, and metric design | The core concept matches an existing project (GiveMeMyMoneyBack); judges who know the space see a variant |
| B | Re-center on hospital financial assistance (charity care) for LEP patients in zh/vi/ar, with the error check as secondary | Partial PRD rewrite; fictional hospital policy + income data | Problem evidence is independent (AJMC, Washington calls; agent-reported, not re-read); software competitors found are English or EN/ES | Several English hackathon FA projects exist; problem evidence still needs re-reading |
| C | Different Track 2 problem | Lose today's planning (no code yet, so cheap now) | Possibly uncrowded | Restarts the grill; dates unknown |

Phase effects (2026-10-17):
- **8.5 verify:** added a limitation and added one load-bearing competitor
  (MedVoice). No verdict flipped.
- **10.5 assess:** FLIPPED a verdict. The "measured accuracy is our edge"
  claim died. It also downgraded 3 claims (the 51 count's independence,
  prize wins, "illusory" -> "duplicated on paper") and added one design
  lesson to the PRD.

## Addendum - option B facts verified (2026-10-17 ~12:40 CDT, Evan asked)

Every row below was read by Claude from the page's own text: a browser
`innerText` read, curl HTML stripped to text, or a README via gh api.

| Claim | Source | Verdict |
|---|---|---|
| 501(r)(4) "requires a tax-exempt hospital organization to establish a written financial assistance policy" | irs.gov FAP page (reviewed 28-Dec-2025) | VERIFIED-VERBATIM |
| FAP, application, and plain language summary must be "widely available on a Web site"; billing statements must carry "a conspicuous written notice" | same | VERIFIED-VERBATIM |
| Translation required for each LEP group that is "the lesser of 1,000 individuals or 5 percent of the community served" | same | VERIFIED-VERBATIM |
| For-profit hospitals are not covered by 501(r) | same: the rule names "tax-exempt hospital organization"; CMS: "If you got care elsewhere, they may still offer financial assistance." | VERIFIED by the rule's scope; state law can add more |
| CMS: "Nonprofit hospitals must give financial assistance to eligible patients"; "Ask them to pause collections" | cms.gov apply-financial-assistance (modified 10/05/2026) | VERIFIED-VERBATIM |
| California: 400% FPL | hcai.ca.gov | **CORRECTED.** Eligible to apply "for a hospital's discount payment or charity care program" if uninsured OR high medical costs, AND income "not more than 400 percent of the federal poverty level". It is not a flat 400% charity-care cutoff. |
| AJMC: 213 of hospitals with posted FAPs (61.0%) offered it in a language other than English | ajmc.com (June 3, 2026; 426 nonfederal hospitals in the 10 most linguistically diverse CBSAs) | VERIFIED-VERBATIM. The study does not name which languages. |
| Washington: 28% of Spanish-language calls "failed to elicit any information ... although that information was relayed 90 [percent] of the time to English speakers" | thestranger.com (2017-08-30) | VERIFIED-VERBATIM |
| B.A.R.S. "languages: none stated" (agent claim) | devpost.com/software/bill-bridge | **AGENT WAS WRONG.** The page says a screening "in their preferred language" (no languages named). |
| BillChill: translation only planned | devpost.com/software/billchill | VERIFIED: listed as future work, alongside "Better policy/rules ingestion with citations and thresholds per state/provider" (also future) |
| finecomb (GitHub) screens for charity care | README | VERIFIED: "also screens for charity care and financial assistance" |
| MoreTime | devpost | No language mention in page text |

**Decisive finding - option B is already built and won a prize.** B.A.R.S.
(hackUMBC 2026, "Winner Second Overall" plus a track win) does the following:
- the patient uploads a photo of the bill and completes "a 5-7 question
  screening in their preferred language";
- it starts the financial-assistance application;
- it has a counselor dashboard;
- for an unknown hospital it "finds that hospital's published policy online,
  extracts its rules with page citations, validates them against state law,
  and queues them for an admin to approve";
- its rules engine is built from the real UMMS FAP, with "37 automated
  tests".

So the "policy extraction is unclaimed" claim in Claude's option-B pitch was
FALSE. It rested on a search that never looked for it. B.A.R.S. reports no
extraction-accuracy number and names no languages. B's remaining delta would
be named zh/vi/ar support plus a measured extraction accuracy on
hand-labeled policies: again a variant of a prize winner.

Not done: the Tennessee FAP sample (moot until the direction is chosen).
