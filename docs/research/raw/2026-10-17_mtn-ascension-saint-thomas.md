# Middle TN hospitals: Ascension Saint Thomas FAP

> Raw subagent report, saved verbatim (non-ASCII transliterated) on 2026-10-17.
> Not yet reviewed or cold-assessed by the orchestrator; numbers are as the agent reported them.
> Source transcript agent id: aa3e9da8c93927423

# Ascension Saint Thomas (Middle TN) - Financial Assistance Policy research
Access date: 2026-10-17 (all fetches that day). Audience: Evan / TNHacks27 "Bill to Help" study. Method: raw PDFs downloaded with curl and read via pdftotext (the documents' own text, so VERBATIM is legitimate). WebFetch was tried on the FAP PDF and could not read it ("raw, compressed PDF"), so it contributed nothing. Stage 10.5 skipped per orchestrator instruction. No file written.

## TL;DR
- ONE policy covers the whole Ascension Saint Thomas hospital family: "Saint Thomas Health dba Ascension Saint Thomas" FAP, dated July 1, 2025. Free care at <=250% FPL, sliding-scale discount to 400% FPL (86/81/79% write-off), "means test" above 400%, asset test at 250% FPL, 240-day application window, presumptive scoring, 13-county residency limit, AGB capped at 20% of gross charges.
- Two exceptions have SEPARATE, different policies: Ascension Saint Thomas Behavioral Health Hospital (Acadia JV, policy dated 5/12/21) and Ascension Saint Thomas Rehabilitation Hospital (Charity Care policy dated 01/06/2023, discount tiers 95/90/85%, not 86/81/79%).
- Biggest practical flaw: the "Community" residency limit is 13 counties, not the 41-county region. A patient outside those 13 is not covered by the text, except for continuity of care from another Ascension facility. Each Saint Thomas hospital's own county is inside the 13.
- Licensed beds NOT found from a state source. Only secondary staffed-bed figures (Wikipedia, AHD). Defer to the mtn-census agent.
- Source-interest: every policy number is VENDOR-SELF-REPORTED (the hospital's own document). This shows what the policy says, not how it is applied.

## 1. Policy-coverage answer
The main FAP (https://healthcare.ascension.org/-/media/healthcare/financial-assistance/tennessee/tnnas/fap/runningfile_tnnas_english_financial-assistance-policy.pdf) names these entities, VERIFIED-VERBATIM:
"Saint Thomas DeKalb Hospital, LLC, dba Ascension Saint Thomas DeKalb; Saint Thomas Hickman Hospital, dba Ascension Saint Thomas Hickman; Saint Thomas Highlands Hospital, LLC, dba Ascension Saint Thomas Highlands; Saint Thomas River Park Hospital, LLC, dba Ascension Saint Thomas River Park; Saint Thomas Rutherford Hospital, dba Ascension Saint Thomas Rutherford; Saint Thomas Midtown Hospital; Saint Thomas Stones River Hospital, LLC, dba Ascension Saint Thomas Stones River; Saint Thomas West, dba Ascension Saint Thomas Hospital, Ascension Saint Thomas Midtown, Ascension Saint Thomas West, Ascension Saint Thomas Three Rivers. Ascension Saint Thomas Hospital for Specialty Surgery."
So 10 facilities: Midtown, West, Rutherford, River Park, DeKalb, Highlands, Stones River, Hickman, Three Rivers, Hospital for Specialty Surgery. The Ascension site page lists the same 10 (names "Ascension Saint Thomas Hospital for Specialty Surgery"; the phone list calls it "Center for Specialty Surgery"). It also lists Stones River Behavioral Health and Highlands Behavioral Health (units, 615-563-3141) and Rutherford Westlawn (satellite of Rutherford; Wikipedia, AHD).
The site page says separately: "For the financial assistance documents for Ascension Saint Thomas Behavioral Health Hospital click below" and the same for the Rehabilitation Hospital.
Page oddity: the page text says these documents "cover services provided at Ascension Saint Thomas locations in Indiana and Kentucky" - an obvious copy-paste error on Ascension's page, though the PDFs are Tennessee.

## 2. Per-hospital table
Beds: staffed beds only, NOT licensed. W = Wikipedia table; A = AHD (cost-report-based, year unstated). Both secondary and unverified. Single-source each; they disagree, which shows these are not licensed counts.

| Facility | City / county | Staffed beds W / A | FAP covering it | AGB (look-back, calc) | Phone on PDF summary (Apr 2025) | Phone on website (2026-10-17) |
|---|---|---|---|---|---|---|
| Ascension Saint Thomas Hospital Midtown | Nashville / Davidson | 396 / 449 | Main FAP | 22.6% (shared with West) | 615-284-5340 | 800-242-7416 |
| Ascension Saint Thomas Hospital West | Nashville / Davidson | 643 / 704 | Main FAP | 22.6% | 615-222-6638 | 800-242-7416 |
| Ascension Saint Thomas Rutherford | Murfreesboro / Rutherford | 354 / 408 | Main FAP | 28.4% | 615-222-6638 | 800-242-7416 |
| Ascension Saint Thomas River Park | McMinnville / Warren | 82 / 61 | Main FAP | 32.8% | 877-348-7082 | 877-348-7082 |
| Ascension Saint Thomas DeKalb | Smithville / DeKalb | 18 / 18 | Main FAP | 47.1% | 877-348-7082 | 877-348-7082 |
| Ascension Saint Thomas Highlands | Sparta / White | 26 / 28 | Main FAP | 34.0% | 877-348-7082 | 877-348-7082 |
| Ascension Saint Thomas Stones River | Woodbury / Cannon | 43 / 41 | Main FAP | 41.3% | 877-348-7082 | 877-348-7082 |
| Ascension Saint Thomas Hickman | Centerville / Hickman | none listed | Main FAP | 74.5% | 931-729-6800 | 931-729-6800 |
| Ascension Saint Thomas Three Rivers | Waverly / Humphreys | none listed | Main FAP | 35.0% | 931-296-0251 | 931-296-0266 |
| Ascension Saint Thomas Hospital for Specialty Surgery | Nashville / Davidson | - / 23 | Main FAP | 30.0% | 615-341-7480 | 615-341-7500 |
| Ascension Saint Thomas Behavioral Health Hospital | Nashville (300 Great Circle Rd) | 76 originally reported (Becker's), Acadia page says 90 - unresolved | OWN FAP (5/12/21) | prospective method, Medicare FFS, 37.43% (calc year 2025; doc dated 29/05/2026) | - | 629-216-2163 |
| Ascension Saint Thomas Rehabilitation Hospital | Nashville (310 21st Ave N) | not found | OWN Charity Care policy (01/06/2023) | not read | - | 629-253-5300 (per its policy) |

Phone numbers differ between the PDF summary and the website (and Medical Group: 844-686-2555 on the summary vs 833-263-9791 on the website). A site that publishes two numbers per hospital is a finding; confirm before telling patients which to call. Midtown also has a 683 licensed-bed figure from search snippets (a TN legislative resolution, UTHSC, Wikipedia); I could not open the resolution (HTTP 403), so that is UNVERIFIED and a lead for mtn-census only.

## 3. Main FAP fields (one policy, all 10 facilities)
Document: "Saint Thomas Health FINANCIAL ASSISTANCE POLICY July 1, 2025". Host Last-Modified: 2025-10-02. Re-download confirmed byte-identical, 150,481 bytes.

| Field | Finding | Status |
|---|---|---|
| Free care | <=250% FPL | VERIFIED-VERBATIM |
| Discount tiers | 251-300% FPL: 86%; 301-350%: 81%; 351-400%: 79% assistance | VERIFIED-VERBATIM (and in Spanish FAP) |
| Above 400% FPL | "Means Test": discount only if total medical debt (Ascension plus any other provider) >= household gross income; discount level = that of a patient at 400% FPL (79%) | VERIFIED-VERBATIM |
| Insured vs uninsured | Applies "on that portion of the charges ... for which the Patient is responsible following payment by an insurer, if any" so insured patients qualify. Out-of-network insurance plans can reduce or deny assistance. Uninsured must work with a financial counselor to apply for Medicaid. | VERIFIED-VERBATIM |
| Asset test | Yes. "A Patient with such assets that exceed that exceed 250% of such Patient's FPL amount may not be eligible" (the doubled "that exceed" is in the original); "may", not "will" | VERIFIED-VERBATIM |
| Residency | Limited to the 13-county "Community": Cannon, Davidson, Dekalb, Hickman, Rutherford, Warren, White, Montgomery, Putnam, Sumner, Williamson, Wilson, Humphrey. Also deemed in if continuity of care from another Ascension facility where the patient already qualified. The text says "twelve (13) Counties" (typo). | VERIFIED-VERBATIM |
| Application window | "on or prior to the 240th day after the Patient's first discharge bill"; later still allowed, but then assistance is "limited to Patient's unpaid balance after taking into account any payments made". Billing policy separately says a patient "may submit a FAP Application at any time". FAP and BCP are loosely inconsistent. | VERIFIED-VERBATIM |
| Presumptive eligibility | Yes, "presumptive scoring" within 240 days of first discharge bill, 100% charity only, applies to that episode of care only. If scored below the most generous tier, patient is told and given time to apply (BCP). | VERIFIED-VERBATIM |
| Documents required | Not in the FAP. Application cover letter: 3 most recent paystubs; most recent tax return (all schedules if self-employed); SS/pension award letter; parent tax return if dependent under 25; unemployment receipt; Medicaid approval/denial; bank statements last 3 months; investments, trusts, money market, mutual funds; optional outstanding medical-bill proof. "We are unable to process or consider applications that are not complete." | CLOSE-PARAPHRASE (list), quote VERBATIM |
| Prior application | Application completed <6 months before eligibility determination may be used; older not | VERIFIED-VERBATIM |
| Nominal fee | "may not exceed the lesser of (a) AGB or (b) the greater of $20 or 10% of the amount for which the patient will be responsible" | VERIFIED-VERBATIM |
| Appeal | 14 calendar days from denial notice; to Ascension Saint Thomas Financial Assistance Department, P O. Box 100983, Atlanta GA 30384 | VERIFIED-VERBATIM |
| Non-FAP help | Uninsured not eligible get the highest-paying-payor discount; prompt-pay discount; uninsured never charged more than 175% of cost per T.C.A. 68-11-262 | VERIFIED-VERBATIM |
| AGB method / % | Look-back method incl. Medicare FFS plus all private insurers. AGB PDF ("Updated July 1, 2026"; host Last-Modified 2026-06-19) lists per-facility calculated percentages (table above) but then: "Saint Thomas Health has chosen to apply a lower AGB percentage for all of the facilities, medical groups, and lab as follows: AGB: 20%". So eligible patients are billed at most 20% of gross charges. | VERIFIED-VERBATIM |
| Services covered | Emergency and other medically necessary care "including employed physician services and behavioral health"; non-employed providers per "List of Providers Covered" (dated 10/1/2026). | VERIFIED-VERBATIM |
| Effective date | Document says July 1, 2025. I found no newer FAP; the AGB (July 2026), application (file modified 2026-09-16) and provider list (10/1/2026) are newer than the FAP. Staleness risk: FAP could be re-issued without a visible date change since file name is "runningfile". | VERIFIED-VERBATIM for date; "current" is inference |
| Application form | Paper: https://healthcare.ascension.org/-/media/healthcare/financial-assistance/tennessee/tnnas/fap-application/runningfile_tnnas_english_financial-assistance-application.pdf ; online: https://ascension.forms.r1rcm.com/stthomas/fa (button "Start Application"; I did not read the form content). Mail to PO Box 100983 Atlanta GA 30384 (hospital) or Lockbox 713441, Chicago IL 60686 (Medical Group). Patient reps 931-738-2669. Form asks for household income, expenses, assets; SSN optional. | VERIFIED-VERBATIM |
| Plain Language Summary | https://healthcare.ascension.org/-/media/healthcare/financial-assistance/tennessee/tnnas/plain-language-summary/runningfile_tnnas_english_financial-assistance-policy-summary.pdf , dated April 1, 2025 (host Last-Modified 2025-03-28), i.e. it predates the July 2025 FAP. Its mail-request address is PO Box 504475, St Louis MO 63150-0001, different from the FAP's Atlanta box. | VERIFIED-VERBATIM |
| PLS languages | The PDF itself lists 7: Arabic, Korean, Laotian, Simplified Chinese, Spanish, Traditional Chinese, Vietnamese. The website posts English + 10 non-English (adds Farsi, French, German). Rehab hospital lists 5 translations on its site. | VERIFIED-VERBATIM (PDF), page links read from HTML |
| Billing and collections (ECA) | See section 4 | VERIFIED-VERBATIM |

Key quote (eligibility): "Patients with income less than or equal to 250% of the Federal Poverty Level income ('FPL'), will be eligible for 100% charity care on that portion of the charges for services for which the Patient is responsible following payment by an insurer, if any". Sliding scale quote: "Patients between 251% FPL and 300% FPL will receive 86% assistance / Patients between 301% FPL and 350% FPL will receive 81% assistance / Patients between 351% FPL and 400% FPL will receive 79% assistance".

## 4. Billing and Collection Policy (ECA)
URL: https://healthcare.ascension.org/-/media/healthcare/financial-assistance/tennessee/tnnas/billing-collection-policy/runningfile_tnnas_english_health-billing-and-collection-policy.pdf . Dated April 1, 2025; host Last-Modified 2026-04-21. Covers the same facility list as the FAP.
- ECAs defined: sale of debt, credit reporting, deferring/denying care for nonpayment, liens, foreclosure, levies, lawsuits, wage garnishment.
- Quote: "The Organization rarely utilizes extraordinary collection actions, or 'ECAs'... may use ECAs in extreme circumstances", defined to include elective non-medically-necessary balances, patients with "substantial resources (e.g., high net worth)" refusing to pay, or "intentional abuse" of the FAP. "The Organization does not use ECAs for accounts that have a remaining balance due to qualifying for only partial financial assistance... or with respect to co-pays on accounts that have qualified for full financial assistance". Final authority: Ascension SVP / Chief Revenue Officer, case by case.
- Timing: no ECAs for at least 120 days from first post-discharge bill; then written notice with deadline no earlier than 30 days, plus PLS and oral notice. Incomplete application: 30 calendar days to fix. Decision within 45 calendar days. Appeal 14 days. Refunds of overpayment unless under $5. ECAs reversed if later approved.
Note: "may" is permissive; the policy bans ECAs only on partially assisted and fully-assisted copays, not on patients who simply never applied.

## 5. Separate-policy facilities
Behavioral Health Hospital (Cumberland Behavioral Health, LLC): FAP "5/12/21", host Last-Modified 2023-12-19. Same shape (250% free; 400% cap; means test; asset test 250%; 240 days; presumptive scoring) but only 12 counties (no Humphrey), nominal fee up to $20, appeals/requests go to Great Circle Rd Nashville (not Atlanta), AGB by prospective Medicare FFS method (37.43%). The 86/81/79 table is missing from the extracted text (it says "ASTBHH utilizes the prospective model for AGB calculation" in its place); footnote digits corrupt several percentages ("2505%"). Per WPLN (search snippet, not opened) the hospital is an Acadia JV that "will lose tax exempt status but retain nonprofit mission" - so IRS 501(r) may not bind it; UNVERIFIED lead.
Rehabilitation Hospital: Charity Care policy 01/06/2023 (host Last-Modified 2025-02-03), hosted on its own site (https://www.ascensionsaintthomasrehabhospital.com/patient-experience/financial-assistance , policy at /docs/zirfascensionsaintthomasrehabhospitallibraries/fap/charity-care-policy.pdf). 13 counties, 250% free, sliding scale: "Patients between 251% FPL and 300% FPL will receive 95% assistance / 301% FPL and 351% FPL will receive 90% / 351% FPL and 400% FPL will receive 85%". The 351% FPL appears in both tier 2 and 3 - an overlap error in the source. Operator/JV partner not stated on the page; not verified.

## 6. Ownership changes
- Williamson Health (Williamson Medical Center, Franklin, County-owned): board voted July 2026 to sell to Ascension Saint Thomas ($700M base, about $900-950M with commitments). Status per MedCity News (WebFetch summary, CLOSE-PARAPHRASE at best): County Commission vote not scheduled, TN AG sign-off needed, close expected 2027-2028. Williamson County is already in the FAP Community. Not an Ascension hospital today.
- Lifepoint JV (December 2023, "Highpoint Health"): AHD lists "Highpoint Health - Sewanee with Ascension Saint Thomas" and "Winchester with Ascension Saint Thomas". These are NOT named in the FAP above; treat as outside Ascension Tennessee FAP. UNVERIFIED lead (search snippet and AHD only).
- Older: 2016 Ascension/Saint Thomas bought out four hospitals from a JV (Capella) = River Park, DeKalb, Stones River, Highlands (headline "Saint Thomas Health Adds 4 Tennessee Hospitals", about.ascension.org; not opened). Midtown was Baptist; Rutherford was Middle Tennessee Medical Center (Wikipedia).
- No facility sale/closure by Ascension Saint Thomas found in 2026 (two searches).

## 7. Verification table (stage 8.5)
Load-bearing claim | Source | Verdict
- 250% FPL free care | FAP PDF, re-downloaded byte-identical (cmp), plus separate Spanish FAP | VERIFIED-VERBATIM
- 86/81/79 tiers to 400% | FAP PDF + Spanish FAP (independent translation file) | VERIFIED-VERBATIM
- 240-day window, presumptive scoring | FAP PDF (6 hits for "240th day") | VERIFIED-VERBATIM
- Asset test 250% FPL | FAP PDF; Spanish FAP; PLS | VERIFIED-VERBATIM
- 13-county Community | FAP, PLS, Rehab policy | VERIFIED-VERBATIM
- AGB 20% floor | AGB PDF | VERIFIED-VERBATIM
- ECA rules | BCP PDF | VERIFIED-VERBATIM
- Facility list | FAP, BCP, PLS, website HTML | VERIFIED-VERBATIM
- Rehab 95/90/85 tiers | Rehab policy PDF | VERIFIED-VERBATIM
- Licensed beds | no state source | NOT-FOUND (provisional; state source not reached)
- Williamson sale | MedCity via WebFetch, plus WebSearch snippets | CLOSE-PARAPHRASE
- BHH JV/for-profit status, Lifepoint JV | search snippets only | UNVERIFIED

## 8. Numbers register
| Number | Claim | Source | Date | Class | Verdict |
|---|---|---|---|---|---|
| 250% FPL | free care ceiling | Ascension FAP | 2025-07-01 | VENDOR-SELF-REPORTED | VERBATIM |
| 86/81/79% | sliding scale write-off | Ascension FAP | 2025-07-01 | VENDOR-SELF-REPORTED | VERBATIM |
| 400% FPL | sliding scale / means-test boundary | Ascension FAP | 2025-07-01 | VENDOR-SELF-REPORTED | VERBATIM |
| 250% FPL | asset test | Ascension FAP | 2025-07-01 | VENDOR-SELF-REPORTED | VERBATIM |
| 240 days | application window | Ascension FAP | 2025-07-01 | VENDOR-SELF-REPORTED | VERBATIM |
| 20% | AGB cap applied to all | Ascension AGB | 2026-07-01 | VENDOR-SELF-REPORTED | VERBATIM |
| 22.6-74.5% | per-hospital calculated AGB | Ascension AGB | 2026-07-01 | VENDOR-SELF-REPORTED | VERBATIM |
| 120 / 30 / 45 / 14 days | ECA wait / notice / decision / appeal | Ascension BCP | 2025-04-01 | VENDOR-SELF-REPORTED | VERBATIM |
| $20 or 10% | nominal fee cap | Ascension FAP | 2025-07-01 | VENDOR-SELF-REPORTED | VERBATIM |
| 175% of cost | uninsured charge cap (T.C.A. 68-11-262) | Ascension FAP | 2025-07-01 | VENDOR-SELF-REPORTED | VERBATIM |
| staffed beds (396, 643, 354, 82, 18, 43, 26) | beds | Wikipedia table | unstated | UNVERIFIABLE | single-source |
| staffed beds (449, 704, 408, 61, 18, 41, 28, 23) | beds | AHD | unstated | UNVERIFIABLE | single-source |
| 683 | Midtown licensed beds | search snippets | - | UNVERIFIABLE | not opened |
| $700M | Williamson sale price | MedCity | 2026-07 | INDEPENDENT (press) | CLOSE-PARAPHRASE |

Structural checks: Interest concentration = 100% of policy numbers are vendor self-reported (disclosed in TL;DR). Same-source dependency: all FAP, PLS, BCP, AGB documents come from one issuer; the Spanish copy is a translation of the same document, not an independent source. The "Asset test" and "means test" are discretionary ("may"), so the policy text overstates certainty about who is actually denied.

## 9. Findings vs interpretation
Findings (stated above). Interpretation, not verified: the 20% AGB floor is generous relative to the calculated 22.6-74.5% figures, so FAP patients are effectively charged at most 20% of list price; the 13-county limit and asset test are the main eligibility barriers for a user from the wider 41-county region; Hickman's 74.5% calculated AGB shows why the blanket 20% matters there.

## 10. Thin / missing
- Licensed beds per hospital from the TN Dept of Health / Joint Annual Report: not found. Searches: "Tennessee Department of Health hospital joint annual report licensed beds Saint Thomas Midtown" and "Ascension Saint Thomas hospitals licensed beds ..." returned only secondary sources; tnsosfiles resolution blocked (403). No second-way run against the TDH site itself.
- Rehab hospital: AGB, billing policy, operator/JV partner, bed count not read.
- BHH: covered-provider list, billing policy, and the sliding-scale table (garbled/missing in extracted text) not read.
- The online application's form fields (r1rcm) were not opened.
- Whether the July 2025 FAP is still the live version: no newer one found, but no changelog exists.
- Practice vs policy (approval rates, denial reasons): needs IRS Form 990 Schedule H or a patient-experience study; not collected.

## 11. What would change this
A newer FAP posted under the same "runningfile" URL; a Schedule H showing charity care is much lower than the policy implies; confirmation that BHH is for-profit (501(r) not binding); Williamson transaction closing (new hospital under this FAP).

## 12. Effect log (2026-10-17)
8.5 verify - added a limitation: WebFetch could not read the PDF at all (so VERBATIM came only from pdftotext), caught the PLS-vs-website language mismatch and the FAP-vs-BCP window inconsistency; flipped no verdict.
10.5 assess - skipped by instruction.

## 13. Sources (accessed 2026-10-17)
- https://healthcare.ascension.org/financial-assistance/tennessee (page: "Financial assistance at Ascension Saint Thomas in TN")
- FAP, PLS, application, BCP, AGB, covered-providers PDFs under https://healthcare.ascension.org/-/media/healthcare/financial-assistance/tennessee/tnnas/ (fap/, plain-language-summary/, fap-application/, billing-collection-policy/, agb/, covered-providers-list/; English file names runningfile_tnnas_english_*)
- Spanish FAP: .../tnnas/fap/runningfile_tnnas_spanish_financial-assistance-policy.pdf
- BHH: https://healthcare.ascension.org/-/media/healthcare/financial-assistance/tennessee/behavioral-health-hospital/fap/runningfile_tnnas_behavioral_health_english_financial-assistance-policy.pdf and .../agb/runningfile_tnnas_behavioral_health_english_amount-generally-billed-calculation.pdf
- Rehab: https://www.ascensionsaintthomasrehabhospital.com/patient-experience/financial-assistance and /docs/zirfascensionsaintthomasrehabhospitallibraries/fap/charity-care-policy.pdf
- Online application: https://ascension.forms.r1rcm.com/stthomas/fa
- https://en.wikipedia.org/wiki/Ascension_Saint_Thomas ; https://www.ahd.com/states/hospital_TN.html (staffed beds)
- https://medcitynews.com/2026/07/ascension-tennessee-health-system-merger/ ; WebSearch results for WSMV, Becker's, WPLN, Acadia (snippets only)
Working copies of the PDFs are in the session scratchpad ...\scratchpad\asc\ (not project files).
