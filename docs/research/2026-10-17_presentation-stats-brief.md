# Customer base and pitch statistics (research-stats)

> Raw subagent report, saved verbatim (non-ASCII transliterated) on 2026-10-17.
> Not yet reviewed or cold-assessed by the orchestrator; numbers are as the agent reported them.
> Source transcript agent id: a62af8f4cab871774

# Research brief: Customer base, and the statistics to put in the pitch

**Date:** 2026-10-17, 23:22-23:50 CDT (timestamps from `date`; UTC-5, so CDT)
**Question:** Who are BillScan's users, how big is the problem, and which numbers best support the pitch?
**For:** Evan and the teammates presenting at TNHacks26 on Sun 2026-10-18 (Track 2). The judges include Oracle executives, Vanderbilt faculty, an HCA application-services director and an internist. The decision this feeds: which numbers go on the slides and in the spoken pitch, and which come off.
**Prior work read (stage 2, treated as claims under test, not facts):** docs/research/2026-10-17_bill-decoder-crowding.md, docs/2026-10-17_pitch-corrections.md (its "numbers nobody has re-opened" list: 29%, 52%, $14B, 2,984, 95,000, $7B, 175%, 24%, 9.3%, 282,294), .claude/project-memory/compliance.md, and the stats lines of docs/2026-10-17_HackTN26_Health_Access_Plan_rev2.txt.

## TL;DR

The debt, language and coverage numbers are strong, independent and recent. They come from KFF, Census, CBPP, Commonwealth Fund and AJMC, and every one below was read on the source's own page. **The weak spot is the pitch's headline charity-care gap ("only 29% get it", "52% never told", "$14 billion").** All three trace to one interested source: Dollar For, a nonprofit that files these applications. Its survey method is not published on the page, and two Dollar For accounts give different sample sizes (over 1,600 vs. more than 1,100). The $14B is Dollar For's own doubling of a $7B figure built from hospitals' self-reported tax filings. The only independent support for the direction is old (KFF Health News 2019, $2.7B, built on the same self-reported filings). No peer-reviewed estimate of charity-care uptake was found by two search routes.

So H1 survives for debt, LEP and coverage, and H0 survives for the charity-care gap: say "Dollar For's survey found..." out loud and never present it as an established fact.

Three pitch numbers are out of date or wrong:
- "95,000 in the coverage gap" -> now 91,000 (CBPP, updated 2026-03-19, 2024 data).
- "9.3% of Tennesseans uninsured" -> 2023 data; 2024 ACS gives 9.7%.
- A web claim that Tennessee banned medical debt from credit reports in 2025 is false. The bill stalled, and Tennessee is not on NCLC's 2026-09-21 list of 15 states plus DC.

## Stage 3 hypotheses (written 2026-10-17 ~23:25 CDT, before deep collection)

- **H1 (expected):** Strong, verifiable customer-base numbers exist for medical debt (KFF ~20M) and LEP (~25M+). The "eligible but not receiving charity care" gap is supported by independent sources, not only Dollar For.
  - *Refuted if:* the gap numbers trace only to Dollar For, or the debt/LEP numbers can't be re-read.
  - **Verdict:** split. Debt, LEP and coverage: SURVIVED. Charity-care gap independence: DIED.
- **H0 (rival):** The charity-care gap numbers rest on one interested source, and the evidence linking LEP to billing problems is thin.
  - **Verdict:** SURVIVED. 29%/52%/$14B/$7B are all Dollar For. No study measuring LEP bill comprehension or LEP charity-care uptake was found (two searches, plus the prior brief).
- **H2:** The popular "headline" stats (66.5% medical bankruptcies, "80% of bills have errors") don't survive scrutiny.
  - **Verdict:** SURVIVED. See "Stats to NOT use".

## Method

**Design.** Desk research only. Primary or near-primary sources: KFF, Census (CPS report P60-291; ACS 2024 1-year via the Census Reporter API), CBPP, Commonwealth Fund, AARP/NAC, IRS, AHA, CFPB, NCLC, AJMC, NEJM via PMC, the Tennessee General Assembly bill site, and Dollar For's own pages. Each load-bearing number was found with WebSearch, then re-read on the page's own text in the browser pane (in-page text/JS reads or get_page_text). That second read is what earns VERIFIED-VERBATIM.

**Limitations.**
- No user interviews. Whether LEP families or caregivers would use BillScan is untested; a human would need to run intercept interviews at a Nashville clinic or community organization.
- Several primary PDFs (Dollar For "Bridging the Chasm" and "Path" reports, the AARP CGUS 2025 full report) use CID-encoded fonts. Neither WebFetch nor a stdlib extractor could read them, and I did not install a PDF library. Their method sections are UNREACHABLE.
- Blocked or unusable: Pew Research (bot check, not bypassed), data.census.gov (virtualized grid), the Census API (now requires a key), the Urban Institute debt map (hung).
- 2025 ACS state-level estimates were not retrieved.

**Side effects.** One browser navigation to the Dollar For PDF made the pane show the user a file-save dialog; I did not save anything. WebFetch auto-cached three PDFs in Claude's own tool-results folder, outside the repo. No repo files were written.

**Phase effects (2026-10-17):**
- 8.5 verify: changed two numbers (95,000 -> 91,000; 9.3% -> 9.7%). Caught one NOT-FOUND, confirmed on the official bill page: the Tennessee credit-reporting ban claim is false. Added two limitations: Dollar For's sample-size conflict and unpublished method, and the same-source dependency between $2.7B, $7B and $14B. Downgraded one wording ("52% never told" -> "52% got no information from their hospital").
- 10.5 assess: skipped per the orchestrator (one cold assessment will cover both briefs). -> RUN 2026-10-18 00:08-00:12 CDT by fresh agents; findings and effects in docs/research/2026-10-18_cold-assessments.md (brief text not yet changed)

## Findings

### 1. Medical debt (the problem's size)
- **KFF/Peterson (2024-02-12), SIPP data as of Dec 2021:** "20 million people (nearly 1 in 12 adults) owe medical debt" over $250; "at least $220 billion in medical debt"; about 3 million owe more than $10,000. Most likely to have it: people with disabilities or in worse health, lower-income people, and uninsured people. [healthsystemtracker.org]. FLAG: the underlying data is older than 2022.
- **KFF (Health Care Debt Survey, Feb-Mar 2022; restated in a brief updated 2026-09-29):** "41% of U.S. adults currently have some type of debt due to medical or dental bills". This is a broad definition that includes credit cards and family loans. It includes 24% with bills past due or unpayable. The same 2026 update says "about three in ten (28%) adults" skipped or postponed needed care in the past 12 months because of cost. [kff.org]
- **Credit reporting status (as of Oct 2026):**
  - The CFPB's Jan 2025 rule removing medical bills from credit reports was vacated on 2025-07-11 (Cornerstone Credit Union League v. CFPB, E.D. Tex.). The CFPB's own archived page states this, last modified 2026-06-25.
  - NCLC (updated 2026-09-21) says the decision vacates the rule nationwide and bars a similar CFPB rule. Its other points: "About 15 million consumers have medical debt on their credit reports". Only the bureaus' voluntary 2022-2023 limits remain nationally (no reporting under $500, nothing until one year delinquent, paid debt removed). 15 states plus DC restrict reporting, and Tennessee is not among them.
  - Tennessee HB539/SB402 (a reporting ban): the official bill history shows HB539 last assigned to a House subcommittee on 2025-02-05. SB402 was last re-assigned to a Senate subcommittee on 2026-01-20. No enactment.

### 2. Charity care: eligible but not enrolled
- **Dollar For, "The Path to Charity Care" (survey "In late 2023"; page read 2026-10-17):**
  - "only 29% of patients with hospital bills they cannot afford are able to learn about, apply for, and receive financial assistance."
  - "51% of those who are potentially eligible do not apply."
  - "Most patients (52%) did not report receiving information about financial assistance from their hospital."
  - Approval is 67% when patients get help; 45% of applicants get no help.
  - The most common denial reasons are bill age (28%) and paperwork (24%).
  - Method caveats: sample size, recruitment and weighting are not on the page, and the PDF was unreadable. ClearHealthCosts (2024-05-14) quotes the report as "Surveying over 1,600 patients". The An Arm and a Leg/KFF Health News transcript (2024-12-05) says Dollar For "hired a firm to survey a sample of more than 11 hundred people". The conflict is unresolved.
- **Dollar For, "Bridging the Chasm" (PDF dated 2024-04-29), as quoted verbatim by ClearHealthCosts:**
  - "approximately $7 billion per year in charity care eligible amounts end up as bad debt."
  - Maryland data "suggests that hospitals self-report less than half... so the actual amount is likely twice that number". That doubling is the $14B.
- **Independent but old (KFF Health News, 2019-10-14):** 1,134 nonprofit hospital organizations (1,651 hospitals) self-reported $2.7B in bills to patients who probably qualified. "45% of nonprofit hospital organizations are routinely sending medical bills" to such patients. FLAG: older than 2022, and it uses the same Schedule H self-reports that Dollar For extrapolates (see the same-source check below).
- **Legal obligation (IRS; 501(r)(4) page reviewed 2026-07-03):**
  - "Section 501(r)(4) requires a hospital organization to establish a written financial assistance policy (FAP)".
  - The FAP must be translated for each LEP group that is "the lesser of 1,000 individuals or 5 percent of the community served".
  - 501(r)(6) requires "reasonable efforts to determine whether an individual is eligible... before engaging in extraordinary collection actions". It also refers to "the 240 day application period" and a 120-day wait after the first post-discharge statement.
- **How many hospitals (AHA Fast Facts 2026):** "Number of Nongovernment Not-for-Profit Community Hospitals 2,984". Caveat: 501(r) covers tax-exempt hospital organizations, so 2,984 approximates the covered count rather than equalling it. Some government hospitals also hold 501(c)(3) status.
- **Business-model signal (relevant to judge Q7, "who pays").** Dollar For spent a year trying to get hospitals to refer patients to it. In the 2024-12-05 transcript, its founder answers whether hospitals signed up: "Um, well they haven't". This is single-source, but it is direct evidence that hospitals don't readily pay for this.

### 3. Limited English proficiency (LEP)
- **ACS 2024 1-year, table B06007, via the Census Reporter API (raw values; I computed the sums):**
  - US: 18,432,220 Spanish speakers plus 10,486,527 other-language speakers who speak English less than "very well" = **~28.9M, 9.0% of people aged 5+**. The total, 321,745,950, matches data.census.gov S1601's 321,745,943 to rounding.
  - Tennessee: **~272,000 (4.0%)**.
  - Davidson County: **~74,900 (11.0%)**.
- **Top LEP languages (C16001, same release):**
  - Tennessee: Spanish 189,781, then Arabic 17,760, then Vietnamese 7,727 and Chinese 6,471 (both after two "other" groups).
  - Davidson: Spanish 50,928, then "other/unspecified" 7,094, then Arabic 5,814, then Vietnamese 2,401.
  - Caveat: county-by-language 1-year estimates have wide margins of error, which I did not pull.
- **KFF (2024-05-16; survey June-Aug 2023):**
  - "about 26 million people who have limited English proficiency". This is an older ACS base than the 28.9M above.
  - Languages: Spanish 62%, Chinese 7%, Vietnamese 3%, Arabic 2%.
  - Income: nearly 1 in 5 have income below 200% FPL, vs. 1 in 10 English-proficient people.
  - Health: fair/poor health is 34% for LEP adults vs. 19% for English-proficient adults.
  - Forms: "about a third of LEP adults" said English difficulty "made it hard for them to fill out forms for a health care provider (34%)".
- **AJMC (2026-06-03; 426 nonfederal hospitals in the 10 most linguistically diverse metros):** "Of the hospitals with posted FAPs, 136 (39.0%) offered this policy only in English". Nashville is not one of the 10 metros, so this is not a Tennessee number.
- **Negative (searched twice):** no study measuring LEP patients' bill comprehension, LEP charity-care uptake, or LEP medical-debt rates was found.

### 4. Uninsured and underinsured
- **US (Census P60-291, 2026-09-15, CPS):** "In 2025, 26.7 million people (7.9 percent) were uninsured for the entire year".
- **Tennessee, ACS 2024 (B27010 via Census Reporter):** 690,683 uninsured, 9.69% (US 8.20%, same table). Davidson County: 12.57%. America's Health Rankings independently lists Tennessee at 9.7% for 2024 (search snippet only).
- **Medicaid expansion (KFF table, "Timeframe: October 2026"):** "Tennessee Not Adopted"; 41 states including DC adopted, 10 did not.
- **Coverage gap (CBPP, updated 2026-03-19, 2024 ACS):** Tennessee has 91,000 uninsured adults "Currently in Coverage Gap", 84,000 eligible for marketplace tax credits, and 174,000 who would be newly eligible under expansion. The superseded 2025-04-10 version said 86,000. CBPP is an advocacy-leaning think tank, pro-expansion.
- **Coverage is shrinking in 2026 (KFF, 2026-06-29):** marketplace enrollment "dropped 13% following the expiration of enhanced premium tax credits", from 22.1M (2025) to 19.2M (Feb 2026).
- **Underinsured (Commonwealth Fund, 2024-11-21; fielded Mar-Jun 2024; ages 19-64):** "23 percent were underinsured". 57% of underinsured adults avoided care because of cost, and 44% were paying off medical or dental debt.

### 5. Bill errors and confusion
- **Commonwealth Fund (2024-08-01; fielded 2023):** "Forty-five percent of insured, working-age adults reported receiving a medical bill or being charged a copayment in the past year for a service they thought should have been free or covered". "Less than half... challenged them". Lack of awareness of the right to challenge was the top reason. Note: these are *perceived* errors.
- **KFF (2022):** 43% of all adults and 53% of adults with health care debt say they got a bill they think was wrong. VERIFIED-VERBATIM in the prior brief; not re-read in this one.
- **No credible audited "share of bills with errors" exists.** The "80%" figure is an advocate's claim (prior brief).

### 6. Family caregivers
- **AARP/NAC, Caregiving in the US 2025 (2025-07-24):** 63 million family caregivers, "a nearly 50% increase since 2015". "a quarter are taking on debt due to caregiving". "Half report negative financial impact".
- **MISSING:** a verified share of caregivers who handle a parent's bills or insurance. The full AARP PDF was unreadable, and Pew 2025/2026 was bot-blocked. A search snippet attributes "31%... managing finances" to Pew (parents 65+ needing help), but it was not re-read, so do not use it.

## Customer base (interpretation, kept separate from the findings)

**Users:**
- (a) Low-income uninsured or underinsured patients holding hospital bills. The 20M with significant medical debt is the outer bound, and the 91,000 Tennessee coverage-gap adults are the sharpest local slice.
- (b) LEP families: ~29M US, ~75,000 in Davidson County, mostly Spanish then Arabic. KFF's 34% "hard to fill out forms" is the cleanest link to BillScan's packet feature.
- (c) Adult children handling a parent's bills: 63M caregivers exist, but the share doing bills is unverified.

**Buyers (if any):** the ~2,984 nonprofit hospitals legally required to have, translate and screen against an FAP. Dollar For's failed hospital-partnership push is a counter-signal.

## Top 8 slide-ready stats (VERIFIED-VERBATIM unless noted)

1. 20 million US adults owe over $250 in medical debt, at least $220 billion in total (KFF, 2024; data from 2021).
2. 41% of US adults have some debt from medical or dental bills (KFF Health Care Debt Survey, 2022).
3. Dollar For's survey: only 29% of patients with hospital bills they can't afford learn about, apply for, and receive financial assistance; 52% got no information from their hospital (Dollar For, late-2023 survey; interested source, method unpublished: say "Dollar For found").
4. Nonprofit hospitals must have a written financial assistance policy and must make reasonable efforts to check eligibility before extraordinary collections (IRS 501(r)); there are 2,984 nonprofit community hospitals (AHA Fast Facts 2026).
5. About 29 million people in the US (9% of age 5+) speak English less than very well; in Davidson County it is ~75,000 (11%), mostly Spanish, with Arabic the next-largest named language (Census ACS 2024; totals computed from the table).
6. 34% of adults with limited English say language made it hard to fill out forms for a health care provider (KFF, 2024).
7. Tennessee has not expanded Medicaid; 91,000 uninsured adults are in the coverage gap; 9.7% of Tennesseans were uninsured (KFF Oct 2026; CBPP 2026 using 2024 data; ACS 2024).
8. 45% of insured working-age adults got a bill they thought insurance should have covered, and fewer than half challenged it (Commonwealth Fund, 2024).

Alternates: 26.7M uninsured nationally, 7.9% (Census, Sept 2026). 39% of hospitals in the 10 most linguistically diverse metros that post an FAP post it in English only (AJMC, 2026). 63M family caregivers (AARP/NAC, 2025).

## Stats to NOT use (or only with the stated fix)

- **"66.5% of bankruptcies are medical" (Himmelstein et al., AJPH 2019).** These are self-reported contributing causes. Dobkin et al. (NEJM 2018-03-22, read on PMC) estimate "hospitalizations cause only 4% of personal bankruptcies among nonelderly U.S. adults". It is a live academic dispute that a Vanderbilt judge may know. Avoid it, and avoid "530,000 medical bankruptcies a year" (not checked; same lineage).
- **"80% of medical bills contain errors."** An advocate's claim with no study behind it (prior brief).
- **"100 million Americans have medical debt."** A KFF Health News headline using a broad definition (credit cards, family loans). Use KFF's "41% of adults" with its definition instead.
- **"$14 billion a year undelivered" and "$7 billion bad debt" as facts.** These are Dollar For extrapolations from hospitals' self-reported Schedule H filings. The $14B is a doubling based on Maryland data. Only say "Dollar For estimates...", and keep it off the market-size slide (rev2 already says not to show a dollar market total).
- **"More than half say their hospital never told them."** The source says 52% "did not report receiving information". Say "52% got no information from their hospital".
- **"95,000 uninsured adults in the coverage gap"** (CBPP 2024 fact sheet). Superseded: use 91,000 (CBPP 2026-03-19, 2024 data).
- **"9.3% of Tennesseans uninsured"** (Sycamore, 2023 data). Superseded: use 9.7% (ACS 2024).
- **"24% of Tennesseans have medical debt on their credit report"** (Sycamore 2019, 2016 data). Stale, and it predates the 2023 bureau changes that dropped debts under $500.
- **"Tennessee bans medical debt from credit reports (2025)"** (CareRoute). False: HB539/SB402 were never enacted.
- **"The CFPB rule removes $49B of medical debt from 15M credit reports."** The rule was vacated 2025-07-11. Never present it as current protection.
- **KFF Health News "$2.7B / 45% of hospital organizations" (2019).** Usable only as history, labeled 2019.
- **Lown Institute "$25.7B fair-share deficit"** (2021 data). Its method is disputed by the AHA, and it was not re-read.
- **Not checked in this brief, still unverified from the pitch list:** Tennessee "175% of cost" cap (search snippet only, the court PDF was blocked), VUMC "24% of charges", TennCare "282,294 renewals".

## Verification table (load-bearing claims)

| Claim | Source | Verdict |
|---|---|---|
| 20M adults >$250 medical debt; >=$220B | healthsystemtracker.org, 2024-02-12 | VERIFIED-VERBATIM |
| 41% of adults have health care debt (2022) | kff.org "Americans' Challenges...", updated 2026-09-29 | VERIFIED-VERBATIM |
| CFPB medical debt rule vacated 2025-07-11 | consumerfinance.gov archive page; NCLC 2026-09-21 (two independent reads) | VERIFIED-VERBATIM |
| TN not among states restricting reporting; TN bill not enacted | NCLC list; wapp.capitol.tn.gov HB0539 | VERIFIED-VERBATIM (absence confirmed on two sources) |
| 29% / 51% / 52% | dollarfor.org/the-path-to-charity-care | VERIFIED-VERBATIM (method UNREACHABLE) |
| Survey of "over 1,600" patients | ClearHealthCosts quoting report, 2024-05-14 | VERIFIED-VERBATIM; CONTRADICTED by "more than 11 hundred" (news-medical.net transcript, 2024-12-05) |
| $7B, doubled to $14B | ClearHealthCosts quoting report | VERIFIED-VERBATIM (as Dollar For's claim) |
| $2.7B; 45% of organizations (2019) | kffhealthnews.org 2019-10-14 | VERIFIED-VERBATIM |
| 501(r)(4) FAP; LEP translation threshold; 501(r)(6) reasonable efforts, 240 days | irs.gov (two pages) | VERIFIED-VERBATIM |
| 2,984 nonprofit community hospitals | aha.org Fast Facts 2026 | VERIFIED-VERBATIM |
| ~28.9M LEP (9.0%); TN 272K; Davidson 74.9K | Census Reporter API, ACS 2024 B06007 (raw) | VERIFIED raw values; sums COMPUTED |
| Davidson top LEP languages Spanish, Arabic | Census Reporter API, C16001 | VERIFIED raw values |
| 26M LEP; 34% forms; 34% vs 19% fair/poor | kff.org 2024-05-16 | VERIFIED-VERBATIM |
| 39.0% English-only FAPs | ajmc.com 2026-06-03 | VERIFIED-VERBATIM |
| 26.7M (7.9%) uninsured 2025 | census.gov P60-291, 2026-09-15 | VERIFIED-VERBATIM |
| TN 9.69% uninsured (2024) | Census Reporter B27010 (raw), computed | VERIFIED raw; corroborated by AHR 9.7% (snippet) |
| TN Not Adopted, Oct 2026 | kff.org state indicator | VERIFIED-VERBATIM |
| TN 91,000 in coverage gap | cbpp.org, updated 2026-03-19 | VERIFIED-VERBATIM |
| Marketplace enrollment -13% | kff.org 2026-06-29 | VERIFIED-VERBATIM |
| 23% underinsured | commonwealthfund.org 2024-11-21 | VERIFIED-VERBATIM |
| 45% got a bill they thought should be covered | commonwealthfund.org 2024-08-01 | VERIFIED-VERBATIM |
| 63M caregivers; a quarter taking on debt | aarp.org PRI page 2025-07-24 | VERIFIED-VERBATIM |
| Hospitalizations cause 4% of bankruptcies | PMC5865642 (NEJM 2018) | VERIFIED-VERBATIM |
| Dollar For hospitals "haven't" signed up | news-medical.net transcript 2024-12-05 | VERIFIED-VERBATIM (fragment; the page later failed to re-render) |

## Numbers register

| Number | Claim | Source | Date | Interest class | Verdict |
|---|---|---|---|---|---|
| 20M / $220B / 3M | adults with >$250 / total / >$10K medical debt | KFF-Peterson (SIPP) | pub 2024-02-12; data Dec 2021 (FLAG: pre-2022 data) | INDEPENDENT | VERIFIED-VERBATIM |
| 41% / 24% | adults with health care debt / past-due or unpayable | KFF | survey Feb-Mar 2022 | INDEPENDENT | VERIFIED-VERBATIM |
| 28% | skipped or postponed care for cost, past 12 months | KFF | brief updated 2026-09-29 | INDEPENDENT | VERIFIED-VERBATIM |
| ~15M | consumers with medical debt on credit reports | NCLC | 2026-09-21 | ADVERSARIAL (consumer advocate; intervenor in the case) | VERIFIED-VERBATIM |
| 15 + DC | states restricting medical debt reporting (TN not listed) | NCLC | 2026-09-21 | ADVERSARIAL | VERIFIED-VERBATIM |
| 29% / 51% / 52% | get charity care / eligible don't apply / no info from hospital | Dollar For | survey late 2023 | VENDOR-SELF-REPORTED (service provider) | VERIFIED-VERBATIM; method unknown |
| 1,600+ vs 1,100+ | survey sample | Dollar For via ClearHealthCosts vs podcast | 2024 | VENDOR-SELF-REPORTED | CONFLICT |
| 67% / 45% | approval with help / applicants with no help | Dollar For | late 2023 | VENDOR-SELF-REPORTED (and self-promoting) | VERIFIED-VERBATIM |
| $7B / $14B | eligible bad debt / doubled estimate | Dollar For | 2024-04 | VENDOR-SELF-REPORTED | VERIFIED-VERBATIM as a claim |
| $2.7B / 45% / 1,134 orgs | self-reported bills to likely-eligible / share of orgs | KFF Health News | 2019-10-14 (FLAG: pre-2022) | INDEPENDENT (journalism on self-reports) | VERIFIED-VERBATIM |
| 2,984 | nonprofit community hospitals | AHA | 2026 | INDEPENDENT count (trade group) | VERIFIED-VERBATIM |
| 1,000 or 5% | FAP translation threshold | IRS | page reviewed 2026-07-03 | INDEPENDENT (regulator) | VERIFIED-VERBATIM |
| 240 / 120 days | application period / wait before ECAs | IRS 501(r)(6) | current page | INDEPENDENT | VERIFIED-VERBATIM |
| 28.9M (9.0%) | US LEP age 5+ | Census ACS 2024 1-yr via Census Reporter | 2024 data | INDEPENDENT | raw VERIFIED; sum COMPUTED |
| 272,039 (4.0%) | Tennessee LEP | same | 2024 | INDEPENDENT | raw VERIFIED; COMPUTED |
| 74,941 (11.0%) | Davidson County LEP | same | 2024 | INDEPENDENT | raw VERIFIED; COMPUTED; MOE not pulled |
| 50,928 / 5,814 | Davidson LEP Spanish / Arabic | ACS C16001 | 2024 | INDEPENDENT | raw VERIFIED; MOE not pulled |
| 26M / 8% | US LEP | KFF | 2024-05-16 | INDEPENDENT | VERIFIED-VERBATIM |
| 34% | LEP adults: hard to fill out provider forms | KFF survey | June-Aug 2023 | INDEPENDENT | VERIFIED-VERBATIM |
| 34% vs 19% | fair/poor health, LEP vs English-proficient | KFF | 2023 survey | INDEPENDENT | VERIFIED-VERBATIM |
| 39.0% (136 of 349) | FAP posted in English only | AJMC | 2026-06-03 | INDEPENDENT (peer-reviewed) | VERIFIED-VERBATIM |
| 26.7M / 7.9% | US uninsured all of 2025 | Census CPS P60-291 | 2026-09-15 | INDEPENDENT | VERIFIED-VERBATIM |
| 9.69% / 690,683 | TN uninsured | ACS 2024 B27010 | 2024 | INDEPENDENT | raw VERIFIED; COMPUTED |
| 12.57% | Davidson County uninsured | same | 2024 | INDEPENDENT | raw VERIFIED; COMPUTED |
| 91,000 / 174,000 | TN coverage gap / total expansion-eligible | CBPP | updated 2026-03-19 (2024 ACS) | INDEPENDENT, advocacy-leaning | VERIFIED-VERBATIM |
| 41 / 10 | states adopted / not adopted expansion | KFF | Oct 2026 | INDEPENDENT | VERIFIED-VERBATIM |
| 13%; 22.1M -> 19.2M | marketplace enrollment drop | KFF citing ASPE | 2026-06-29 | INDEPENDENT | VERIFIED-VERBATIM |
| 23% / 57% / 44% | underinsured / avoided care / paying debt | Commonwealth Fund | 2024-11-21 | INDEPENDENT | VERIFIED-VERBATIM |
| 45% | insured workers billed for something they thought was covered | Commonwealth Fund | 2024-08-01 (fielded 2023) | INDEPENDENT | VERIFIED-VERBATIM |
| 43% / 53% | think they got an erroneous bill | KFF | 2022 | INDEPENDENT | VERIFIED-VERBATIM (prior brief only) |
| 63M; 1/4 debt; 1/2 negative financial impact | family caregivers | AARP/NAC | 2025-07-24 | INDEPENDENT (advocacy org) | VERIFIED-VERBATIM |
| 31% | parents needing help with finances | Pew (via search) | 2025 | INDEPENDENT | UNREACHABLE (bot check); do not use |
| 4% | bankruptcies caused by hospitalization | Dobkin et al., NEJM | 2018-03-22 (FLAG: pre-2022) | INDEPENDENT | VERIFIED-VERBATIM |
| 66.5% | bankruptcies with a medical contributor | Himmelstein et al., AJPH | 2019 (FLAG) | ADVERSARIAL (single-payer advocates) | search snippet only |
| 24% / $739 | TN medical debt on credit reports | Sycamore | 2019 pub, 2016 data (FLAG) | INDEPENDENT | VERIFIED-VERBATIM; stale |
| 175% of cost | TN uninsured charge cap | court filing via search | n/a | INDEPENDENT | UNVERIFIED (PDF blocked) |

**Structural checks:**
1. **Same-source dependency.** The 29%, 51%, 52%, $7B and $14B all come from Dollar For. The "independent" $2.7B (KFF Health News 2019) and Dollar For's $7B both rest on the same input, hospitals' self-reported Schedule H bad-debt figures, so they rise and fall together. Separately, Dollar For's 67% approval-with-help number praises Dollar For's own service.
2. **Interest concentration.** Of the ~25 load-bearing numbers, 6 are VENDOR-SELF-REPORTED, all from Dollar For. That is under half overall, but it is 100% of the charity-care-gap numbers, which carry the pitch's opening hook. That is why it is in the TL;DR.

## Thin / missing

- **No peer-reviewed or government estimate of the share of eligible patients who receive charity care.** Searches: "peer-reviewed study share of patients eligible for hospital financial assistance who apply OR receive" (extended); "presumptive eligibility JAMA Health Forum charity care uptake"; "Bai Zare charity care eligible bad debt". The nearest items are a 25-interview gyn-onc paper and a PAN/Harris familiarity poll (21% "extremely or very familiar"), neither re-read.
- **No study of LEP patients' bill comprehension, LEP charity-care uptake, or LEP medical-debt rates.** Two searches here, plus the prior brief.
- **No verified share of caregivers who handle a parent's bills or insurance.** The AARP PDF was unreadable and Pew was blocked.
- **No current Tennessee or Nashville medical-debt-in-collections rate.** The Urban Institute map hung, and Sycamore's figure is 2016.
- **No 2025 ACS state uninsured rate for Tennessee** (Census Reporter API does not yet support acs2025).
- **No Tennessee-specific FAP-translation audit.** AJMC covered 10 metros that exclude Nashville.

## What would change this conclusion

- Dollar For's methodology appendix, read from a text-readable copy. If the sample was its own clients or followers, the 29% describes Dollar For's audience, not "patients"; if it was a weighted panel from a survey firm, the number strengthens.
- Any independent uptake estimate, such as Maryland HSCRC data, a state AG audit or a CFPB study. That would upgrade or replace the 29%.
- The full AARP CGUS 2025 table on managing finances. That would let the caregiver persona carry a number.
- Davidson County ACS margins of error, which could make the Arabic-vs-other ranking not statistically distinguishable.

## Sources (all read 2026-10-17 unless noted)

- KFF-Peterson, "The burden of medical debt in the United States", 2024-02-12. https://www.healthsystemtracker.org/brief/the-burden-of-medical-debt-in-the-united-states/
- KFF, "Americans' Challenges with Health Care Costs", updated 2026-09-29. https://www.kff.org/health-costs/americans-challenges-with-health-care-costs/
- KFF, "Health Care Debt in the U.S.", 2022-06-16. https://www.kff.org/health-costs/report/kff-health-care-debt-survey/
- CFPB archived newsroom page (rule vacatur note), modified 2026-06-25. https://www.consumerfinance.gov/archive/newsroom/cfpb-finalizes-rule-to-remove-medical-bills-from-credit-reports/
- NCLC, "The Latest on Keeping Medical Debt Out of Credit Reports", updated 2026-09-21. https://library.nclc.org/article/latest-keeping-medical-debt-out-credit-reports
- Tennessee General Assembly, HB0539/SB0402 bill history. https://wapp.capitol.tn.gov/apps/BillInfo/Default.aspx?BillNumber=HB0539&GA=114
- Dollar For, "The Path to Charity Care" (survey late 2023). https://dollarfor.org/the-path-to-charity-care/ ; report PDFs (unreadable) https://dollarfor.org/wp-content/uploads/2024/04/Dollar_For_Path.pdf and https://dollarfor.org/wp-content/uploads/2024/04/Dollar_For.Bridging_the_Chasm.pdf
- ClearHealthCosts, 2024-05-14. https://clearhealthcosts.com/blog/2024/05/looking-for-hospital-financial-aid-good-luck-and-dont-hold-your-breath/
- An Arm and a Leg / KFF Health News transcript via News-Medical, 2024-12-05. https://www.news-medical.net/news/20241205/An-Arm-and-a-Leg-New-lessons-in-the-fight-for-charity-care.aspx
- KFF Health News, "Patients Eligible For Charity Care Instead Get Big Bills", 2019-10-14. https://kffhealthnews.org/health-care-costs/patients-eligible-for-charity-care-instead-get-big-bills/
- IRS 501(r)(4), reviewed 2026-07-03. https://www.irs.gov/charities-non-profits/financial-assistance-policy-and-emergency-medical-care-policy-section-501r4 ; IRS 501(r)(6) https://www.irs.gov/charities-non-profits/billing-and-collections-section-501r6
- AHA, Fast Facts on U.S. Hospitals 2026. https://www.aha.org/statistics/fast-facts-us-hospitals
- Census Reporter API, ACS 2024 1-year: B06007 and C16001 for US, TN and Davidson. https://api.censusreporter.org/1.0/data/show/latest?table_ids=B06007&geo_ids=01000US,04000US47,05000US47037 ; B27010 https://api.censusreporter.org/1.0/data/show/acs2024_1yr?table_ids=B27010&geo_ids=01000US,04000US47,05000US47037
- KFF, "Language Barriers in Health Care", 2024-05-16. https://www.kff.org/racial-equity-and-health-policy/language-barriers-in-health-care-findings-from-the-kff-survey-on-racism-discrimination-and-health/
- AJMC, "Availability of Hospital Financial Assistance Documents in Non-English Languages", 2026-06-03. https://www.ajmc.com/view/availability-of-hospital-financial-assistance-documents-in-non-english-languages
- Census, P60-291 "Health Insurance Coverage in the United States: 2025", 2026-09-15. https://www.census.gov/library/publications/2026/demo/p60-291.html
- KFF, Status of State Medicaid Expansion (Timeframe Oct 2026). https://www.kff.org/affordable-care-act/state-indicator/state-activity-around-expanding-medicaid-under-the-affordable-care-act/
- CBPP, "Nearly 3 Million Uninsured Adults Would Gain a Path to Medicaid Coverage...", updated 2026-03-19. https://www.cbpp.org/research/health/nearly-3-million-uninsured-adults-would-gain-a-path-to-medicaid-coverage-if-their ; prior version 2025-04-10 https://www.cbpp.org/research/health/closing-medicaid-coverage-gap-would-provide-over-15-million-uninsured-adults-path
- KFF, "ACA Marketplace Enrollment Is Down By 3 Million...", 2026-06-29. https://www.kff.org/quick-insights/aca-marketplace-enrollment-is-down-by-3-million-after-big-jump-in-premium-payments/
- Commonwealth Fund, 2024 Biennial Survey, 2024-11-21. https://www.commonwealthfund.org/publications/surveys/2024/nov/state-health-insurance-coverage-us-2024-biennial-survey
- Commonwealth Fund, "Unforeseen Health Care Bills and Coverage Denials", 2024-08-01. https://www.commonwealthfund.org/publications/issue-briefs/2024/aug/unforeseen-health-care-bills-coverage-denials-by-insurers
- AARP/NAC, Caregiving in the US 2025, 2025-07-24. https://www.aarp.org/pri/topics/ltss/family-caregiving/caregiving-in-the-us-2025/
- Dobkin et al., "Myth and Measurement: The Case of Medical Bankruptcies", NEJM 2018-03-22. https://pmc.ncbi.nlm.nih.gov/articles/PMC5865642/
- Sycamore Institute, "Medical Debt in Tennessee", 2019-05-08. https://sycamoretn.org/medical-debt-tennessee/
- Unreachable or not re-read: Pew Research 2026-02-26 (bot check); Urban Institute Debt in America map (hung); data.census.gov S1601 (virtualized grid); Census API (key required); Tennessee court PDF for the 175% cap (browser validation).

---
**Note for the orchestrator:** no files were written. The brief is ASCII-only by construction, but I did not run the skill's grep check because no file was written; run `grep -nP '[^\x00-\x7F]'` on the saved file. Stage 10.5 was skipped as instructed. The business-model signal (Dollar For's hospitals "haven't" signed up) bears on pitch judge answer Q7 and the "hospitals pay per completed application" line.
