# Sustainability: funding evidence, hospital WTP, regulation (research-money-2)

> Raw subagent report, saved verbatim (non-ASCII transliterated) on 2026-10-17.
> Not yet reviewed or cold-assessed by the orchestrator; numbers are as the agent reported them.
> Source transcript agent id: a13982e8fad2da35e

Evan - research-money supplement (ASCII markdown, ready to merge). No sub-agents spawned, no files written. Stage 10.5 skipped as you instructed. Access date for every source: 2026-10-17 (CDT, UTC-05:00). One side effect: navigating the browser pane to an oregon.gov PDF made the pane show a save dialog. I downloaded nothing through it. Dismiss the dialog if it is still open.

## TL;DR (verdict first)

- **H2 (grants/philanthropy) survived. H1 (B2B SaaS to nonprofit hospitals) mostly died as BillScan is built today.**
- The closest comparable lives almost entirely on donations:
  - Dollar For, FY2025: 96.8% contributions, $1.46M revenue, 18 employees, $0 government grants.
  - Undue Medical Debt, FY2025: 97.8% contributions/grants, and about half of that is government money ($31.4M).
- **Hospitals do pay for screening, but they buy something different from what BillScan does.**
  - They buy presumptive-charity scoring from incumbents (Experian, Waystar), priced in tiers per transaction. No public price was found.
  - They buy it to move bad debt into charity, which raises reported community benefit and supports 501(r) compliance.
  - Federal 501(r) does not require presumptive screening. It is one of two "reasonable efforts" paths.
  - In the one state with independent evidence (Oregon), hospitals' pain was giving financial assistance to too many people. They lobbied the screening threshold up from $500 to $1,500 (HB 4040, 2026). A patient-side tool that raises uptake works against the paying buyer's interest.
- **H5 (government) came back partly alive.** Cities and states pay Undue (for example NYC, $6M per year). LA County (HASC, L.A. Care, DPH) ran 2025 RFPs to buy presumptive-eligibility income data and a portal.
- **Interest concentration.** Most load-bearing financial numbers are self-reported IRS filings (attested, but self-reported). The hospital-side willingness-to-pay evidence rests mainly on one state, Oregon. Both belong up front.

## Method (2-3 lines)

- Primary sources first: ProPublica 990 full text (browser text = verbatim), eCFR, NCLC docket page, CMS fact sheet, company IR pages and help pages, an OHA state report (PDF read directly), hospital 990 Schedule H.
- Secondary sources only for statutes I could not reach. Justia's Cloudflare challenge blocked the Tennessee code; I did not bypass it.
- Limitations: no primary data. No hospital CFO interviews and no vendor price quotes; those are the methods that would settle H1.
- Phase effects (2026-10-17):
  - 8.5 verify: caught one source error (Orrick says "Northern District of Texas"; the NCLC docket shows E.D. Tex., No. 4:25-cv-00016-SDJ). Downgraded 1 claim (Tennessee "175% of cost" cap -> UNVERIFIED). Replaced two stale search-summary numbers with newer 990s (Dollar For FY2025 instead of FY2024; Undue FY2025 instead of FY2021).
  - 10.5 assess: skipped per orchestrator instruction.

## 1. Comparables' funding

**Dollar For (EIN 46-0889864), FY ending Dec 2025, Form 990 filed 2026-05-14. Read verbatim from the ProPublica full text.**

| Item | 2025 | 2024 |
|---|---|---|
| Total revenue | $1,460,202 | $1,678,080 |
| Contributions and grants | $1,413,942 (96.8%) | $1,659,194 |
| Government grants (line 1e) | blank (none reported) | - |
| Program service revenue ("PROGRAM SERVICE REVENUE", source unspecified) | $25,000 | $0 |
| Total expenses | $1,644,067 | $1,391,750 |
| Net | -$183,865 | - |
| Program expenses | $1,333,666 (81.1%) | - |
| Fundraising | $141,230 | - |
| Salaries and benefits | $1,055,521 | $619,489 |
| Employees (W-3) | 18 | - |

- Self-reported outcomes: "HELPED 18,000 PATIENTS APPLY FOR HOSPITAL FINANCIAL ASSISTANCE" and "CRUSHED 55 MILLION IN MEDICAL DEBT".
- Derived: about $91 total expense per patient helped ($1,644,067 / 18,000). That is my arithmetic, not a filed number.
- Growth: revenue $113,798 (2016) -> $326,382 (2021) -> $913,227 (2022) -> $1,211,241 (2023) -> $1,678,080 (2024) -> $1,460,202 (2025). The first decline came in 2025.
- Known funders (secondary, not re-verified):
  - Draper Richards Kaplan Foundation: $300,000 over 3 years (Chronicle of Philanthropy, 2022).
  - CauseIQ lists Greater Houston Community Foundation $260,000 and FFWD $137,928 (2023 filings).
- No evidence that hospitals pay Dollar For. The search returned none, and the hospital partner page found says it is free to patients.

**Undue Medical Debt (legal name Medical Debt Resolution Inc, EIN 47-1442997), FY ending Dec 2025, Form 990 filed 2026-07-31. Verbatim, ProPublica full text.**

| Item | 2025 | 2024 |
|---|---|---|
| Total revenue | $62,529,512 | $92,580,019 |
| Government grants (line 1e) | $31,420,501 (50.2% of revenue) | - |
| All other contributions (line 1f) | $29,728,988 | - |
| Total contributions | $61,149,489 (97.8%) | - |
| Noncash contributions (included above) | $10,016,202 | - |
| Program service revenue | $0 | - |
| Investment income | $1,414,424 | - |
| Total functional expenses | $62,916,819 | $33,118,125 |
| Program expenses | $57,163,541 (90.9%) | - |
| Salaries and benefits | $6,071,690 | $3,990,904 |
| Employees | 53 | - |

- Self-reported outcomes: "HELPED OVER 6.5 MILLION PEOPLE AND RELIEVED MORE THAN $9.9 BILLION OF MEDICAL DEBT".
- The model is debt purchase, not application help. It is a different mechanism from BillScan.

**For-profit patient-side services (vendor self-reported prices, read verbatim on their own pages):**
- **Goodbill:** 20% of savings, capped at $1,000. No fee unless a settlement is reached. Hospital bills only (CareRoute comparison page, secondary).
- **Resolve:** It does not serve bills under $5K.

  | Bill size | Deposit | Success fee |
  |---|---|---|
  | $5-15K | $250 | 20% of savings |
  | $15-200K | $499 | 8% of savings |
  | Over $200K | $499 | 8% or less |

  - "Minimum total fee of $800" on the lower tiers; $2,000 minimum on the top tier.
  - Self-reported: "average of 60%" and "Total Patient Savings to Date: $55,235,678".
- **CareRoute (Healtheja, Inc.):** percentage of savings with a $1,000 hard cap, $0 upfront. Triage and estimate tools are free. Search summary only, not opened in the browser.
- **Implication:** consumer contingency fees only pencil out on large bills. Charity-care-eligible patients with small bills are exactly who these services leave out. That is the gap Dollar For fills with philanthropy.

**Patient-financial-engagement / RCM vendors (how hospitals pay):**
- **Waystar** (FY2025 release, 2026-02-17, verbatim):
  - Revenue $1,099.3M.
  - Subscription revenue $558.4M (+22%) and volume-based revenue $534.8M (+11%). So hospitals pay about half subscription, half per-volume.
  - 1,391 clients over $100K in LTM revenue; NRR 112%.
- **Flywire FY2025 10-K** (WebFetch partial read): "more than 150 healthcare systems". Revenue $623.0M. The excerpt read gives no healthcare revenue split or take rate.
- **Cedar:** private. No primary pricing found. Third-party write-ups only (subscription plus % of collections), so treat as UNVERIFIABLE. Premier group-purchasing agreement (2022) with undisclosed pricing.

## 2. What hospitals spend on presumptive screening

- **No published per-account or per-contract price was found** from Experian, Waystar, TransUnion or Optum. Searches that produced this negative are in the thin/missing list.
- **Pricing structure (CLOSE-PARAPHRASE, WebFetch):** Trinity Health's revenue-cycle partner (Emily Huizenga, Healthrise; HFMA, 2025-12-16) described "tiered-based, per transaction" pricing.
  - Setup "could be cost prohibitive".
  - At Trinity's volume, the per-transaction cost is "actually quite low".
- **Waystar / Atrium Health case study** (vendor PDF, (c) 2018, read verbatim):
  - "Charity reclassification increase by $75M annually"; in-house collections +$4.6M; early-out +$3.4M; bad-debt vendor performance +$3M.
  - The stated purpose: reclassify "millions of dollars to charity that otherwise would have gone to bad debt - helping with both 501(r) compliance and to further exhibit the significant amount of community benefit". VENDOR-SELF-REPORTED.
- **Experian / UCHealth:** case-study title claims a $26M charity write-off. Vendor blog, not opened.
- **Oregon Health Authority, "Hospital Feedback on the First Quarter Implementation of HB 3320 Financial Assistance Prescreening", January 2025** (PDF read directly; INDEPENDENT state agency, relaying hospital views):
  - OHA met with 34 hospitals.
  - "Hospitals use two third-party vendor tools to prescreen for FA eligibility: Experian and Waystar."
  - The tools use no tax returns or confirmed income.
  - Most hospitals estimated about 85% accuracy and complained of OVER-awarding assistance and "significant lost hospital revenue".
  - One small hospital estimated 3.5 FTE to run prescreening.
  - Hospitals doing front-end work (asking patients household and income questions) reported better results. "One hospital that does not use a software tool reported smooth implementation", using information patients chose to provide. But "Most hospitals have expressed that collecting front end information is too administratively burdensome."
- **Buyer-side procurement exists:** HASC with L.A. Care and LA County DPH issued a "bulk purchasing options for income estimation/verification" RFP (issued 2025-10-24, due 2025-11-14, contract target 2026-02-20; verbatim on hasc.org) plus a separate portal RFP (due 2025-12-12). No award or price found.

## 3. Hospital economics

- **AHA:** latest annual uncompensated care figure found is $42.67B (2020, community hospitals); "almost $745 billion" since 2000 (fact sheet dated February 2022). No AHA figure for 2021 or later was found. CLOSE-PARAPHRASE.
- **KFF** (2023-03-14, revised 2023-03-27; verbatim):
  - Value of tax exemption about $28B (revised from $27.6B to $28.1B) vs charity care costs of $16B among nonprofit hospitals in 2020.
  - Exemption value grew from about $19B (2011).
  - No newer KFF edition was found.
- **Lown Institute** (verbatim from project page; ADVERSARIAL to hospitals, funded by Arnold Ventures):
  - April 2025 report: "54% of nonprofit hospitals spent less on community investment than their tax exemption"; deficit "$11.5 billion per year" across 20 states.
  - AHA disputes the method (secondary).
  - Lown 2021 list put VUMC among the 10 largest fair-share deficits at -$157M (2021 release, older data).
- **VUMC (EIN 35-2528741), Schedule H, ProPublica "TY 2024" = FYE June 2025** (verbatim):

  | Item | Amount |
  |---|---|
  | Revenue | $8,674,383,028 |
  | Financial Assistance at cost | $233,093,209 (2.818% of total expense) |
  | Medicaid net benefit | $36,186,276 |
  | Bad debt expense | $17,259,145 |
  | Bad debt attributable to FAP-eligible patients | $4,050,175 |

  - VUMC states that unpaid accounts "are first reviewed under a presumptive charity policy". A large Nashville nonprofit already runs presumptive screening.
- **Ascension Saint Thomas:** the main acute hospitals' filer EIN was not found.
  - EIN 58-1716804 (FYE June 2025, revenue $109.7M) covers behavioral, rehab and LTAC facilities only. Its Financial Assistance at cost is $314,910 (0.248%) and bad debt $950,390. Not representative of Saint Thomas West/Midtown.
- **HCA (for-profit, no 501(r) duty):** "charity care, uninsured discounts and other uncompensated care at an estimated cost of approximately $4.5 billion in 2025" (verbatim, HCA site, company-wide).
  - Policy: 100% write-off for emergency care under 200% FPG; out-of-pocket capped at 4% of income for 200-400% FPG.
- **Oregon (Lund Report, 2026-02-24, WebFetch):**
  - OHSU memo estimated the 2023 law adds at least $50M per year in costs.
  - OHSU charity care went from about $73M (2021) to over $165M (2025).
  - These are hospital-sourced figures (ADVERSARIAL to the mandate).

## 4. Regulation status as of 2026-10-17

- **CFPB medical-debt credit-reporting rule** (90 Fed. Reg. 3276, 2025-01-14): **VACATED 2025-07-11** by consent judgment.
  - Court: E.D. Tex., Cornerstone Credit Union League v. CFPB, No. 4:25-cv-00016-SDJ.
  - The CFPB joined the plaintiffs on 2025-04-30. NCLC-represented intervenors objected.
  - The NCLC page reads "Resolved Case"; no appeal was found.
  - Orrick InfoBytes (2025-07-18) wrongly says "Northern District". The court name was corrected from the NCLC docket.
  - Per NCLC (secondary), 15 state medical-debt credit-reporting laws are unaffected.
- **CMS price transparency:** CY2026 OPPS final rule (CMS-1834-FC; fact sheet 2025-11-21).
  - New requirements: median and 10th/90th percentile allowed amounts, named attester, Type 2 NPI. Effective 2026-01-01; enforcement delayed to 2026-04-01.
  - CMP cut 35% if a hospital waives its ALJ hearing (not for core violations).
  - CY2027 OPPS proposed rule (2026-07-02) adds only a price-transparency RFI per the summaries.
- **IRS 26 CFR 1.501(r)-6** (eCFR, current to 2026-10-15, verbatim):
  - "(c)(1)... reasonable efforts... only if the hospital facility meets the requirements described in paragraph (c)(2) or (c)(3)".
  - (c)(2) "Presumptive FAP-eligibility determinations based on third-party information or prior FAP-eligibility determinations" is OPTIONAL. It is one safe-harbor path; notification under (c)(3) is the other.
  - Where a patient is presumed eligible for less than the most generous tier, the hospital must notify, give time to apply, and process a full application.
- **States with screening/presumptive mandates (verified level varies):**
  - **Oregon:** HB 3320 (2023, ORS 442.615). Prescreening began 2024-07-01 for uninsured, Medicaid, or owing over $500. HB 4040 (2026) is enrolled as Chapter 109 and raises the threshold to $1,500 per encounter (OLIS via WebFetch; OHA rulemaking hearing 2026-06-17).
  - **California:** AB 1312, Ch. 450, Stats. 2025, chaptered 2025-10-07. Presumptive eligibility for CalFresh/CalWORKs/WIC etc. enrollees takes effect 2027-07-01 (search summary citing HCAI PIL 25-01; not opened).
  - **Colorado:** HB21-1198. Must screen each uninsured patient unless they decline; eligibility up to 250% FPG (search summary of the HCPF manual).
  - **Maryland:** presumptive eligibility since 2020 (secondary).
  - **Illinois:** HB 2719 = P.A. 103-0323 (2023-07-28). Final presumptive text not confirmed.
  - **Washington:** HB 1616 (Ch. 197, Laws 2022) expanded charity care. Presumptive language not confirmed.
  - **Six-state list (CA, DE, IL, MD, NC, OR):** KFF Health News, via a secondary republication only.
  - **New York:** not found.
- **Tennessee:** TCA 68-11-262, "Limit on amount of charges for services to an uninsured patient", cited verbatim in the UT Medical Center policy (revised 2024-12-02).
  - The cap value ("175% of cost") comes only from careroute.ai and is UNVERIFIED.
  - Fowler v. Morristown-Hamblen: no private right of action (secondary).
  - **No Tennessee charity-care screening or presumptive mandate was found.**

## 5. Funders

- **Community Foundation of Middle Tennessee:** 2025 Community Impact Grants. 95 grants, "averaged $21,000 in unrestricted support" (verbatim).
  - Focus areas: Arts $485K, Positive Mental Health $725K, Child/Youth $810K. **No health-access or medical-debt category.**
- **HCA Healthcare Foundation:** "$2.1 million in grants to 89 nonprofit organizations across Middle Tennessee" (TriStar release 2026-06-24, verbatim). Average about $23.6K (my arithmetic).
  - Also $1.84M to Mile High United Way including United Way of Greater Nashville (2025-03-25, secondary).
- **BlueCross BlueShield of Tennessee Foundation:** 2025 Healthy Place projects just over $10M (parks, not access).
  - An aggregator claims a median grant of $10K across 217 grants totaling $20.5M. UNVERIFIABLE.
- **RWJF:** $2.4M to Community Catalyst for hospital financial-assistance work and $190,000 to Georgia Watch (secondary, 2022-era). No 2024-2026 award found.
- **Arnold Ventures:** $1.5M over 2 years to Lown for hospital tax-exemption and policy database work (Lown release, not opened). No direct-service grants found.
- **Draper Richards Kaplan:** $300K over 3 years to Dollar For (secondary, 2022).
- **Government as funder:** Undue $31.4M in 2025 (verbatim, 990).
  - NYC contract $6M per year for 3 years; New Jersey about $500K ARPA per round; Delaware $500K; Connecticut $6.5M ARPA (government pages via search summary, not opened).
- **Commonwealth Fund, Healthier Tennessee:** no grant program or size found.

## Numbers register

Interest classes: IND = INDEPENDENT; VSR = VENDOR-SELF-REPORTED (990 = an attested IRS filing, still self-reported); ADV = ADVERSARIAL; UNV = UNVERIFIABLE. Verdicts: VV = VERIFIED-VERBATIM; CP = CLOSE-PARAPHRASE; UNVERIFIED = search summary only.

| Number | Claim | Source | Date | Class | Verdict |
|---|---|---|---|---|---|
| $1,460,202 | Dollar For revenue FY2025 | ProPublica 990 | filed 2026-05-14 | VSR (990) | VV, 2 calls |
| $1,413,942 / 96.8% | Dollar For contributions share | same | same | VSR (990) | VV |
| $25,000 | Dollar For program service revenue | same | same | VSR (990) | VV |
| $1,644,067 | Dollar For expenses (program $1,333,666) | same | same | VSR (990) | VV |
| 18 | Dollar For employees | same | same | VSR (990) | VV |
| 18,000 / $55M | Patients helped / debt relieved, Dollar For | same, Part III | same | VSR | VV (claim not audited) |
| $62,529,512 | Undue revenue FY2025 | ProPublica | filed 2026-07-31 | VSR (990) | VV, 2 calls |
| $31,420,501 | Undue government grants | 990 Part VIII 1e | same | VSR (990) | VV |
| $57,163,541 | Undue program expenses | 990 Part IX | same | VSR (990) | VV |
| 53 | Undue employees | 990 | same | VSR (990) | VV |
| 6.5M / $9.9B | Undue people helped / debt relieved | 990 Part III | same | VSR | VV (claim not audited) |
| 20%, $1,000 cap | Goodbill fee | help.goodbill.com | undated, accessed 2026-10-17 | VSR | VV |
| $250 + 20%; $499 + 8%; $800 min | Resolve fees | resolvemedicalbills.com/partners/konnectmd | same | VSR | VV |
| $1,099.3M; $558.4M; $534.8M | Waystar FY2025 revenue / subscription / volume | Waystar IR | 2026-02-17 | VSR | VV |
| 150+ | Flywire healthcare systems | 10-K FY2025 | 2026 | VSR | CP |
| $75M/yr | Atrium charity reclassification | Waystar case study | (c) 2018 | VSR | VV |
| 85% | Hospital-estimated accuracy of prescreening tools | OHA report | 2025-01 | IND (relaying hospitals) | VV |
| 34 | Hospitals interviewed | OHA | same | IND | VV |
| 3.5 FTE | Prescreening staff, one small hospital | OHA | same | ADV (hospital) | VV |
| $500 -> $1,500 | Oregon screening threshold (HB 4040, Ch. 109) | OLIS + Lund Report + OHA rule notice | 2026 | IND | CP |
| $50M/yr | OHSU-estimated cost of the Oregon law | Lund Report citing OHSU memo | 2026-02-24 | ADV | CP |
| $42.67B | AHA uncompensated care, 2020 | AHA fact sheet | 2022-02 | ADV (trade group) | CP |
| $28.1B vs $16B | Tax-exemption value vs charity care, 2020 | KFF | 2023-03-27 rev. | IND | VV |
| $11.5B; 54% | Lown fair-share deficit, 20 states | Lown | 2025-04 | ADV | VV |
| -$157M | VUMC fair-share deficit | Lown 2021 release | 2021-07-11 | ADV | VV |
| $233,093,209; 2.818% | VUMC financial assistance at cost | VUMC 990 Sch H | FYE 2025-06 | VSR (990) | VV |
| $17,259,145 / $4,050,175 | VUMC bad debt / FAP-eligible share | same | same | VSR (990) | VV |
| $314,910 | Saint Thomas Health (non-acute) FA at cost | 990 Sch H | FYE 2025-06 | VSR (990) | VV |
| ~$4.5B | HCA charity + uninsured + other uncompensated, 2025 | HCA website | data as of 2025-12-31 | VSR | VV |
| 2025-07-11 | CFPB rule vacated | NCLC + Orrick | 2025 | IND (NCLC is an intervenor) | VV, 2 sources |
| 2026-04-01 | CMS enforcement start for new transparency requirements | CMS fact sheet | 2025-11-21 | IND | CP |
| 35% | CMP reduction for ALJ waiver | CMS fact sheet | same | IND | CP |
| 2027-07-01 | CA AB 1312 presumptive screening start | HCAI PIL via search | 2025-10 | IND | UNVERIFIED |
| 250% FPG | CO HB21-1198 eligibility | HCPF manual via search | 2024-25 | IND | UNVERIFIED |
| 175% of cost | TN uninsured charge cap | careroute.ai | 2026 | VSR / UNV | UNVERIFIED |
| $21,000 avg | CFMT 2025 grant size | cfmt.org | 2025 | IND | VV |
| $2.1M / 89 | HCA Foundation Middle Tennessee grants | TriStar | 2026-06-24 | VSR | VV |
| $300K / 3 yrs | DRK grant to Dollar For | Chronicle of Philanthropy via search | 2022 | IND | UNVERIFIED |
| $2.4M | RWJF to Community Catalyst | Chronicle via search | 2022 | IND | UNVERIFIED |
| $6M/yr x 3 | NYC contract with Undue | NYC Council page via search | 2025-03 | IND | UNVERIFIED |
| Nov 14 / Dec 12, 2025 | LA HASC presumptive-eligibility RFP due dates | hasc.org | 2025-10-22 | IND | VV (bulk); portal UNVERIFIED |

**Structural checks:**
1. **Same-source dependency.** The case against H1 (hospitals' pain is over-awarding; they lobby to shrink screening; vendors are inaccurate) rests on Oregon. The OHA report, Lund Report and HB 4040 are one state's single episode wearing three hats. It is not national evidence.
2. **Interest concentration.** About 60% of load-bearing numbers are self-reported: 990s (attested filings) plus vendor pages. The only fully independent load-bearing numbers are KFF, the CMS/eCFR regulatory text, and the OHA report. Put this in the TL;DR.

## Verdict on the hypotheses

- **H1 (B2B SaaS to nonprofit hospitals): mostly dead for a patient-side screener. A narrow variant is untested.**
  - Willingness to pay exists, but it is for incumbent data products already wired into Epic and bought to (a) shift bad debt to charity for community-benefit reporting and (b) satisfy a 501(r) safe harbor that is optional.
  - Where states mandate screening, the hospital buyer wants fewer false positives and less staff time. A tool that maximizes patient uptake is the opposite.
  - Tennessee has no mandate, and VUMC already runs a presumptive charity policy.
  - Surviving variant: patient-attested, front-end household and income intake as an accuracy check, in mandate states (OR, CA from 2027-07-01, CO, MD). OHA says front-end work helped. No price evidence exists, and most hospitals call front-end collection "too administratively burdensome".
- **H2 (grants/philanthropy): survived.** It is the only proven funding path for free patient-side charity-care help.
  - The scale ceiling is real: Dollar For needs about $1.5M per year for 18 staff and 18,000 patients.
  - Local Tennessee grants average about $21-24K and are not aimed at medical debt.
  - National funders back policy and advocacy orgs (Community Catalyst, Lown) more than new tools.
- **H3 (licensing to PFE/EHR vendors): no evidence for or against.** Incumbents already have presumptive products (Waystar acquired PARO in 2019). Untested.
- **H4 (Dollar For-style nonprofit): viable in principle, but crowded.** Dollar For is national, free, and doing the same job. Collaboration (its 2025 990 mentions a "hospital toolkit" and model legislation) may beat competition.
- **H5 (government): partially alive.** Governments fund Undue's debt buys, and LA County procured presumptive-eligibility data and a portal. The buyer is a county or health plan consortium, not a single hospital.

## Thin / missing (and the searches that produced each negative)

- **Any public price for presumptive-charity screening** (Experian, Waystar, TransUnion, Optum).
  - Searches: "presumptive charity care screening pricing per account hospital RFP contract price"; "Experian Healthcare Patient Financial Advisor presumptive charity pricing per inquiry cost hospital"; "presumptive charity screening Experian OR Waystar contract board minutes county hospital approve amount per year"; plus the HFMA Q&A (structure only).
  - TransUnion healthcare never appeared in any result. Optum/Change: not searched separately (gap).
- **The HASC/LA award and price.** Search: "HASC L.A. Care presumptive eligibility income verification vendor selected award 2026 portal RFP". No award notice.
- **Any hospital paying Dollar For.** Search: "Dollar For hospital partnership program fee hospitals pay..."; the 990 shows only $25K unspecified program revenue.
- **Cedar primary pricing.** Search: "Cedar patient financial engagement pricing model health systems per statement fee". Only third-party write-ups.
- **Flywire healthcare take rate.** 10-K partial read (first 100K of 391K chars). The MD&A was not read, so this is a gap, not a confirmed negative.
- **AHA uncompensated care after 2020.** Two searches ("AHA uncompensated hospital care cost fact sheet 2025 billion 2023" and an aha.org-scoped fact-sheet search). Latest edition found is February 2022.
- **Ascension Saint Thomas main-hospital Schedule H.** Two ProPublica-scoped searches; the filer EIN was not identified.
- **Tennessee 68-11-262 statute text.** Justia was blocked by Cloudflare (not bypassed); only the hospital-policy citation was found. The 175% figure is unverified.
- **Tennessee screening mandate.** One search ("Tennessee hospital charity care law uninsured discount statute TCA 68-11..."). Not confirmed a second way, so "none found" is provisional.
- **RWJF / Arnold / Commonwealth grants in 2024-2026 for medical-debt tech.** One search each for RWJF and Arnold; Commonwealth not searched for grants. Provisional.
- **NY, WA, IL presumptive statute text.** Not confirmed.
- **CFPB appeal.** No appeal found. Second way: the NCLC case page reads "Resolved Case".

## What would change this conclusion

- A hospital CFO or patient-access director in a mandate state saying they would pay for patient-attested intake that cuts false positives would revive H1. That takes interviews, which a desk brief cannot do.
- A published per-transaction price from Experian or Waystar, or the HASC award, would let H1 be sized at all.
- A Tennessee funder with a health-access or medical-debt line (BCBST Foundation "Access" focus area; not confirmed to fund tools) would strengthen local H2.

## Sources (all accessed 2026-10-17)

- ProPublica, Dollar For: https://projects.propublica.org/nonprofits/organizations/460889864 ; 2025 990 full text: /nonprofits/full_text/202641349349307424/IRS990
- ProPublica, Medical Debt Resolution Inc (Undue): https://projects.propublica.org/nonprofits/organizations/471442997 ; 2025 990: /nonprofits/full_text/202622129349301127/IRS990
- ProPublica API JSON for both EINs (api/v2/organizations/{ein}.json)
- ProPublica, VUMC Sch H: /nonprofits/full_text/202621279349301822/IRS990ScheduleH ; Saint Thomas Health Sch H: /nonprofits/full_text/202641329349307429/IRS990ScheduleH
- Goodbill: https://help.goodbill.com/en/articles/254209
- Resolve: https://www.resolvemedicalbills.com/partners/konnectmd
- CareRoute: https://www.careroute.ai/bill-defense (search summary)
- Waystar FY2025 release: https://investors.waystar.com/news-releases/news-release-details/waystar-reports-fourth-quarter-and-fiscal-year-2025-results (2026-02-17)
- Waystar Atrium case study: https://www.waystar.com/wp-content/uploads/2019/01/Waystar_CaseStudy_AtriumHealth.pdf
- Flywire 10-K FY2025: https://www.sec.gov/Archives/edgar/data/1580560/000119312526067540/flyw-20251231.htm
- OHA HB 3320 report: https://www.oregon.gov/oha/HPA/ANALYTICS/HospitalReporting/Hospital%20Prescreening%20Implementation%20Interview%20Summary.pdf (January 2025)
- Oregon HB 4040: https://apps.oregonlegislature.gov/liz/2026R1/Measures/Overview/HB4040
- Lund Report: https://www.thelundreport.org/content/hospitals-push-curb-charity-care-sparks-opposition (2026-02-24)
- HFMA Q&A: https://www.hfma.org/?p=108398 (2025-12-16)
- HASC bulk-pricing RFP: https://hasc.org/2025/10/22/medical-debt-and-presumptive-eligibility-rfp-bulk-pricing/
- eCFR 26 CFR 1.501(r)-6: https://www.ecfr.gov/current/title-26/chapter-I/subchapter-A/part-1/subject-group-ECFR062882ac6495890/section-1.501(r)-6
- NCLC case page: https://www.nclc.org/resources/cornerstone-credit-union-league-et-al-v-cfpb-et-al/
- Orrick InfoBytes: https://infobytes.orrick.com/2025-07-18/district-court-tosses-cfpbs-medical-debt-rule/
- CMS CY2026 OPPS price transparency fact sheet: https://www.cms.gov/newsroom/fact-sheets/cy-2026-opps-ambulatory-surgical-center-final-rule-hospital-price-transparency-policy-changes (2025-11-21)
- KFF: https://www.kff.org/health-costs/the-estimated-value-of-tax-exemption-for-nonprofit-hospitals-was-about-28-billion-in-2020/
- Lown fair share: https://lowninstitute.org/projects/hospital-fair-share-spending/ ; Lown 2021 release: https://lowninstitute.org/press-release-most-us-nonprofit-hospitals-neglect-community-investment-obligation-analysis-reveals/
- AHA fact sheet: https://www.aha.org/fact-sheets/2020-01-06-fact-sheet-uncompensated-hospital-care-cost
- HCA patient financial support: https://www.hcahealthcare.com/patients/pricing-and-financial-information/patient-financial-support
- UT Medical Center FAP (cites TCA 68-11-262): https://www.utmedical.org/sites/default/files/media/documents/Discounts%20and%20Financial%20Assistance%20Program%20Policy%20Dec%202025.pdf
- CFMT 2025 grants: https://www.cfmt.org/stories/2025-community-impact-grantees/
- TriStar / HCA Foundation: https://www.tristarhealth.com/about-us/newsroom/tristar-health-announces-hca-healthcare-foundation-grants-supporting-89-middle-tennessee-nonprofits (2026-06-24)
- Search-summary-only sources (UNVERIFIED): Chronicle of Philanthropy (DRK and RWJF grants); CauseIQ (Dollar For funders); calmatters / HCAI (AB 1312); HCPF (CO HB21-1198); ilga.gov (HB 2719); lawfilesext.leg.wa.gov (HB 1616); Undue / NJ / NYC / CT / DE government pages; grantedai.com (BCBST aggregator).
