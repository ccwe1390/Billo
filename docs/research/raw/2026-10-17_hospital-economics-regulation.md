# Hospital economics, TN targets and regulation (willingness-to-pay)

> Raw subagent report, saved verbatim (non-ASCII transliterated) on 2026-10-17.
> Not yet reviewed or cold-assessed by the orchestrator; numbers are as the agent reported them.
> Source transcript agent id: a62c9dd035841c880

Evan - research report: BillScan willingness-to-pay desk research. Checked 2026-10-17. No files written. The only downloads were PDFs pulled for text extraction: one into the scratchpad (`dl_hfc/hfc2024.pdf`), the rest auto-saved by WebFetch into the session's tool-results folder.

**Main flaw first.** Dollar For is the patient-side nonprofit closest to BillScan. Its own Nov 2025 analysis says that giving charity care to every eligible patient costs hospitals money. It does not save them money. The ceiling is about 0.7% of net revenue, offset only by lower collection costs, which they did not measure. So a tool that raises FAP enrollment has a weak business case to a hospital where no law requires screening. Tennessee requires none: no FAP mandate, no screening duty, and its 2025 credit-reporting bill stalled. Hospitals pay where states require screening (CO, OR, IL, MD, WA, CA from July 2027, NC, DE) or where a payer or public-health coalition funds it (the LA County RFP).

Format per item: claim | quote | URL | date | confidence.

## A. Hospital economics

1. **AHA national uncompensated care, latest year published: 2020, $42.67B.** This is the cost of bad debt plus charity care across 5,139 community hospitals. AHA does not split it into charity vs bad debt. I found no newer AHA edition.
   - Quote: "Since 2000, hospitals of all types have provided almost $745 billion"
   - https://www.aha.org/system/files/media/file/2020/01/2020-Uncompensated-Care-Fact-Sheet.pdf | PDF is the Feb 2022 edition | High. The PDF table's columns are shifted by one row; the 2020 value reads as $42.67B.
   - AHA's later "rising uncompensated care" figures are rates, not dollars: the median uncompensated-care rate went from 6.4% (Q1 2023) to 8.7% (July 2023), from vendor Syntellis data. https://www.aha.org/news/headline/2023-09-20-blog-uncompensated-care-increases-medicare-dsh-cuts-exacerbate-hospitals-challenges | 2023-09-20 | Medium.
   - **Charity vs bad debt split, national: MISSING.** Searches: AHA fact sheets, AHA Fast Facts, the AHA domain for 2022/2023.
2. **KFF: nonprofit tax exemption about $28B vs charity care about $16B (2020).**
   - Quote: "exceeded total estimated charity care costs ($16 billion) among nonprofit hospitals in 2020"
   - https://www.kff.org/health-costs/the-estimated-value-of-tax-exemption-for-nonprofit-hospitals-was-about-28-billion-in-2020/ | 2023-03-14, revised 03-27 | High.
3. **Bai et al., Health Affairs, Apr 2021 (2018 Medicare cost reports): charity care per $100 of total expenses** was about $2.30 at nonprofit, $4.10 at government and $3.80 at for-profit hospitals.
   - Seen only via secondary pages: https://pnhp.org/news/charity-care-in-government-nonprofit-and-for-profit-hospitals/ ; the JHU Hub page returned 403.
   - Medium-high: several sources agree, but I did not read the paper itself.
4. **Lown Institute "fair share" 2025 report.** 20 states, about 1,800 hospitals, 2020-2022 data. Combined deficit $11.5B; about 54% of hospitals in deficit. The earlier national figure was $25.7B (2021 data).
   - https://lownhospitalsindex.org/wp-content/uploads/2025/04/fair-share-2025-national-report-20250409.pdf | 2025-04-09 | Medium. The PDF was over 10MB and would not fetch, so these numbers come from search summaries and Crowe coverage. I could not check whether Tennessee is among the 20 states.
   - VUMC fair-share deficit: about -$157M (2018 data) and -$158M (2020 data), per Lown and Becker's coverage. https://www.beckershospitalreview.com/hospital-finance/25-hospitals-where-charity-care-falls-behind-tax-breaks.html | Medium. AHA disputes Lown's method.
5. **Dollar For: $14B a year in undelivered charity care.**
   - Quote: "hospitals fail to provide at least $14 billion annually in charity care"
   - https://dollarfor.org/wp-content/uploads/2024/04/Dollar_For.Bridging_the_Chasm.pdf | created 2024-04-29 | method read from the PDF text.
   - **Step 1, about $7B (self-reported).** 2019 KFF Health News analysis: $2.7B of charity-eligible bad debt self-reported on Schedule H by 1,651 nonprofit hospitals, which is $1.6M per hospital. That average was imputed to the other 1,336 nonprofits (+$2.2B) and to 1,235 for-profits (+$2B). Total: about $7B.
   - **Step 2, doubling to $14B.** In a 2020 HSCRC study (about 2M patients in 2017-18, matched to 1.2M Comptroller tax records), "the bills for 60% of patients at or below 200% FPL ended up as bad debt". That is $147M of $433.5M Maryland bad debt (33.9%). Maryland hospitals self-reported only $31M as charity-eligible, "less than half". The doubling assumes the Maryland ratio holds nationally.
   - Confidence: high on what the report says; medium on the estimate itself, which is an extrapolation.
6. **Dollar For "The Bottom Line" (key for willingness to pay).** Covering all eligible patients would cut hospital net revenue by at most 0.7%. Patient out-of-pocket is 2.5% of hospital net revenue, and eligible patients' share is 1.1%.
   - Quote: "Only 29% of eligible patients receive financial assistance, but covering everyone would only reduce hospital revenue by 0.7%"
   - The report says collection-cost savings "would likely offset lost revenue, at least in part". It does not measure them.
   - It also claims a DSH reimbursement upside. I could not verify that claim, so treat it as unverified.
   - https://dollarfor.org/wp-content/uploads/2025/11/BottomLine.pdf | Nov 2025 (CMS NHE 2023 + MEPS 2023) | Medium, advocacy source.
7. **Evidence that presumptive screening reduces bad debt or collection cost: no peer-reviewed study found.**
   - McDermott (law firm), only qualitative: "hospitals could experience a reduction in bad debt by encouraging eligible uninsured patients to get health coverage". https://www.mcdermottlaw.com/?p=259948 | 2023-12-04.
   - Experian (vendor) gives a hypothetical, not a result: 1,460 uninsured patients a month, 10% Medicaid-eligible, "$146,000 per month", avoiding about $1.8M a year in write-offs. https://www.experian.com/blogs/healthcare/hospitals-streamline-checks-to-meet-new-charity-care-policies/ | 2022-08-09 | Low.
   - Oregon (Tradeoffs via KFF Health News): "Hospitals in Oregon more than doubled the amount of charity care they provided, on average". OHSU's share of patients getting aid went from 12% to 64%. https://kffhealthnews.org/health-industry/hospital-financial-aid-obstacles-presumptive-eligibility-texas-oregon | 2026-10-15 | High. This shows more aid, not less bad debt.
   - Oregon, about 80% of 2025 aid recipients "never filled out an application", from the first 26 hospitals to report. https://news.outsourceaccelerator.com/presumptive-eligibility-charity-care/ | 2026-10-08 | Medium, secondary.
   - Searches run: "presumptive charity screening reduces bad debt study", "propensity to pay results", HFMA charity screening.
8. **Cost to collect.**
   - HFMA best-practice cost-to-collect is about 2% (down from 3%). It is HFMA "Ask the Expert" content from 2012, updated 2022: https://www.hfma.org/revenue-cycle/kpis/7284/ | Medium.
   - Crowe collection rates: true self-pay patients pay about 6.06 cents on the dollar; insured patients' out-of-pocket about 15.51%; collectability drops sharply above $7,500. I saw this only in search snippets (the healthcarefinancenews page returned 403) | Low-medium.
   - **Current hospital cost-to-collect for self-pay specifically: MISSING.**

## B. Nashville / Tennessee targets

1. **VUMC (EIN 35-2528741), from ProPublica:**
   - FY2025 (ended June 2025): revenue $8,674,383,028; expenses $8,258,963,378; net $415,419,650. 990 filed 2026-05-07, Schedule H listed.
   - FY2024: revenue $7,706,035,528.
   - https://projects.propublica.org/nonprofits/organizations/352528741 | High.
   - **Schedule H figures (charity care at cost, bad debt, charity-eligible bad debt): MISSING.** The ProPublica XML sits behind a Cloudflare security check, which I did not bypass, and the PDFs would not load. Next step: open https://projects.propublica.org/nonprofits/organizations/352528741/202621279349301822/IRS990ScheduleH in a normal browser and read Part I line 7a and Part III lines 2-3.
   - VUMC FAP: the plain-language summary gives no FPL figures and does not mention presumptive eligibility ("Financial hardship is evaluated on a case-by-case basis"). https://vanderbilthealth.com/information/financial-assistance-plain-language-summary.
   - VUMC's 2024 AGB notice sets the AGB at 26% of billed charges.
2. **HCA (for-profit), FY2025 10-K:** "The estimated cost of total uncompensated care was $4.605 billion for 2025, $4.366 billion for 2024 ... $3.720 billion for 2023". Total 2025 revenue $75.6B; implicit price concessions $7.674B; "approximately 88% of our admissions of uninsured patients occurred through our emergency rooms".
   - https://www.sec.gov/Archives/edgar/data/860730/000119312526044769/hca-20251231.htm | filed 2026 | High (company-reported).
   - HCA policy: free emergency care under 200% FPG; 200-400% FPG capped at "4% of their annual income"; uninsured discount "approximately 92%". https://www.hcahealthcare.com/patients/pricing-and-financial-information/patient-financial-support | High.
3. **Ascension, system-wide FY25:** "$1.7 billion in care for persons living in poverty" and other programs, plus $1.8B unreimbursed Medicare, $3.4B total. Operating loss $491M. https://about.ascension.org/news/2025/09/ascension-releases-q4-fy25-financial-results | 2025-09-17 | High (self-reported). No separate charity-care line.
   - **Ascension Saint Thomas Tennessee, FY2025: MISSING.** The latest found is more than $154M in community benefit in FY2021, secondary.
   - Caveat: Saint Thomas files under several EINs. A TY2024 Schedule H for "Saint Thomas Health" (EIN 58-1716804) covers only 3 small facilities: FA at cost $314,910; free care up to 250% FPG, discounts up to 400%; charity-eligible bad debt reported as $0. I read this from an IRS e-file render while another agent was steering the shared browser pane, so re-verify before citing. The main Saint Thomas hospitals' 990s were not found.
4. **Nashville General Hospital:**
   - An enterprise fund of the Hospital Authority, which is "a component unit of the Metropolitan Government of Nashville", "exempt from Federal and State income taxes".
   - FY2022 audit: gross charges $264.1M; charity care $38.6M (at charges); bad debt $22.6M; self-pay allowance about 100%; Metro subsidy approved for FY2023 $54.4M.
   - https://comptroller.tn.gov/content/dam/cot/la/advanced-search/2022/health-care/10187-2022-cn-nashvillehospital-rpt-cpa284-10-09-23.pdf | High but old.
   - FY2026 Metro subsidy: $60.7M, reported by a hospital board meeting transcript site (citizenportal.ai). Medium.
   - FY2027 proposed: $67,879,500. Final FY2027 amount: MISSING.
   - **501(c)(3) status: MISSING.** No 990 or EIN found.
   - IRS rule: 501(r) applies to government hospitals only if they "are (or seek to be) recognized" as 501(c)(3). Those that are must "meet all section 501(r) requirements that do not involve disclosure on or with the Form 990". https://www.irs.gov/charities-non-profits/section-501r-reporting | reviewed 2026-07-06 | High. Verify Nashville General via IRS TEOS.
5. **Tennessee statewide (HFC 2024 report, 2022 JAR data, self-reported):** covers only 25 hospitals that hold certificate-of-need (CON) approvals. Uncompensated care $3.44B, charity care $2.53B (charges basis). https://www.tn.gov/content/dam/tn/hfc/documents/HFC-Charity_Care_Report-2024.pdf | 2024-01-15 | Medium.

## C. Regulatory hooks (status as of Oct 2026)

1. **26 CFR 1.501(r)-6(c)(2), presumptive eligibility: allowed, not required.** A facility may find a patient FAP-eligible "based on information other than that provided by the individual or based on a prior FAP-eligibility determination".
   - If the patient is found eligible "for less than the most generous assistance available under the FAP", the hospital must:
     - give notice;
     - allow "a reasonable period of time to apply for more generous assistance";
     - process any application.
   - The regulation's examples include enrollment in means-tested programs and hospital or public data.
   - The 120-day rule: no extraordinary collection actions (ECAs) "for at least 120 days from the date the hospital facility provides the first post-discharge billing statement".
   - ECAs include credit reporting, selling debt, liens, garnishment and lawsuits.
   - https://www.law.cornell.edu/cfr/text/26/1.501(r)-6 (the eCFR link redirected to a block page) | High.
   - Schedule H, Part V line 20d asks whether the facility "Made presumptive eligibility determinations". 2025 Schedule H instructions: https://www.irs.gov/pub/irs-pdf/i990sh.pdf.
2. **Tennessee:**
   - TCA 68-11-262: hospitals may not charge uninsured patients more than 175% of cost (using the cost-to-charge ratio).
   - TCA 68-11-268: hospitals with a charity policy must post a "concise statement" of it.
   - "Tennessee does not require hospitals to adopt or implement financial assistance policies".
   - https://www.hilltopinstitute.org/wp-content/uploads/hcbp/hcbp_docs/HCBP_CBL_TN.pdf | June 2016 | Medium; may be stale. The statute text itself was 403 on Justia.
   - **2025-26 bills:** HB0223/SB0230 (medical debt off credit reports) was last acted on 03/12/2025, when it was taken off notice in subcommittee, with no public chapter. https://wapp.capitol.tn.gov/apps/BillInfo/default.aspx?BillNumber=HB0223&GA=114 | High.
   - **No enacted Tennessee medical-debt or screening law found.**
3. **CFPB medical-debt credit-reporting rule: vacated.**
   - Vacated 2025-07-11 in E.D. Tex. (No. 4:25-cv-00016) on the CFPB's own joint request, "over our clients' objections".
   - I found no appeal and no reissue. https://www.nclc.org/resources/cornerstone-credit-union-league-et-al-v-cfpb-et-al/ ("Resolved Case") | High.
   - States are filling the gap (e.g., Oregon SB 605 and Rhode Island, both effective 2026-01-01) | Medium.
4. **CMS price transparency:** the CY2026 OPPS final rule adds median and 10th/90th-percentile allowed amounts and a senior-official attestation. Effective 2026-01-01; enforcement from 2026-04-01. https://www.cms.gov/files/document/webinar-hospital-price-transparency-cy2026-opps-asc-final-rule-slides.pdf | Medium (secondary summaries).
5. **State screening mandates (these create buyers):**
   - **Colorado HB21-1198:** "must screen each uninsured patient unless a patient declines"; covers income up to 250% FPL. https://hcpf.colorado.gov/hospital-discounted-care | High.
   - **Oregon:** HB 3320 (2023) requires presumptive screening. HB 4040 (2026) raised the insured-patient threshold from $500 to $1,500; uninsured and OHP patients must still be screened before any bill. https://www.thelundreport.org/content/oregon-democrats-weaken-protections-against-hospital-bills-low-and-middle-income-patients | 2026-04-14 | High. Correction to the brief: HB 3076 is the 2019 FAP law, not the screening law.
   - **Illinois:** the 2023 Protect Illinoisans from Unfair Medical Debt law requires screening of uninsured patients "before pursuing any collection action". In force for services from 2024-06-29. Existing rule 77 Ill. Adm. Code 4500 requires a presumptive eligibility policy. High.
   - **Washington:** RCW 70.170.060(10)(c): "An initial determination of sponsorship status shall precede collection efforts". Free care up to 300% FPL at large systems. Amended 2025 c 182 (content not verified). https://app.leg.wa.gov/RCW/default.aspx?cite=70.170.060 | High.
   - **California AB 1312:** signed 2025-10-07 (Ch. 450). Mandatory screening plus presumptive eligibility via CalFresh/CalWORKs, from 2027-07-01. High.
   - **New York:** PHL 2807-k amended, effective 2024-10-20: uniform FAP form and 400% FPL. Presumptive eligibility not confirmed.
   - **Maryland:** free care under 200% FPL; refunds owed for 2017-2021. Collection limits in HB 268 (2025) not verified.
   - Six states will require presumptive eligibility by July 2027: CA, DE, IL, MD, NC, OR (KFF Health News 2026-10-15).
   - NCOIL model act (press release 2026-08-06): "requires nonprofit hospitals to adhere to charity care screening procedures". https://ncoil.org/news/ncoil-adopts-charity-medical-care-and-medical-debt-reform-model-act/.
6. **Federal:** H.R. 7478, the Patient Debt Relief Act (Rep. Vasquez): screening, a collection pause, and $100M for debt relief. Status MISSING; Congress.gov and GovTrack both returned 403. Medium-low.
7. **OBBBA / H.R. 1 (Public Law 119-21):** CBO projects 10M more uninsured by 2034, 7.5M of them from Medicaid/CHIP. Ramp: 1.3M (2026), 5.2M (2027), 8.6M (2029).
   - https://ccf.georgetown.edu/2025/08/14/new-cbo-health-coverage-estimates-of-budget-reconciliation-law/ (CBO data: https://www.cbo.gov/system/files/2025-08/61367-Uninsured-Data.xlsx) | 2025-08-11 | High.
   - Medicaid retroactive coverage shrinks to one month from 2027-01-01 (per Dollar For).
   - Urban Institute: +$283B uncompensated care 2025-2034, of which about $85B is hospital-related. This modeled the House version, not the final law. Medium.
   - Caveat: Tennessee did not expand Medicaid, so the largest single driver (work requirements for expansion adults, 5.3M) mostly misses Tennessee.

## D. What hospitals pay for screening or PFS outsourcing

- **Public price figures: MISSING.** Searches run:
  - county contract presumptive eligibility vendor per-account fee
  - PFS early-out / contingency fee rates
  - HFMA charity screening (HFMA 2025-12-09 says only "can be expensive")
  - KFF Health News and Tradeoffs coverage (no prices)
  - Experian blogs (no pricing)
- **Best structural evidence: the LA County RFP** (DPH + L.A. Care Health Plan + HASC, funded by L.A. Care).
  - Scope: a "centralized financial assistance and presumptive eligibility portal" brokering credit-bureau queries for hospitals.
  - Pricing asked for: per-hospital tiers (1-10 / 11-25 / 26-50 / 51+), per-query fee, per-user fee, annual service fee, and a 3-year total cost for 5 hospitals.
  - Dates: issued 2025-11-07; award 2026-01-19; contract start 2026-02-20.
  - No award amount found.
  - https://hasc.org/file/rfp-portal-solution/ | High.
  - Takeaway: the buyer was a payer plus a public-health coalition, not a single hospital. BillScan, as stateless and patient-facing, sits outside that credit-bureau model.

**Unverified or missing, overall:** VUMC Schedule H figures; Saint Thomas TN FY25; Nashville General's 501(c)(3) status and final FY27 subsidy; any national charity-vs-bad-debt split after 2020; any measured bad-debt reduction from screening; any vendor price. Other agents were using the same browser pane during this run, so I stopped using it.
