# Middle TN hospitals: HCA TriStar FAP

> Raw subagent report, saved verbatim (non-ASCII transliterated) on 2026-10-17.
> Not yet reviewed or cold-assessed by the orchestrator; numbers are as the agent reported them.
> Source transcript agent id: a99d57c7a15a76319

Evan - HCA / TriStar Health financial-assistance brief (access date 2026-10-17, CDT, UTC-5). ASCII only; nothing written to disk in the project.

## TL;DR
- HCA publishes ONE system-wide policy text. TriStar's own page carries the thresholds, and all 9 Tennessee TriStar hospital pages link to that same page (verified by href in each hospital page's HTML). I found no hospital-specific policy page. The hospital-level URL pattern .../locations/tristar-<hospital>/.../financial-assistance returns 404 for every hospital.
- Thresholds (VERIFIED-VERBATIM): free care ("100% Charity discount") for 0-200% FPL; expanded assistance for 201-400% FPL when the balance is over $1,500; uninsured discount modeled on managed care, ~92% at most facilities (HCA national page).
- Not published on any page I could reach: an effective date, the policy PDF itself, the application form, the application window, residency or asset tests, presumptive eligibility, languages, and detailed collections rules. Third-party sites (CareRoute) state some of these, such as 240 days. Those are unverified, and probably imported from the nonprofit 501(r) rule, which does not apply to HCA.
- Both pages say discounts "may vary by location" and some locations "may have identified additional criteria." So one system policy is the best reading, but a hospital-level variation cannot be excluded without the full internal policy.
- Interest concentration: all load-bearing numbers come from HCA / TriStar self-reporting (VENDOR-SELF-REPORTED). The only independent source is the Tennessee statute, and I could only reach it through a 2016 secondary summary.

## Method
- Stage 3 hypotheses. H1: HCA runs one uniform policy across its TN hospitals. Rival H2: each hospital has its own thresholds. Rival H3: the policy is a 501(r)-style FAP with a 240-day window.
- Raw page text came from curl, run twice with different user-agents (the page's own HTML text, so VERIFIED-VERBATIM). WebSearch snippets are CLOSE-PARAPHRASE at best.
- The shared browser pane was unusable: another agent's navigation hijacked my tab and the tab cap blocked a new one. That is why I used curl.
- Stage 10.5 (cold assessment) skipped as instructed.
- Phase effects (2026-10-17): 8.5 verify - added a limitation. It downgraded the CareRoute 240-day and 92% claims to unverified and flagged that Justia (HTTP 403) blocked the statute text. 10.5 - skipped.

## Which hypotheses survived
- H1 survived (strongest). Evidence: the system page, HCA's page, and all 9 hospital pages pointing to one URL. Residual risk: the "may vary by location" disclaimers.
- H2 was not supported; no hospital-specific page or text was found. It is not killed, because the full policy was not obtained.
- H3 died for the primary sources: neither page mentions 240 days or a 501(r) FAP. The 240 days appears only on CareRoute.

## Where the policy lives
- TriStar system page, the "Charity Discount Policy" section: https://www.tristarhealth.com/patient-resources/patient-financial-resources/financial-assistance. Its meta description reads "TriStar Health offers many forms of financial assistance for patients without healthcare insurance needing emergent or non-elective services." The page has no effective date and no PDF link.
- HCA corporate page: https://www.hcahealthcare.com/patients/pricing-and-financial-information/patient-financial-support. It says "Data as of Dec. 31, 2025 unless otherwise noted", and that is the only date. It is a data-as-of date, not a policy effective date.
- Intermediate HCA page: https://hcahealthcare.com/patients/pricing-and-financial-information.dot redirects to /patients/pricing-and-financial-information. It links to the HCA corporate page and to a facility locator.

## Hospital list (tristarhealth.com/about-us says "10 hospitals")
- Page text: "TriStar Health is proud to offer 111 physician practices, 18 urgent care centers, 10 hospitals, 8 surgery centers and 7 freestanding emergency rooms across Tennessee and Southern Kentucky."
- Hospitals found on /locations: Centennial, Skyline, Summit, Hendersonville, StoneCrest, Southern Hills, Horizon, Ashland City, NorthCrest (Springfield, TN), and Greenview Regional (Bowling Green, KY - outside the Tennessee region).
- Centennial Children's, Centennial Women's and Centennial Parthenon Pavilion appear as separate bill-pay and insurance entries. Skyline has a Madison Campus bill-pay entry. I did not verify their separate licensure.
- NorthCrest was not in your example list; it is a Middle Tennessee hospital and should be included.

## Per-hospital table
Beds are marketing text from the hospital's own web page (VERIFIED-VERBATIM as page text), NOT licensed beds. The census agent should use the state source. County is my general knowledge, not verified from these pages.

| Hospital | Address (from site) | Beds per website | FA policy URL | Policy applies? |
|---|---|---|---|---|
| TriStar Centennial Medical Center | 2300 Patterson St, Nashville 37203 | "741-bed comprehensive facility" | system page above | Hospital page links to it (VERIFIED) |
| TriStar Skyline Medical Center | 3441 Dickerson Pike, Nashville 37207 | NOT-FOUND on site (secondary: 233 per a recruiter listing; 223 per Turquoise; conflicting, unreliable) | same | Linked (VERIFIED) |
| TriStar Summit Medical Center | 5655 Frist Blvd, Hermitage 37076 | "234-bed" | same | Linked |
| TriStar Hendersonville Medical Center | 355 New Shackle Island Rd, Hendersonville 37075 | "159-bed" | same | Linked |
| TriStar StoneCrest Medical Center | 200 Stonecrest Blvd, Smyrna 37167 | "119-bed" | same | Linked |
| TriStar Southern Hills Medical Center | 391 Wallace Rd, Nashville 37211 | "136-bed" | same | Linked |
| TriStar Horizon Medical Center | 111 Highway 70 E (Dickson, TN - city not captured from the page) | "158-bed" | same | Linked |
| TriStar Ashland City Medical Center | 313 N Main St, Ashland City 37015 | NOT-FOUND on site. The page title reads "Rural Emergency Hospital" (VERIFIED). A secondary source says 12 beds (single source, unverified). | same | Linked |
| TriStar NorthCrest Medical Center | 100 Northcrest Dr, Springfield 37172 | "109-bed" | same | Linked |
| (Out of region) TriStar Greenview Regional | Bowling Green, KY | "211-bed" | same | Linked |

All fields below are identical across hospitals because there is one policy:

| Field | Value | Status |
|---|---|---|
| Free care | 0-200% FPL: "100% Charity discount" | VERIFIED-VERBATIM |
| Partial / discount tier | 201-400% FPL, balance over $1,500 | VERIFIED-VERBATIM |
| Cap in the expanded tier | 4% of annual income, sliding scale (HCA page only; absent from the TriStar page) | VERIFIED-VERBATIM (HCA page) |
| Uninsured discount | "approximately 92% of the patient's total bill at most facilities" (HCA page); "may vary by location" (TriStar page) | VERIFIED-VERBATIM; a per-hospital % is NOT-FOUND |
| Insured patients | "We make both of these charity care policies available to all patients, regardless of their insurance coverage." | VERIFIED-VERBATIM |
| Under-insured above 400% FPL | "Under-insured Discount/Patient Liability Protection (PLP)", need-based sliding scale; no thresholds | VERIFIED-VERBATIM (name and description only) |
| Asset test | None stated; Medicare patients need "independent income and resource verification" | NOT-FOUND for a general asset test |
| Residency | NOT-FOUND (CareRoute says "none stated", which is not evidence) | NOT-FOUND |
| Application window | NOT-FOUND (CareRoute: "about 240 days", unverified) | NOT-FOUND |
| Documents | Medicare: most current federal tax return preferred, or two items from a list (state tax return, pay stubs, written documentation from income sources, 3 months of bank statements, current credit report) | VERIFIED-VERBATIM (Medicare only) |
| Documents, non-Medicare | "All Medicare accounts and all non-Medicare inpatient accounts will be required to have supporting income verification documentation." | VERIFIED-VERBATIM (non-Medicare outpatient is not addressed) |
| Presumptive eligibility | NOT-FOUND | NOT-FOUND |
| How to apply | "contact your hospital for details"; mentions a "Financial Assistance Application" (Medicare context) and a "Uninsured Patient Information document" signed at service; pricing line (800) 370-1983. No application form, link or address found. | CLOSE-PARAPHRASE / form NOT-FOUND |
| Languages | NOT-FOUND (no language statement on the pages; the site is en-US) | NOT-FOUND |
| Effective date | NOT-FOUND | NOT-FOUND |
| Collections | HCA: "We do not report to credit bureaus, and we do not pursue litigation activity that involves suing patients or filing liens on patient bad debt accounts." Also "interest-free payment arrangements". Nothing about timelines or extraordinary collection actions on the TriStar page. | VERIFIED-VERBATIM (HCA page) |

## Quoted evidence (page text via curl; exact strings re-confirmed with a second curl)

TriStar system page:
- "Financial relief may be available to patients who have received non-elective care and do not qualify for state or federal assistance and are unable to establish partial payments or pay their balance. In most cases, this will apply to patients who fall between 0 - 200% of the Federal Poverty Level. Federal Poverty Levels based on total household income, with sufficient supporting documentation provided by the patient, will have a 100% Charity discount processed."
- "For patients with balances greater than $1,500, and whose documented income is in-between 201 and 400 percent of the Federal Poverty Level, we have an expanded financial assistance policy that may reduce the amount you owe."
- "Some locations may have identified additional criteria for charity eligibility besides the Federal Poverty Levels as noted above (i.e., high medical costs, more lenient income levels, etc.). To verify your eligibility for assistance under this policy, we recommend you contact the hospital."
- "No charity discount can be applied to any account with any outstanding payer liability."
- "All Self-Pay patients, excluding elective cosmetic procedures and facility designated self-pay flat rate procedures, will receive discount similar to managed care, referred to as an 'uninsured discount'. The Uninsured Discount is limited to patients who have no third party payer source of payment or do not qualify for Medicaid, Charity or any other discount program the facility offers. The amount of the discount offered may vary by location based on state requirements, patient income levels, and local rates."

HCA corporate page:
- "Charity Care Policy - provides a 100% write-off of charges related to emergency services for qualifying patients. Generally, patients with annual household incomes of less than 200% of FPG qualify for this program"
- "Expanded Charity Care Policy - provides financial relief for emergency services to families with annual household incomes between 200% and 400% of FPG. For patients who qualify for this program, we cap their out-of-pocket balances at 4% of their annual income using a sliding scale. For example, a family of four with a household income of $100,000 would have their liability capped at $4,000. (We make both of these charity care policies available to all patients, regardless of their insurance coverage.)"
- "Uninsured Discount Policy - offers patients with no insurance, or exhausted insurance benefits, a discount for emergency services. The discount is approximately 92% of the patient's total bill at most facilities, which is similar to expected reimbursement for patients with Medicaid coverage."
- "Under-insured Discount/Patient Liability Protection (PLP) - the PLP program provides protection for patients with household incomes above 400% of FPG."
- "Unless otherwise noted, this information applies to HCA Healthcare facilities located in the United States."

## Discrepancies Evan should know about
1. Service scope: the HCA page says charity applies to "emergency services". The TriStar page says "non-elective care". The TriStar scope is the wider one, and it is the one patients see in Tennessee.
2. Boundary at exactly 200% FPL: HCA says "less than 200%" (free) and "between 200% and 400%" (expanded). TriStar says "0 - 200%" (free) and "201 and 400" (expanded). Treat 200% as free per TriStar.
3. The $1,500 balance floor for the expanded tier and the "4% of income" cap appear on only one page each (TriStar and HCA respectively). The 4% cap is not on TriStar's page.
4. Other HCA divisions publish different bands. A search snippet says HCA HealthONE uses 251-400% for the expanded tier. This is evidence that "may vary by location" is real, so it is a reason not to assume uniformity for facilities outside TriStar's page. It is a snippet only (not fetched).
5. For-profit status: no IRS 501(r) FAP rules apply (no 240-day window, no required plain-language summary). The 240 days, "presumptive eligibility" and "residency none" claims on CareRoute are template defaults, not HCA statements.

## Tennessee law (secondary source only; primary text UNREACHABLE)
- Source: Hilltop Institute, "Community Benefit State Law Profile: Tennessee", June 2016 (https://www.hilltopinstitute.org/wp-content/uploads/hcbp/hcbp_docs/HCBP_CBL_TN.pdf; read as text via pdftotext, VERIFIED-VERBATIM for what it says). It is a 10-year-old summary, not the statute.
- "Tennessee does not require hospitals to adopt or implement financial assistance policies but requires hospitals that have charity care policies to develop a 'concise statement' of these policies." (Tenn. Code 68-11-268)
- "Tennessee law requires all hospitals to post a statement of their charity care policies in a place accessible to the public." (68-11-268)
- "Tennessee law prohibits all hospitals from requiring an uninsured patient to pay an amount that exceeds 175 percent of the cost for the services provided (calculated using the cost-to-charge ratio in the most recent joint annual report to the state's Department of Health)." (68-11-262)
- Hospitals licensed by the state must file the Joint Annual Report, which includes charity care and bad debt data (68-11-310).
- The statute text on Justia returned HTTP 403 (Cloudflare), so I could not read it. The current text and any post-2019 amendments are not verified. A WebSearch snippet says Fowler v. Morristown-Hamblen Hospital Association (Tenn. Ct. App. E2018-00782) held there is no private right of action under 68-11-262. That is from a snippet only (CLOSE-PARAPHRASE at best) and not verified.
- Also reachable: Tennessee Health Facilities Commission Charity Care Report 2024 (https://www.tennessee.gov/content/dam/tn/hfc/documents/HFC-Charity_Care_Report-2024.pdf). It covers only Certificate-of-Need facilities approved 2017-2022, and none of the TriStar hospitals turned up in the text. It is not useful for per-hospital charity data.

## Numbers register
| Number | What it claims | Source | Date | Interest class | Verdict |
|---|---|---|---|---|---|
| 200% FPL (free) | Free care ceiling | tristarhealth.com FA page | accessed 2026-10-17 (page undated) | VENDOR-SELF-REPORTED | VERIFIED-VERBATIM x2 curl calls |
| 201-400% FPL | Expanded tier | same | same | VENDOR-SELF-REPORTED | VERIFIED-VERBATIM |
| $1,500 | Balance floor for expanded tier | same | same | VENDOR-SELF-REPORTED | VERIFIED-VERBATIM |
| 4% of income | Cap in expanded tier | hcahealthcare.com | data as of 2025-12-31 | VENDOR-SELF-REPORTED | VERIFIED-VERBATIM |
| ~92% | Uninsured discount "at most facilities" | hcahealthcare.com | same | VENDOR-SELF-REPORTED | VERIFIED-VERBATIM |
| ~$4.5 billion | HCA uncompensated care cost in 2025 | hcahealthcare.com | same | VENDOR-SELF-REPORTED | VERIFIED-VERBATIM (not load-bearing) |
| 175% of cost | TN cap on uninsured charges | Hilltop 2016 summary of 68-11-262 | 2016 | INDEPENDENT (secondary) | CLOSE-PARAPHRASE; current statute UNREACHABLE |
| 240 days | Application window | careroute.ai only | July 2026 | UNVERIFIABLE (a bill-defense company with a commercial interest) | NOT-FOUND in any HCA/TriStar source (fetched pages only) |
| 741 / 234 / 159 / 119 / 136 / 158 / 109 / 211 beds | Marketing bed counts | each hospital's tristarhealth.com page | 2026-10-17 | VENDOR-SELF-REPORTED | VERIFIED-VERBATIM as marketing text; not licensed beds |

- Interest concentration: every load-bearing threshold is VENDOR-SELF-REPORTED (the TL;DR states this).
- Same-source dependency: the TriStar page and the HCA page are both HCA-authored. They agree on the free tier at 200% and on the 201-400% band, but that is one author, not two independent confirmations.

## Verification table (stage 8.5)
| Load-bearing claim | Source | Verdict |
|---|---|---|
| Free care at 0-200% FPL | TriStar FA page, curl x2 | VERIFIED-VERBATIM |
| Expanded tier 201-400% FPL, balance over $1,500 | TriStar FA page, curl x2 | VERIFIED-VERBATIM |
| 4% income cap and ~92% uninsured discount | HCA corporate page, curl x2 | VERIFIED-VERBATIM |
| Charity available to insured patients | HCA corporate page | VERIFIED-VERBATIM |
| All 9 TN TriStar hospital pages point to the one system policy | hrefs extracted from each hospital page's HTML | VERIFIED |
| No hospital-specific FA pages exist | 404 on all hospital-level URL patterns tried (negative; tried both /for-patients/ and /patient-resources/ patterns) | Provisional negative; a hospital-specific policy could exist outside the pages tried |
| No application window / effective date / residency / presumptive / languages | text of FA page, HCA page, pricing-FAQ, contact-us pages | NOT-FOUND (searched: curl text of 6 TriStar pages; WebSearch for application form and for a 240-day window) |
| 240-day window | careroute.ai | NOT-FOUND in primary sources |
| TN 175% cost cap | Hilltop 2016 | CLOSE-PARAPHRASE; statute UNREACHABLE (Justia 403, lawserver JS wall) |

## Thin / missing
- The actual HCA policy document (with an effective date) and the application form. Searches: tristarhealth.com pages (6), HCA corporate pages (2), WebSearch x3 for a PDF or "Financial Assistance Application"; none surfaced a PDF. Ask the hospital's financial counseling or call the (800) 370-1983 pricing line.
- A per-hospital uninsured discount percentage; only "approximately 92% at most facilities" exists.
- Application window, residency, asset test, presumptive eligibility, languages, and the specific collections timeline: none published on the pages I reached. The 240-day figure appears only on CareRoute.
- Current text of Tenn. Code 68-11-262 and 68-11-268 (primary source blocked); suggested route: capitol.tn.gov or Lexis/Westlaw.
- Licensed beds for Skyline and Ashland City (the hospital pages give no bed count). The Tennessee Health Facilities Commission Alter Bed Capacity report (https://www.Tennessee.gov/content/dam/tn/hfc/documents/Alter-Bed-Capacity-Report-FY2020.pdf) surfaced in search but I did not read it; the census agent should.
- Primary field data (a mystery-shopper call to a TriStar financial counselor) is not simulated here.

## What would change this conclusion
- A hospital-specific policy PDF with different tiers (kills H1).
- An HCA policy document with an application window or a plain-language summary.
- A 2026 amendment to TN law changing the 175% cap or adding a for-profit FAP requirement.

## Sources (accessed 2026-10-17 CDT)
- https://www.tristarhealth.com/patient-resources/patient-financial-resources/financial-assistance
- https://www.hcahealthcare.com/patients/pricing-and-financial-information/patient-financial-support
- https://hcahealthcare.com/patients/pricing-and-financial-information.dot (redirects to /patients/pricing-and-financial-information)
- https://www.tristarhealth.com/about-us
- https://www.tristarhealth.com/locations/tristar-{centennial,skyline,summit,hendersonville,stonecrest,southern-hills,horizon,ashland-city,northcrest}-medical-center and /tristar-greenview-regional-hospital
- https://www.tristarhealth.com/patient-resources/patient-financial-resources/{pricing-estimates-and-information, our-pricing-commitment, contact-us, insurance-information, make-a-payment}
- https://www.hilltopinstitute.org/wp-content/uploads/hcbp/hcbp_docs/HCBP_CBL_TN.pdf (2016 secondary)
- https://www.tennessee.gov/content/dam/tn/hfc/documents/HFC-Charity_Care_Report-2024.pdf
- https://www.careroute.ai/hospital-financial-assistance/tristar-health (third-party, unverified, commercial interest)
- WebSearch result snippets, for context only: hcafloridahealthcare.com and capitalregionalmedicalcenter.com FA pages ($1,500 / 201-400%), healthonecares.com FA page (251-400%).

Scratch files (curl captures and strip scripts) are in <session scratchpad>\tri\ - session-local, not for the project.
