# Middle TN hospital census and 75% cut (mtn-census)

> Raw subagent report, saved verbatim (non-ASCII transliterated) on 2026-10-17.
> Not yet reviewed or cold-assessed by the orchestrator; numbers are as the agent reported them.
> Source transcript agent id: a2d1e0252d598b395

# Middle Tennessee acute-care hospitals holding 75% of licensed beds (census + cut)

Date: 2026-10-17 (data pulled ~23:30-23:55 CDT, UTC-5). Part of the 5-agent study; this is the census and the cut. No files written to the project (scratch only). For: orchestrator, who compiles the final brief and hands the cut list to the 4 policy-collection agents.

## Definitions (as used)
- **Middle Tennessee** = the 41 counties of the Middle Grand Division in TCA 4-1-201, as published on the tn.gov directory page (second source: Wikipedia wikitext, same 41).
  - Counties: Bedford, Cannon, Cheatham, Clay, Coffee, Davidson, DeKalb, Dickson, Fentress, Franklin, Giles, Grundy, Hickman, Houston, Humphreys, Jackson, Lawrence, Lewis, Lincoln, Macon, Marshall, Maury, Montgomery, Moore, Overton, Perry, Pickett, Putnam, Robertson, Rutherford, **Sequatchie**, Smith, Stewart, Sumner, Trousdale, Van Buren, Warren, Wayne, White, Williamson, Wilson.
  - **Cumberland County is East Tennessee by statute**, so Cumberland Medical Center (Crossville, 189 beds) is OUT. The Tourism site's looser definition includes Cumberland; see sensitivity G.
- **Hospital** = hospital licensed by the state Health Facilities Commission (HFC) as a general acute-care hospital, including critical access hospitals (CAH).
  - **Excluded, licensed but not acute:**
    - Encompass Health Rehab Hospital of Franklin (40, rehab).
    - Ascension Saint Thomas Rehabilitation Hospital (40, rehab).
    - Vanderbilt Stallworth Rehabilitation Hospital (80, rehab).
    - Select Specialty Hospital - Nashville (100, long-term acute care).
    - Trustpoint Hospital, Murfreesboro (217, 175 psychiatric, Acadia).
  - **Excluded, other:**
    - Psychiatric hospitals outside the HFC file: Middle TN Mental Health Institute, Ascension Saint Thomas Behavioral Health, Rolling Hills, Pinewood Springs, Behavioral Healthcare Center Clarksville and Columbia.
    - VA Middle Tennessee (Nashville and Murfreesboro).
    - Closed or inactive: Jamestown TN Medical Center (85, Licensed-Inactive) and Cumberland River Hospital, Celina (33, see Thin/missing).
    - Rural Emergency Hospitals (0 inpatient beds): TriStar Ashland City, Wayne Medical Center.
    - 8 "Closed - Satellite" license rows.
    - Freestanding ERs (not enumerated).
- **Size measure** (one measure throughout the main ranking) = **"Total_Beds" on the HFC Hospital Full Bed Report, July 2026.**
  - File: https://www.tn.gov/content/dam/tn/hfc/documents/HFC-Hospital_Full_Bed_Report_July2026.xlsx. HTTP Last-Modified 2026-08-10; sha256 ba0f84e4...eac693, identical on a second download.
  - It is a licensed-bed count, not staffed.
  - It includes psychiatric, rehab, NICU and swing units that sit inside a general-hospital license (e.g. VUMC 106 psych, Centennial 132 psych).
- **Multi-campus licenses are counted once per license, as the state does.**
  - Saint Thomas West + Midtown = license #24 = 1,184.
  - Rutherford (#100, 478) includes the Westlawn campus and now Stones River (Woodbury, Cannon).
  - Skyline (#23) includes Madison.
  - Hendersonville (#135) includes Portland Medical Park.
  - Highpoint Winchester (#139) includes Sewanee.
  - Vanderbilt Wilson County (#137) is a two-campus license.
  - VUMC (#27) includes the adult, Children's and Psychiatric hospitals.
- Secondary measures, used only as labeled sensitivities, never mixed into the main ranking:
  - JAR FY2024: hospital self-reported licensed and staffed "adult and pediatric" beds. Scope varies by reporter, so cross-check only.
  - Total minus psychiatric, rehab and alcohol/drug beds (the "ex-psych/rehab" column below).

## TL;DR
- **Hypothesis H1 (a small core set holds 75%) mostly survived.**
  - On the main measure, 75% of 8,149 licensed beds (38 operating acute licenses) is reached at the 13th hospital.
  - After 12 hospitals the share is 74.7%; TriStar Hendersonville takes it to 76.7%.
- **The line is knife-edge.**
  - The first nine are inside under every variant I ran: VUMC; Ascension Saint Thomas West/Midtown; TriStar Centennial; Ascension Saint Thomas Rutherford; TriStar Skyline; Williamson Medical Center; Cookeville Regional; Vanderbilt Clarksville; Maury Regional.
  - Positions 10-13 depend on measure and boundary. The cut ranges from 11 to 13 hospitals.
- **Four owners dominate the 13.**
  - Vanderbilt Health 1,978 beds; Ascension Saint Thomas 1,662; HCA TriStar 1,541; three public hospitals 901; one Lifepoint/Ascension joint-venture hospital 167.
- **Interest concentration:** all bed numbers come from one regulator file (independent of the hospitals' marketing, though hospital-reported at licensure). No vendor-self-reported number is load-bearing. Details in Verification.

## Method
- Design:
  - Primary source is the HFC licensure file, filtered to the 41 counties.
  - Cross-checks: CMS Hospital General Information; TDH Joint Annual Report (JAR) FY2024 master file; hospital and news pages.
  - Tools: the browser pane was unavailable. All reads were raw bytes or text via curl with a browser user-agent, because tn.gov returns 403 to WebFetch. No WebFetch answer is cited as verbatim.
- Hypotheses written before collection:
  - H1: a small set (about 10-14 hospitals) holds 75%, and the set is stable across reasonable measures.
  - H0 (rival): membership is unstable, so "the 75% set" is an artifact of definition.
  - Result: H1 holds for the top nine; H0 holds for positions 10-13.
- Limitations:
  - No staffed-bed series exists in the licensed file.
  - Hospital marketing "beds" were not used.
  - The full interactive JAR hospital-by-hospital reports were not read, only the master file.
  - The Oct 2026 HFC report was not yet posted; the page's newest entry is July 2026.
- Stage 10.5 (cold assessment) was SKIPPED per instruction.
- Phase effects (2026-10-17):
  - 8.5 verify: caught my own error (I first listed Cumberland, not Sequatchie, in the 41 counties). This flipped Cumberland Medical Center out of the base set and showed it changes the cut (G).
  - 8.5 verify: found and downgraded stale ownership labels in CMS.
  - 8.5 verify: found a data oddity in the state file (Cookeville).
  - 8.5 verify: a search summary's "134 new beds" for Williamson was NOT on the cited page, so it was dropped.
  - 10.5 assess: not run.

## Table 1 and 2: operating acute-care hospitals, sorted by licensed beds, cumulative share
Columns: rank | HFC license # | hospital (campuses in the license) | city / county | system / owner | type | licensed beds (HFC-J26) | ex-psych/rehab beds | cumulative beds | cumulative %.

Type key: NP nonprofit, FP for-profit, GOV government. Ownership type comes from JAR FY2024 self-reported "Organization Type", updated by dated news where ownership changed.

| # | Lic | Hospital | City / County | System / owner | Type | Beds | Ex-psy/rehab | Cum | Cum% |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 27 | Vanderbilt University Medical Center (adult + Children's + Psychiatric) | Nashville / Davidson | Vanderbilt Health (VUMC) | NP | 1463 | 1357 | 1463 | 18.0 |
| 2 | 24 | Saint Thomas West (+ Midtown campus) | Nashville / Davidson | Ascension Saint Thomas | NP | 1184 | 1184 | 2647 | 32.5 |
| 3 | 136 | TriStar Centennial | Nashville / Davidson | HCA Healthcare (TriStar) | FP | 741 | 609 | 3388 | 41.6 |
| 4 | 100 | Ascension Saint Thomas Rutherford (+ Westlawn; absorbed Stones River, Woodbury) | Murfreesboro / Rutherford | Ascension Saint Thomas | NP | 478 | 478 | 3866 | 47.4 |
| 5 | 23 | TriStar Skyline (+ Madison) | Nashville / Davidson | HCA (TriStar) | FP | 407 | 360 | 4273 | 52.4 |
| 6 | 128 | Williamson Medical Center | Franklin / Williamson | Williamson Health, county-owned (board voted 2026-07-06 to sell to Ascension Saint Thomas; not closed) | GOV | 337 | 337 | 4610 | 56.6 |
| 7 | 95 | Cookeville Regional Medical Center | Cookeville / Putnam | Cookeville Regional Health System (Medical Center Authority; city-bought 1927) | GOV | 309 | 289 | 4919 | 60.4 |
| 8 | 90 | Vanderbilt Clarksville Hospital | Clarksville / Montgomery | Vanderbilt Health since 2026-02-02 (was CHS/Tennova, for-profit in JAR FY2024) | NP | 270 | 250 | 5189 | 63.7 |
| 9 | 74 | Maury Regional Hospital | Columbia / Maury | Maury Regional Health (county-owned; calls itself not-for-profit) | GOV | 255 | 255 | 5444 | 66.8 |
| 10 | 137 | Vanderbilt Wilson County Hospital (2 campuses) | Lebanon / Wilson | Vanderbilt Health | NP | 245 | 170 | 5689 | 69.8 |
| 11 | 33 | TriStar Summit | Hermitage / Davidson | HCA (TriStar) | FP | 234 | 214 | 5923 | 72.7 |
| 12 | 116 | Highpoint Health-Sumner with Ascension Saint Thomas | Gallatin / Sumner | Highpoint Health JV (Lifepoint majority, Ascension Saint Thomas partner) | FP (JAR) | 167 | 138 | 6090 | 74.7 |
| **13** | 135 | **TriStar Hendersonville** (+ Portland Medical Park) | Hendersonville / Sumner | HCA (TriStar) | FP | 159 | 159 | **6249** | **76.7 (CUT)** |
| 14 | 29 | TriStar Horizon | Dickson / Dickson | HCA | FP | 158 | 145 | 6407 | 78.6 |
| 15 | 139 | Highpoint Health-Winchester (+ Sewanee) | Winchester / Franklin | Highpoint JV (joined Mar 2025) | FP (JAR: Lifepoint) | 152 | 128 | 6559 | 80.5 |
| 16 | 22 | Metropolitan Nashville General | Nashville / Davidson | Metro Nashville government | GOV | 150 | 150 | 6709 | 82.3 |
| 17 | 21 | TriStar Southern Hills | Nashville / Davidson | HCA | FP | 136 | 119 | 6845 | 84.0 |
| 18 | 18 | Vanderbilt Tullahoma-Harton | Tullahoma / Coffee | Vanderbilt Health | NP | 135 | 135 | 6980 | 85.7 |
| 19 | 120 | Ascension Saint Thomas River Park | McMinnville / Warren | Ascension Saint Thomas | NP | 125 | 110 | 7105 | 87.2 |
| 20 | 162 | TriStar StoneCrest | Smyrna / Rutherford | HCA | FP | 115 | 115 | 7220 | 88.6 |
| 21 | 92 | Livingston Regional | Livingston / Overton | Lifepoint Health since 2026-06-01 (was ScionHealth) | FP | 114 | 84 | 7334 | 90.0 |
| 22 | 99 | TriStar NorthCrest | Springfield / Robertson | HCA | FP | 109 | 109 | 7443 | 91.3 |
| 23 | 87 | Southern Tennessee Regional Health System (STRHS) Lawrenceburg | Lawrenceburg / Lawrence | Lifepoint Health | FP | 99 | 89 | 7542 | 92.6 |
| 24 | 52 | STRHS Pulaski | Pulaski / Giles | Lifepoint Health | FP | 95 | 68 | 7637 | 93.7 |
| 25 | 138 | Ascension Saint Thomas DeKalb | Smithville / DeKalb | Ascension Saint Thomas | NP | 71 | 71 | 7708 | 94.6 |
| 26 | 2 | Vanderbilt Bedford | Shelbyville / Bedford | Vanderbilt Health | NP | 60 | 60 | 7768 | 95.3 |
| 27 | 127 | Ascension Saint Thomas Highlands | Sparta / White | Ascension Saint Thomas | NP | 60 | 46 | 7828 | 96.1 |
| 28 | 17 | Unity Medical Center | Manchester / Coffee | Independent (nonprofit since 2019; Ascension alliance 2025) | NP | 49 | 49 | 7877 | 96.7 |
| 29 | 85 | Lincoln Medical Center | Fayetteville / Lincoln | Leased from Lincoln County; Huntsville Health System member (JAR) | GOV | 49 | 49 | 7926 | 97.3 |
| 30 | 36 | Ascension Saint Thomas Three Rivers (CAH) | Waverly / Humphreys | Ascension Saint Thomas | NP | 25 | 25 | 7951 | 97.6 |
| 31 | 55 | Houston County Community Hospital (CAH) | Erin / Houston | Braden Health (private; AG approved sale 2022-07) | FP | 25 | 25 | 7976 | 97.9 |
| 32 | 56 | Saint Thomas Hickman (CAH) | Centerville / Hickman | Ascension Saint Thomas | NP | 25 | 25 | 8001 | 98.2 |
| 33 | 75 | Marshall Medical Center (CAH) | Lewisburg / Marshall | Maury Regional Health (county) | GOV | 25 | 25 | 8026 | 98.5 |
| 34 | 80 | Macon Community Hospital (CAH) | Lafayette / Macon | Independent nonprofit (Macon County General Hospital, Inc.), managed by Ovation Healthcare | NP | 25 | 25 | 8051 | 98.8 |
| 35 | 118 | Highpoint Health-Trousdale (CAH) | Hartsville / Trousdale | Highpoint JV | FP | 25 | 25 | 8076 | 99.1 |
| 36 | 129 | Highpoint Health-Riverview (CAH) | Carthage / Smith | Highpoint JV | FP | 25 | 15 | 8101 | 99.4 |
| 37 | 200 | Perry County Community Hospital | Linden / Perry | BradenHealth | FP | 25 | 25 | 8126 | 99.7 |
| 38 | 152 | Saint Thomas Hospital for Specialty Surgery (surgical specialty; flagged) | Nashville / Davidson | Ascension Saint Thomas (JAR: managed by USPI/Tenet; org type blank) | NP (unverified) | 23 | 23 | 8149 | 100.0 |

- All beds: HFC Hospital Full Bed Report, July 2026 (file Last-Modified 2026-08-10).
- Ownership: TDH JAR FY2024 master file (self-reported), pulled 2026-10-17, plus the dated sources listed under Sources.
- Totals: 38 licenses, 8,149 beds; 75% = 6,111.75.
- Seven CAHs are confirmed by the HFC CAH Listing, July 2026 (rows 30-36 except Perry). Perry's CAH status is unverified.

### Listed but not in the denominator
- Cumberland River Hospital (Celina, Clay): HFC "Licensed" 33 beds, but closed in practice. Adding it changes nothing (sensitivity B).
- Jamestown TN Medical Center (Fentress): Licensed-Inactive, 85.
- TriStar Ashland City (Cheatham, HCA) and Wayne Medical Center (Wayne, Maury Regional): Rural Emergency Hospitals, 0 beds. Wayne converted 2024-12-01 per Maury.
- The 5 non-acute licenses and 8 closed satellites above.

## The cut and sensitivities
Cut = first hospital at which cumulative share >= 75%.

| Case | Licenses | Total beds | Cut at | Last in | Share before / after |
|---|---|---|---|---|---|
| A. Base | 38 | 8,149 | 13 | TriStar Hendersonville | 74.7 / 76.7 |
| B. + Cumberland River | 39 | 8,182 | 13 | same | 74.4 / 76.4 |
| C. - Cumberland River - Specialty Surgery | 37 | 8,126 | 13 | same | 74.9 / 76.9 |
| D. Ex-psych/rehab/alcohol-drug beds | 38 | 7,540 | 12 | TriStar Hendersonville | 73.0 / 75.1 (Highpoint Sumner falls out; order changes) |
| E. JAR FY2024 staffed adult+peds | 37 (no Perry) | 6,310 | 11 | Highpoint Winchester | 74.8 / 77.1 (Wilson County falls out) |
| F. JAR FY2024 licensed adult+peds | 37 | 7,763 | 13 | TriStar Hendersonville | 73.6 / 75.7 |
| G. Base + Cumberland Medical Center (189; East TN by statute) | 39 | 8,338 | 13 | Highpoint Sumner (Hendersonville falls out) | 73.3 / 75.3 |

### System rollup, 13 hospitals in the base cut (6,249 beds)
- Vanderbilt Health: VUMC 1463 + Clarksville 270 + Wilson 245 = 1,978.
- Ascension Saint Thomas: West/Midtown 1184 + Rutherford 478 = 1,662.
- HCA TriStar: Centennial 741, Skyline 407, Summit 234, Hendersonville 159 = 1,541.
- Public: Williamson 337, Cookeville 309, Maury 255 = 901.
- Highpoint JV: Sumner 167.

### System share of all 8,149 beds
- Vanderbilt Health 2,173 (26.7%): the five above plus Tullahoma 135 and Bedford 60.
- HCA 2,059 (25.3%).
- Ascension Saint Thomas 1,991 (24.4%).
- Public (Williamson, Cookeville, Maury, Marshall, Nashville General, Lincoln) 1,125 (13.8%).
- Lifepoint plus the Highpoint JV 677 (8.3%): Highpoint Sumner/Winchester/Trousdale/Riverview 369, STRHS Lawrenceburg/Pulaski 194, Livingston 114.
- Independent or other: Unity 49, Macon 25, Braden-owned Houston and Perry 50.
- Williamson's pending sale would move 337 beds to Ascension (expected close 2027-2028 per press).

## Completeness check
- **State list for the 41 counties:** the HFC file has 183 hospital rows statewide; **61 in the 41 counties**.
  - 44 Licensed: 39 general acute + 5 non-acute (3 rehab, 1 long-term acute care, 1 psychiatric).
  - 2 Rural Emergency Hospital.
  - 1 Licensed-Inactive.
  - 6 satellites of a licensed hospital.
  - 8 Closed-Satellite.
- **I found 39 state-licensed general acute hospitals; 38 are operating** (Cumberland River excluded as closed). Both numbers are the state's list; no hospital is in my table that the state does not list.
- **CMS Hospital General Information (modified 2026-07-22, retrieved 2026-10-17):** 38 acute/CAH provider numbers in the 41 counties, after setting aside Trustpoint, 2 REH, 6 psychiatric and 2 VA.
  - Reconciliation: 38 CMS = 37 HFC licenses + Stones River (own CMS number, but folded into license #100 in the state's July 2026 file).
  - HFC-only: Perry County (new) and Cumberland River (closed).
- **JAR FY2024 master file:** has a record for every base license except Perry (new). The Cumberland River row is blank.
- **Counties with no hospital in any of the three sources:** Grundy, Jackson, Lewis, Moore, Pickett, Sequatchie, Stewart, Van Buren. This negative was checked in HFC, CMS and JAR.
- Unresolved items are listed under Thin/missing.

## Verification (stage 8.5)
Load-bearing claims. Page-text reads are marked verbatim; summarized tool answers are marked paraphrase.

| Claim | Source | Verdict |
|---|---|---|
| The 41-county list, Cumberland excluded, Sequatchie included | tn.gov directory "County & City Web Sites", citing TCA 4-1-201 (2020); Wikipedia wikitext | VERIFIED-VERBATIM (raw HTML text), second source agrees |
| Per-license bed values (all 38) | HFC xlsx, parsed from cell values; re-downloaded, hash identical; table ref A1:P184 = 183 rows | VERIFIED-VERBATIM (file read) |
| Licensed beds match an independent self-report | JAR FY2024 licensed adult+peds: Centennial 741, Skyline 286+121=407, Summit 234, Maury 255, Clarksville 270, Williamson 337, Sumner 167, Hendersonville 134+25=159, Midtown 643 + West 541 = 1,184 | VERIFIED-VERBATIM (cell values) |
| Wilson County 245 | JAR 170 + psych 49 + rehab 26; also VUMC 2021 filing "VWCH is a two-campus facility licensed for 245 beds" | VERIFIED-VERBATIM |
| VUMC series | VUMC 2021 disclosure: 726 + 343 + 106 = 1,175 = HFC 2021 value; 1,463 (July 2026) is state-only, new tower opened Oct 2025 | 2021 VERIFIED-VERBATIM; 2026 single-source |
| Cookeville 309 | Crossville Chronicle 2026-03-31: "raising the hospital's licensed bed count to 309". The HFC row has an odd field (Swing = 269); the Sept 2021 file had 269 total | VERIFIED-VERBATIM (news); state field anomaly flagged |
| Rutherford 478 | Apr 2026 file 418 + Stones River 60 (now "Closed - Satellite") = 478. JAR 392 + 8 + 60 = 460; the 18 gap fits Ascension's 18 new critical care beds. Ascension page now names the site "Ascension Saint Thomas Rutherford Stones River" | CLOSE-PARAPHRASE (arithmetic plus page title); inference |
| Clarksville is Vanderbilt-owned | VUMC news 2026-02-02: "the 270-bed hospital will be named Vanderbilt Clarksville Hospital" | VERIFIED-VERBATIM |
| Houston County sold to Braden Health | WPLN 2022-07-26 (AG approval); JAR FY2024 org type and system "Braden Health Incorporated" | VERIFIED (title/tags) plus JAR |
| Highpoint = Lifepoint majority + Ascension partner; Winchester/Sewanee added March 2025 | Trade/press search summaries; JAR FY2024 lists LifePoint, investor-owned | CLOSE-PARAPHRASE for JV terms; VERIFIED for JAR field |
| Livingston under Lifepoint since 2026-06-01 | Search summary of Lifepoint release | CLOSE-PARAPHRASE; JAR FY2024 shows ScionHealth |
| Williamson sale vote | Press via search summaries (board 12-0 on 2026-07-06; commission non-binding LOI) | CLOSE-PARAPHRASE |
| Williamson "134 new beds" | Cited page (Williamson Scene, 2024-06-20) does not contain it | **NOT-FOUND, dropped** |
| VUMC "1,741 licensed beds across 7 hospitals" | VUMC facts page via search summary (2023); the Jan 2026 report URL returned 404 | CLOSE-PARAPHRASE; not reconciled with HFC (see Thin/missing) |

- Same-source dependency: the HFC file and the JAR FY2024 file are both Tennessee Department of Health / HFC products, but one is regulator licensure data and the other is hospital self-reporting, so the match is a real consistency check. Both are state data; neither is a fully independent census.
- Interest concentration: 0 of the load-bearing numbers are vendor self-reported. The JAR is self-reported by the hospitals, which has some interest (see Numbers register).
- Zero-result cross-checks:
  - "No hospital in 8 counties" (Grundy, Jackson, Lewis, Moore, Pickett, Sequatchie, Stewart, Van Buren): negative in HFC, CMS and JAR.
  - "No newer HFC hospital report than July 2026": checked by listing the HFC licensure-reports page twice; no Oct 2026 entry.
  - "No second source for Jamestown reopening": two searches (news and HFC status), nothing found after the inactive status.

## Numbers register
Source-interest classes: INDEPENDENT, VENDOR-SELF-REPORTED, ADVERSARIAL, UNVERIFIABLE. Hospital filings are SELF-REPORTED but regulated.

| Number | Claims | Source | Date | Class | Verdict |
|---|---|---|---|---|---|
| 41 | counties in Middle Grand Division | tn.gov directory (TCA 4-1-201) | 2020 statute, page read 2026-10-17 | INDEPENDENT | VERIFIED-VERBATIM |
| 183 / 61 | HFC hospital rows statewide / in the 41 counties | HFC July 2026 | file 2026-08-10 | INDEPENDENT | VERIFIED-VERBATIM |
| 38 / 8,149 | operating acute licenses / licensed beds | computed from HFC | 2026-10-17 | INDEPENDENT | VERIFIED (computation re-run on re-download) |
| 6,111.75 / 6,249 | 75% threshold / cumulative at the cut | computed | - | INDEPENDENT | VERIFIED |
| 74.7% / 76.7% | cumulative share before / at the cut | computed | - | INDEPENDENT | VERIFIED |
| 1,463; 1,184; 741; 478; 407; 337; 309; 270; 255; 245; 234; 167; 159 | licensed beds, top 13 | HFC July 2026 | 2026-08-10 | INDEPENDENT | file read; JAR matches for 9 of 13 exactly, other 4 reconciled in table above |
| 1,175 (VUMC, 2021) | VUH 726 + MCJCHV 343 + VPH 106 | VUMC 2021 CDA filing | June 2021 | VENDOR-SELF-REPORTED | VERIFIED-VERBATIM; used only to validate the HFC 2021 row |
| 1,741 | VUMC licensed beds, 7 hospitals | VUMC facts page (via search) | FY2023 data | VENDOR-SELF-REPORTED | CLOSE-PARAPHRASE; unreconciled |
| 6,310 | JAR FY2024 staffed adult+peds beds (37 licenses) | TDH JAR master file | filed 2025 | SELF-REPORTED | VERIFIED-VERBATIM (cells); scope varies |
| 309 | Cookeville licensed beds | Crossville Chronicle | 2026-03-31 | INDEPENDENT (local press) | VERIFIED-VERBATIM |
| 270 | Vanderbilt Clarksville beds | VUMC news | 2026-02-02 | VENDOR-SELF-REPORTED | VERIFIED-VERBATIM; HFC and JAR agree |

## Thin / missing
- **Cumberland River Hospital (Celina):** the HFC file still shows it "Licensed", 33 beds. News says it closed March 1, 2019, was bought and reopened, then closed again (the second-closure year is not stated in the articles I could read; the Becker's article returned 403). JAR FY2024 is blank; CMS has no entry. Treated as non-operating; it changes no cut result.
- **Stones River:** treated as folded into license #100 by arithmetic (418 + 60 = 478) and the Ascension page rename. No state document says so in words.
- **Perry County Community Hospital:** HFC lists 25 beds, licensed. One news summary says it opened around 2025-09-29 under BradenHealth. CAH status unconfirmed (not on the CAH list). No JAR or CMS record yet.
- **VUMC reconciliation:** the HFC licenses VUMC owns sum to 1,983 (1,463 + 245 + 60 + 135 + 80 Stallworth). VUMC's own 2023 figure is 1,741 across 7 hospitals. Unreconciled; the HFC value includes the Jim Ayers Tower (first patients 2025-10-01; planned total 180 beds; construction to early 2027), so some licensed beds may not be staffed yet.
- **Staffed vs licensed gap is large for small hospitals:** e.g. Nashville General 150 licensed / 60 staffed, DeKalb 71 / 12, Hickman 25 / 8 (JAR FY2024). If "beds" is a proxy for patient volume, licensed beds overstate small rural hospitals.
- **Cookeville:** the state row stores 269 in the "Swing Beds" column and 20 in rehab; the 309 total is corroborated by the 2026 news item, but the 20-bed gap between 289 (269 + 20) and 309 is unexplained.
- **Highpoint:** the Ascension partner's ownership share was not found; classified for-profit because JAR and press say Lifepoint holds the majority.
- **Lincoln Medical Center:** JAR says hospital district or authority, leased from Lincoln County, Huntsville Health System member. No Lincoln-side page was read.
- **Macon:** nonprofit entity name from tax-exempt records; hospital's own page not read.
- **Saint Thomas Hospital for Specialty Surgery (23):** surgical specialty hospital included as acute (it is a state-licensed hospital with acute CMS type). Excluding it does not move the cut (C).
- Not checked: Blanchfield Army Community Hospital at Fort Campbell (federal, located on the Kentucky side); freestanding emergency departments; HFC Off-Campus ED report.
- Not done: the interactive JAR hospital-by-hospital reports; a CMS Provider of Services beds file (the hospital POS file was not found on data.cms.gov; only iQIES HHA/ASC datasets were listed).
- Searches that produced negatives:
  - "TDH hospital licensure data 2024" returned only old summaries; the HFC page was found instead.
  - POS hospital beds file: not found.
  - Jamestown reopening: nothing found.

## What would change this conclusion
- A different county definition (G): moves the 13th slot from Hendersonville to Highpoint Sumner and adds a hospital.
- Staffed beds instead of licensed (E): the set shrinks to 11 and Wilson County drops out.
- Williamson sale closing: moves 337 beds from public to Ascension (not before 2027).
- The Oct 2026 HFC report or later license changes (e.g. Jim Ayers Tower beds) could shift ranks 10-13.
- Untested falsifier of H1: a measure based on discharges or patient days instead of beds. That needs the JAR utilization schedules (not pulled).

## Sources (all retrieved 2026-10-17)
- HFC Hospital Full Bed Report, July 2026 xlsx: https://www.tn.gov/content/dam/tn/hfc/documents/HFC-Hospital_Full_Bed_Report_July2026.xlsx (Last-Modified 2026-08-10). Also April 2026 xlsx (Apirl%202026) and Sept 2021 pdf for comparison.
- HFC Critical Access Hospital Listing, July 2026 xlsx: https://www.tn.gov/content/dam/tn/hfc/documents/HFC-Hospital_CAH_Report_July2026.xlsx
- HFC licensure reports index: https://www.tn.gov/hfc/publication-and-reports/licensure-reports.html
- TDH Public JARs master file (hospitals, "Current" = JAR 2024): https://internet.health.tn.gov/PublicJArs/ (retrieved by form post, 2026-10-17)
- County list: https://www.tn.gov/directory/county-city-web-sites.html (TCA 4-1-201, 2020); https://en.wikipedia.org/wiki/Middle_Tennessee
- CMS Hospital General Information (dataset xubh-q36u), modified 2026-07-22, via data.cms.gov provider-data API
- VUMC 2021 CDA filing: https://www.vumc.org/finance/sites/default/files/public_files/VUMC%206.30.21%20CDA%20Final.pdf
- VUMC news, 2026-02-02 Clarksville acquisition: https://news.vumc.org/2026/02/02/vanderbilt-health-acquires-tennovas-clarksville-hospital-and-related-physician-clinics-from-community-health-systems
- Crossville Chronicle, 2026-03-31, CRMC 4 West (licensed beds 309)
- WPLN, 2022-07-26, Houston County hospital takeover by Braden Health
- Williamson Scene, 2024-06-20, West Tower opening; MedCity News and other press (July 2026), Williamson Health sale to Ascension
- Ascension location page, Rutherford Stones River (published metadata 8/7/2026)
- Lifepoint / Ascension joint venture releases (2023-12, 2025-03); Lifepoint ScionHealth acquisition (2026-06-02); Cookeville HFC CON staff review (April 2026) and Becker's (city purchase 1927); WPLN and Becker's on Cumberland River, Perry County, Wayne Medical Center
- Scratch artifacts (not deliverables): parsed TSVs and scripts under <session scratchpad> and <user path>

