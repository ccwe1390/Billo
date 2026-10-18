# Middle TN hospitals: other systems FAPs (mtn-others)

> Raw subagent report, saved verbatim (non-ASCII transliterated) on 2026-10-17.
> Not yet reviewed or cold-assessed by the orchestrator; numbers are as the agent reported them.
> Source transcript agent id: a674a5587b09e1ee7

Evan, research brief: non-Vanderbilt / non-HCA / non-Ascension Middle TN hospitals, financial assistance policies. Access date 2026-10-17 (CDT). ASCII only. No files written to the project (scratch files only, in the session scratchpad).

## TL;DR
- Six hospitals have a policy I read in the page's own text: Nashville General, Maury Regional, Williamson Medical Center, Cookeville Regional, Covenant Cumberland Medical Center (Crossville), and Highpoint Sumner. Hypothesis H1 (most publish a current FAP with FPL tiers) mostly survived: 6 of 10 checked hospitals. The rival (the Lifepoint-run ones publish nothing usable) survived for the Lifepoint community hospitals: STRHS Lawrenceburg and Pulaski, and the Highpoint sites other than Sumner.
- Ownership changed for several candidates, so some belong to other agents' scopes:
  - Tennova Clarksville is now Vanderbilt Clarksville Hospital (acquired 2026-02-01/02). Harton in Tullahoma is Vanderbilt Tullahoma-Harton.
  - NorthCrest (Springfield) is HCA/TriStar NorthCrest.
  - Highpoint Health (Sumner, Riverview, Trousdale, Livingston, and per its site Winchester and Sewanee) is majority Lifepoint, co-owned with Ascension Saint Thomas since the Dec 2023 JV.
- Thresholds differ widely. Free care runs from 100% FPL (Maury) up to 200% (Nashville General, Highpoint, Covenant, and Cookeville at 100% FPL only). Discounts end at 250% (Maury, Williamson), 300% (Nashville General, Highpoint, Covenant) and 300% (Cookeville, only a 25% discount).
- Interest concentration: all numbers come from the hospitals' own policies, so they are VENDOR-SELF-REPORTED by nature. Policy text is the authority, so I treat that as acceptable here.
- Stage 10.5 (cold assessment) skipped as instructed.

## Method
Source types were primary only: hospital web pages and policy PDFs, plus the TN Health Facilities Commission bed list. Web searches located the pages; pages and PDFs were then fetched by a different call (curl). Where a PDF text layer was garbled or an image, I rendered pages to PNG and read them myself. Searches via a summarizer tool counted as CLOSE-PARAPHRASE at most and were never used as VERIFIED-VERBATIM. No new primary data (calls to billing offices) could be gathered; that is a limitation.

Phase effects (2026-10-17): 8.5 verify - caught that Maury's current page links a policy that expired 9/13/2025, and that Covenant's newer April 2026 policy (image-only) differs in format from the 2024 one. Downgraded Cookeville's "effective date" to NOT-FOUND. 10.5 assess - skipped by instruction.

## Per-hospital table

Beds are from the TN HFC "Hospital Full Bed Listing", updated September 2021 (stale, state source). Ownership is from hospital pages or news. 501(r) applies only to 501(c)(3) hospitals.

| Hospital | Beds (HFC 2021) | Owner / type | Policy URL and date | Free / discount tiers | Status |
|---|---|---|---|---|---|
| Nashville General (Metro Nashville Hospital Authority) | 150 | Metro government hospital authority. 501(r) NOT claimed in the policy. | https://nashvillegeneral.org/sites/default/files/2022-06/Financial_Assistance_Credit_%2B_Collections_Policy_2022.pdf ("2022"; the site still links only this on 2026-10-17). No effective date printed. | 100% under 200% FPG; 80% for 200-300%; 60% for 300-400% | VERIFIED-VERBATIM (policy is 2022, possibly stale) |
| Maury Regional Medical Center (also Marshall, Wayne, MRMG) | 255 (also on its own site) | Not-for-profit system | https://www.mauryregional.com/media/2e3ec7ad758a426a828c390cf79aff09/financial-assistance-charitable-care-policy-09_13_2024.pdf (effective 9/13/2024, shown "Expiration 9/13/2025") | Free at or below 100% FPL; discounted 100-250% FPL; catastrophic care for high expenses | VERIFIED-VERBATIM (web page and rendered PDF) |
| Williamson Medical Center / Williamson Health | 203 | County-origin hospital with a Vanderbilt affiliation (2011); NOT owned by Vanderbilt. Tax status not verified. | https://williamsonhealth.org/content/uploads/2026/02/CHARITY-POLICY-UPDATE-2-18-2026.pdf, "Updated February 18, 2026" | 100% discount to 100% FPL; 90% to 150%; 80% to 175%; 70% to 200%; 60% to 250% | VERIFIED-VERBATIM |
| Cookeville Regional Medical Center | 269 | City-owned, authority-governed (third-party descriptions; not confirmed on a primary page) | https://crmchealth.org/patients-visitors/financial-services/ (policy text is on the page itself; no effective date shown) | 100% at 100% FPL or below; 75% at 101-150%; 50% at 151-200%; 25% at 201-300%; none above 300% | VERIFIED-VERBATIM (date NOT-FOUND) |
| Covenant Cumberland Medical Center, Crossville (Cumberland Co. is one of the 41 Middle TN counties) | 189 | Covenant Health (Knoxville nonprofit). Reference 26 CFR 1.501(r). | https://www.covenanthealth.com/wp-content/uploads/2025/06/3500.070-Financial-Assistance-Policy-English-revised-April-2026.pdf (approved 4/2/26). PLS: .../3500.070-Patient-Account-Services-Charity-Care-Plain-Language-Summary-English-Revised-April-2026.pdf | 100% for 0-200% FPL; 90% for 201-300% | VERIFIED-VERBATIM (policy page images read). Earlier 2024 text also read. |
| Highpoint Health - Sumner (Sumner Regional) | 167 (155 per a news summary) | Lifepoint majority, co-owned with Ascension Saint Thomas | https://www.highpointhealthsystem.com/docs/ahhighpointhealthlibraries/default-document-library/financial-assistance-policy---sumner.pdf (effective 04/2025, last revised 12/2025) | Per plain language summary (below): free at or below 200% FPL; 100% to 60% sliding for 200-300% | Policy VERIFIED-VERBATIM; tiers from the summary |
| Highpoint Livingston Regional (Overton Co.) | 114 | Highpoint (see above) | No separate policy found | n/a | NOT-FOUND |
| Highpoint Riverview, Trousdale | 35, 25 | Highpoint | No separate policy found | n/a | NOT-FOUND (below 100 beds) |
| Highpoint Winchester (formerly Southern TN Regional, Franklin Co.) | 152 | Highpoint site links to /winchester | The Highpoint FAP page lists only the "---sumner" policy | n/a | NOT-FOUND for a Winchester-specific policy |
| Southern TN Regional - Lawrenceburg | 99 | Lifepoint (own site says "formerly Crockett Hospital"); site shares the Lifepoint platform | https://www.southerntnlawrenceburg.com/patients-and-visitors/financial-arrangements has no FAP link | n/a | NOT-FOUND |
| Southern TN Regional - Pulaski | 95 | Lifepoint (site platform) | Only /pay-my-bill and /understanding-your-healthcare-costs found; no FAP | n/a | NOT-FOUND |
| Unity Medical Center, Manchester | 49 | Nonprofit conversion 2019 (news); below the size cutoff | Site domain redirects to a landing page | n/a | UNREACHABLE |
| Tennova Healthcare - Clarksville | 270 | Now Vanderbilt Clarksville Hospital (acquired 2026-02-01/02 per VUMC) | Belongs to the VUMC agent | n/a | Handoff |
| NorthCrest Medical Center | 109 | HCA/TriStar (2021 per TriStar page) | Belongs to the TriStar agent | n/a | Handoff |
| Harton (Tullahoma) | 135 | Vanderbilt Tullahoma-Harton | Belongs to the VUMC agent | n/a | Handoff |
| Starr Regional | n/a | Athens, East TN (not in the 41-county region); not checked | n/a | n/a | Excluded |
| TrustPoint Hospital (Murfreesboro) | 217 psychiatric | Acadia Healthcare (for-profit, own site) | Not found | n/a | NOT-FOUND, low relevance (behavioral) |

## Field detail and quoted evidence

### Nashville General (policy "2022", pdftotext of raw PDF)
- Quote: "Patients who do not qualify for full (100%) financial assistance may qualify for discounts on a sliding fee scale."
- Quote: "60% Discount - 300% - 400% of FPG10% up to $2,500 paid in advance; 80% Discount - 200% - 300% of FPG 5% up to $1,000 paid in advance; 100% Discount - Under 200% of FPG Cost Share of $10 per clinic visits; $100 for non-urgent procedures"
- Uninsured discount: 40% off charges, capped at 175% of cost per TCA 68-11-262.
- Residency: "All recipients of financial assistance must be residents of Davidson County". Non-Davidson residents are not scheduled for elective services.
- Automatic 100% if a Davidson resident "qualify for food stamps" or is certified by an FQHC. 12-month approval for Neighborhood Health Clinic; other approvals are 6 months (policy also says up to 180 days).
- Application window: services within the last 90 days or pending. Decision within 30 days. Appeal within 30 days.
- Insured: under-insured patients "are not eligible for discounting but will be considered on a case by case basis for partial discounting." Patients with access to insurance who do not pay premiums are not eligible.
- Assets: "A spend-down of these assets may be required"; 25% of treatment cost paid before funds apply. Appendix B shows the 2022 FPG table (1 person $13,590).
- Documents: photo ID; two proofs of Davidson address; 3 months of income documents; asset list; expenses; proof of healthcare exemption if income above 138% FPL. Applications via Financial Counseling 615.341.4165 (page), assisted by MedAssist/Firstsource.
- Plain Language Summary: not found. Languages: English and Spanish policy only (Spanish file https://nashvillegeneral.org/sites/default/files/2022-06/Financial_Assistance_Credit_%2B_Collections_Policy_2022_%28SPANISH%29.pdf).
- AGB: not found. The policy does not cite 501(r).
- Presumptive: food stamps and FQHC certification (above).

### Maury Regional
- Page quote (curl text): "Patients of MRH who are U.S. citizens and legal immigrants with annual family incomes of less than 250% of the federal poverty level and without sufficient assets available to meet patient payment obligations will be eligible for MRH financial assistance."
- Page quote: "Free care is available to patients with limited assets and family income equal to or less than the federal poverty level. Discounted care is available to patients with limited assets and family income between the federal poverty level and 250% of the federal poverty level."
- Policy (rendered page images read): Origination 8/27/2014; Effective, Reviewed and Last Revised 9/13/2024; Expiration 9/13/2025. Covers uninsured and underinsured. 6-month qualification period, retroactive to unpaid bills for services in the previous 12 months. Applicability list: MRMC, WMC, MMC, MRMG.
- AGB: "will not exceed the rate paid by the most favored commercial insurance payer." Uninsured discount: 175% of cost per Tennessee law.
- Documents: last tax return and schedules; current proof of income; bank, investment and payment-app statements; retirement; real estate; vehicles; immigrant patients need an active Green Card/Visa; Amish patients need 12 months of records; two certified letters of support if documentation is inadequate.
- Apply: mail to Attn: Financial Counselor, 1224 Trotwood Ave., Columbia TN 38401, or hand-deliver to the Admitting Office. 931.381.1111 option 4. financialcounselor@mauryregional.com.
- Languages: English and Spanish application; Spanish policy dated 10-01-21 on the page. Page says "Not-for-profit". Plain Language Summary: not found. Application window days: not read (pages 6-11 of the policy not read).
- Caveat: the current web page links a policy whose printed expiration (9/13/2025) has passed. I could not find a newer file.
- Note: another agent's browser tab was showing TriStar when I looked; I found no evidence Maury is HCA-owned (the HCA/Maury item in search was an opposition to an HCA hospital, not an acquisition).

### Williamson Medical Center
- Policy says: "Updated February 18, 2026" (original "Effective January 1, 2013"). The prior version, updated May 1, 2023, was also read (125-225% era: 100% at 225% FPL by my arithmetic of $32,805 for one person; that arithmetic is mine, not the document's).
- Table (pdftotext, columns mangled but values readable): 100% discount 0-$15,960 (1 person, 100% FPL); 90% $15,961-$23,940 (150%); 80% $23,941-$27,930 (175%); 70% $27,931-$31,920 (200%); 60% $31,921-$39,900 (250%).
- Eligibility: "any U.S. citizen or legal immigrant ... uninsured, underinsured, ineligible for any government health care benefit program." Residency: "For scheduled procedures, the patient must live within 60 miles of Williamson Medical Center."
- Assets: "Take into account the patient's available assets." Credit reports may be pulled.
- Re-evaluated every 6 months. Incomplete application gets 20 days to complete. Appeal within 30 days. Catastrophic section: partial payment required is 15% to 30% of gross annual income by bracket.
- Uninsured discount: automatic 47% so charges do not exceed 175% of cost, citing TCA-68-11-262.
- Documents (application, May 2025): two paystubs, all pages of the prior-year tax return, 60 days of bank, investment and payment-app statements, proof of dependents; no-income applicants need two notarized letters. Processing "up to two (2) weeks". Mail to Williamson Health, P.O. Box 681868, Franklin TN 37068-1868.
- Not found: AGB, 501(r) statement, Plain Language Summary, other languages, presumptive eligibility.

### Cookeville Regional (page text, curl)
- Quote: "100% or below Federal Poverty Level 100% discount; 101-150% of Federal Poverty Level 75% discount; 151-200% Federal Poverty Level 50% discount; 201-300% Federal Poverty Level 25% discount; 301% and above Federal Poverty Level no discount."
- Quote: "PATIENT MAXIMUM LIABIITY - Amount of total patient liability for patients at 200% of the poverty level or below will not exceed 10% of total household income."
- Residency: only patients in the 14-county service area (Putnam, Jackson, White, Cumberland, Warren, Van Buren, Cannon, Fentress, Overton, Pickett, Smith, Clay, DeKalb, Macon). "Charity care assistance will not apply to accounts with a combined total less than $500."
- Applies to "patients who are not insured through a third party or who are unable to pay in full the balance of their account after exhaustion of all third party liability." Must cooperate in applying for Medicaid. Uninsured not qualifying may get a 25% prompt-pay discount within 60 days of discharge.
- Documents: application plus W-2, tax return, paystubs, bank statements. Approvals over $5,000 need CFO.
- Not found: effective date, AGB, 501(r), Plain Language Summary, languages, application window, asset test (none stated). A "state mandated discount" is applied first. Contact 931-783-2360.

### Covenant Cumberland (April 2026 policy images read by me; 2024 text by curl)
- Policy header: "Effective Date: Jan 99; Revised Date: June 25; Reviewed Date: June 25, March 26, April 26"; final approval signed 4/2/26; Reference "26 C.F.R. 1.501(r)".
- Quote: "at or below 300% of the current federal poverty limits" ; table "0 - 200% of Poverty Limits 100.0%; 201 - 300% of Poverty Limits 90.0%"; 2026 FPL base $15,960 for one person.
- Assets: 10% of net assets added to income; primary dwelling counts only for equity above $100,000. AGB: look-back method, facility percentage in Fair Charges Policy 3500.580 Table II.
- Presumptive: patients referred from community free clinics and mammography voucher program "will be presumed eligible". Approval holds 6 months for new accounts; no new application up to 12 months.
- Apply: application at registration, by mail request at 865-374-3000, or covenanthealth.com. Cumberland PLS (Feb 2021 version, still online): call 931-459-7614; Box 110, 421 South Main St, Crossville. Spanish policy, PLS and application exist.
- Application window: not stated.
- Note: the covenanthealth.com Cumberland page returned 403/404 to curl; the policy page was read via a summarizer (CLOSE-PARAPHRASE for link list only); document text itself is verbatim.

### Highpoint Health - Sumner
- Policy header: Origination 01/2024, Approved/Effective 04/2025, Last Revised 12/2025, applicability "Sumner Regional Medical Center". Policy text: "Eligibility is generally determined by measuring a patient's gross family income against the Federal Poverty Guidelines".
- Applies to "uninsured patients" only. Plain Language Summary: "Uninsured patients whose family income is equal to or less than 200% of the Federal Poverty Guidelines are generally eligible for free emergency and medically necessary care. Uninsured patients whose family income is between 200% and 300% of the Federal Poverty Guidelines generally receive a sliding scale discount ranging from 100% to 60%."
- Window: "Submitting a complete Financial Assistance Application with supporting documentation within 60 days from receiving service." Determination about 30 business days; eligibility lasts up to 12 months.
- AGB: look-back method. Undocumented residents and patients without a home address may apply. Spanish policy, PLS, application and billing policy are on the site.
- Apply: Patient Financial Services, PO Box 1558, Gallatin TN 37066; 615-328-8888; 555 Hartsville Pike.
- The discount guidelines 2025 attachment is an image I did not open; tiers rely on the PLS.

## Verification table (load-bearing claims)
| Claim | Source | Verdict |
|---|---|---|
| NGH free at <200% FPG, 80% at 200-300%, 60% at 300-400% | NGH 2022 PDF, pdftotext | VERIFIED-VERBATIM |
| Maury eligibility under 250% FPL; free at 100% | Maury web page, curl text | VERIFIED-VERBATIM |
| Maury policy effective 9/13/2024, expires 9/13/2025 | Rendered PDF page 1 | VERIFIED-VERBATIM |
| WMC tiers 100/90/80/70/60% to 250% FPL, updated 2/18/2026 | WMC PDF, pdftotext | VERIFIED-VERBATIM |
| Cookeville 100/75/50/25% tiers | CRMC page, curl | VERIFIED-VERBATIM |
| Covenant 100% to 200%, 90% to 300%, April 2026 | Rendered PDF pages 1, 2, 4 | VERIFIED-VERBATIM |
| Highpoint Sumner free to 200%, sliding to 300% | Highpoint PLS PDF, pdftotext | VERIFIED-VERBATIM |
| Tennova Clarksville is now Vanderbilt Clarksville | VUMC news via search summary | CLOSE-PARAPHRASE (second source, Chief Healthcare Executive, agrees) |
| NorthCrest is TriStar since 2021 | TriStar and Becker's via search summary | CLOSE-PARAPHRASE |
| Highpoint is Lifepoint-majority, Ascension JV | Lifepoint/Ascension releases via search summary; Highpoint site wording "with Ascension Saint Thomas" confirmed by curl | CLOSE-PARAPHRASE (plus verbatim naming) |
| Beds per hospital | TN HFC bed listing, Sept 2021, pdftotext | VERIFIED-VERBATIM, STALE (2021) |

## Numbers register
| Number | Claim | Source | Date | Interest class | Verdict |
|---|---|---|---|---|---|
| 200/300/400% FPG | NGH tiers | NGH policy | 2022 | VENDOR-SELF-REPORTED | VERBATIM |
| 100%, 250% FPL | Maury free and discount limits | Maury | 2024 | VENDOR-SELF-REPORTED | VERBATIM |
| 100/150/175/200/250% FPL | WMC tiers | WMC | 2026-02-18 | VENDOR-SELF-REPORTED | VERBATIM |
| 100/150/200/300% FPL, 10% income cap | CRMC tiers | CRMC page | undated | VENDOR-SELF-REPORTED | VERBATIM |
| 200%, 300% FPL | Covenant | Covenant | 2026-04 | VENDOR-SELF-REPORTED | VERBATIM |
| 200%, 300%, 60 days | Highpoint Sumner | Highpoint | 2025 | VENDOR-SELF-REPORTED | VERBATIM |
| 175% of cost / 47% automatic discount | Uninsured cap (TCA 68-11-262) | WMC, NGH, Maury policies | various | VENDOR-SELF-REPORTED (statute cited) | VERBATIM |
All numbers are hospital self-reports, so interest concentration is 100%; they are the legal policy documents, not marketing claims.

## Thin / missing
- Current Maury policy after 9/13/2025 expiry: searched the Maury site (financial assistance page, media links); only the 2024 file is linked. Pages 6-11 of Maury's policy (application window, appeals) were not read.
- Nashville General: any policy newer than 2022 - searched the site billing page and the policy links; only the 2022 files exist. No Plain Language Summary on its site.
- STRHS Lawrenceburg and Pulaski, Highpoint Livingston/Riverview/Trousdale/Winchester: no FAP. Searches: web search "Southern Tennessee Regional Health System Lawrenceburg Winchester Pulaski financial assistance policy"; "southerntnlawrenceburg.com financial assistance policy plain language summary"; "Southern Tennessee Regional Health System Financial Assistance Policy ... Crockett Hospital"; direct URL guesses (/financial-assistance, /patient-financial-assistance, /billing-and-insurance, and the equivalents on southerntnpulaski.com) all 404; /patients-and-visitors/financial-arrangements has no FAP text. A directory (Turquoise) calls Lawrenceburg "voluntary non-profit" but I could not confirm this, and the site platform and "formerly Crockett Hospital" suggest Lifepoint; ownership of STRHS Lawrenceburg/Pulaski is UNVERIFIED.
- Unity Medical Center and Livingston Regional: their old domains redirect to a "/lander" parking page (UNREACHABLE). Searches: "Unity Medical Center Manchester Tennessee hospital owner beds financial assistance"; "Livingston Regional Hospital Tennessee owner Lifepoint Highpoint financial assistance policy" (found only the unrelated Livingston HealthCare, Montana).
- TrustPoint Hospital (Acadia): "TrustPoint Hospital Murfreesboro financial assistance policy charity care owner" found nothing.
- Lincoln Medical Center (Fayetteville, 49 beds), Jamestown Regional and other small hospitals: not checked (under about 100 beds).
- State licensed beds: only a September 2021 list; a current state source was not found (tn.gov JAR pages 404).
- Cookeville ownership and 501(r) status: third-party descriptions only. WMC tax status unverified.
- Plain Language Summaries found only at Covenant and Highpoint. Not found at NGH, Maury, WMC, CRMC.
- Primary-data gap: unspecified items (actual practice, denial rates) would need calls or records requests.

## What would change this
A newer Maury or NGH policy, a Highpoint policy for Winchester/Livingston, or a published STRHS FAP would change the table. Confirming WMC and CRMC tax status would change which are subject to 501(r).

## Sources (accessed 2026-10-17)
- https://nashvillegeneral.org/patient-visitor-info/billing-insurance and its 2022 policy PDF (above)
- https://www.mauryregional.com/billing-and-insurance/financial-assistance/ and policy PDF (above); https://www.mauryregional.com/about-us/
- https://williamsonhealth.org/patients-and-visitors/patient-information/patient-financial-information/; policy https://williamsonhealth.org/content/uploads/2026/02/CHARITY-POLICY-UPDATE-2-18-2026.pdf; application https://williamsonhealth.org/content/uploads/2025/05/2025.05-Financial-Assistance-App_combined.pdf; prior version https://williamsonmedicalcenter.org/wp-content/uploads/2023/04/CHARITY-POLICY-UPDATE-5-1-23.pdf
- https://crmchealth.org/patients-visitors/financial-services/
- https://www.covenanthealth.com/patients-visitors/financial-assistance/ (via WebFetch) and the April 2026 policy PDF; 2024 policy https://covenanthealth.com/wp-content/uploads/2024/11/Financial-Assistance-Policy-English-updated-2024.pdf
- https://www.highpointhealthsystem.com/patient-financial-assistance, policy and plain language summary under /docs/ahhighpointhealthlibraries/default-document-library/
- https://www.southerntnlawrenceburg.com (about, financial-arrangements); https://www.southerntnpulaski.com
- TN HFC https://www.tn.gov/content/dam/tn/hfc/documents/HFC-Hospital_Full_Beds_Report_September2021.pdf
- Ownership via web search summaries: VUMC news (https://news.vumc.org/2026/02/02/vanderbilt-health-acquires-tennovas-clarksville-hospital-and-related-physician-clinics-from-community-health-systems), Lifepoint/Ascension JV (https://www.businesswire.com/news/home/20231201970776/en/Lifepoint-Health-and-Ascension-Saint-Thomas-Partner-to-Advance-Healthcare-for-Middle-Tennesseans), TriStar NorthCrest (https://www.tristarhealth.com/locations/tristar-northcrest-medical-center/about-us).

Scratch files (not in the project): <session scratchpad>\ (mtn\ downloads, png_cov26, png_maury, pdf2png.ps1).
