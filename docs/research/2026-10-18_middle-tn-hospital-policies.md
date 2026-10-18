# Research brief - Middle Tennessee hospitals holding 75% of beds, and their financial assistance policies

**Date:** 2026-10-18 00:00 CDT (compiled from 5 agent reports collected
2026-10-17 ~23:20-23:58 CDT).
**Question:** Which Middle Tennessee hospitals hold the largest 75% of
acute-care beds, and what do their financial assistance policies (FAPs) say?
**For:** Evan and the team. It feeds the roadmap decision on encoding real
policies (features brief candidate 1) and judge Q&A. It does NOT change the
demo: the app stays on the synthetic Cumberland General policy (hard rule).
**Status:** compiled by the orchestrator from agent reports. The orchestrator
has NOT re-fetched the sources. Stage 10.5 (cold assessment) NOT run. Every
policy number is the hospital's own document (VENDOR-SELF-REPORTED by nature;
it is the legal text, but it says what the policy promises, not how it is
applied).

Sources (full text, citations, verification tables):
- docs/research/raw/2026-10-17_mtn-census.md - census and the 75% cut
- docs/research/raw/2026-10-17_mtn-vumc.md - Vanderbilt (VUMC)
- docs/research/raw/2026-10-17_mtn-ascension-saint-thomas.md - Ascension
- docs/research/raw/2026-10-17_mtn-hca-tristar.md - HCA TriStar
- docs/research/raw/2026-10-17_mtn-other-systems.md - everyone else

> 2026-10-18 00:13 CDT: cold assessment run - 3 factual errors and 1 scope error found (L35-37 "same county", L40-41 VUMC 120/240, L100-101 4 -> 5 outside 501(r), L79 HCA 4% emergency only); see docs/research/2026-10-18_cold-assessments.md section 4. Not yet corrected here.

## TL;DR

- **13 hospitals hold 76.7% of 8,149 licensed acute beds** in the 41
  statutory Middle TN counties (state HFC Full Bed Report, July 2026). The
  first 9 are in under every measure tried. Positions 10-13 move with the
  measure (11 to 13 hospitals).
- **The 13 run on only 7 distinct policies.** VUMC (one FAP, 3 hospitals),
  Ascension Saint Thomas (one FAP, 2 licenses), HCA TriStar (one system
  page, 4 hospitals), plus Williamson, Cookeville, Maury and Highpoint
  Sumner, one each. 3 systems cover 9 of the 13, plus 4 single-hospital
  policies.
- **Free-care ceilings range from 100% FPL (Williamson, Cookeville, Maury)
  to 350% FPG (Vanderbilt Clarksville).** Same county, different answer: a
  household at 220% FPL gets 100% free at VUMC, 100% free at Ascension, 25%
  off at Cookeville and nothing free at Maury.
- **Application windows range from 60 days after service (Highpoint
  Sumner) to 240 days after the first statement (Ascension).** VUMC's own
  policy contradicts itself (240 in a definition, 120 in the operative
  text). BillScan reads the window from the policy JSON
  (days_from_statement), so a real policy can carry its own window, but the
  "from service" vs "from statement" anchor differs too.
- **Residency limits are common:** Ascension 13 named counties; Cookeville
  14 counties and a $500 minimum; Williamson 60 miles for scheduled care;
  Nashville General Davidson County only. VUMC states none.

## Census: the 75% cut (state HFC licensed beds, July 2026)

| # | Hospital (license) | County | Owner | Beds | Cum % | Policy |
|---|---|---|---|---|---|---|
| 1 | Vanderbilt University Medical Center (adult + Children's + Psych) | Davidson | VUMC | 1463 | 18.0 | VUMC |
| 2 | Saint Thomas West + Midtown (one license) | Davidson | Ascension Saint Thomas | 1184 | 32.5 | Ascension |
| 3 | TriStar Centennial | Davidson | HCA | 741 | 41.6 | HCA TriStar |
| 4 | Ascension Saint Thomas Rutherford (+ Westlawn, Stones River) | Rutherford | Ascension Saint Thomas | 478 | 47.4 | Ascension |
| 5 | TriStar Skyline (+ Madison) | Davidson | HCA | 407 | 52.4 | HCA TriStar |
| 6 | Williamson Medical Center | Williamson | County (sale to Ascension voted 2026-07-06, not closed) | 337 | 56.6 | Williamson |
| 7 | Cookeville Regional | Putnam | City medical center authority | 309 | 60.4 | Cookeville |
| 8 | Vanderbilt Clarksville (ex-Tennova, VUMC since 2026-02-02) | Montgomery | VUMC | 270 | 63.7 | VUMC App. C |
| 9 | Maury Regional | Maury | County | 255 | 66.8 | Maury |
| 10 | Vanderbilt Wilson County (2 campuses) | Wilson | VUMC | 245 | 69.8 | VUMC |
| 11 | TriStar Summit | Davidson | HCA | 234 | 72.7 | HCA TriStar |
| 12 | Highpoint Health-Sumner | Sumner | Lifepoint-majority JV with Ascension | 167 | 74.7 | Highpoint Sumner |
| 13 | TriStar Hendersonville | Sumner | HCA | 159 | 76.7 (CUT) | HCA TriStar |

Sensitivities (census report): excluding psych/rehab beds gives 12 hospitals
(Highpoint Sumner out); JAR staffed beds give 11 (Wilson County out);
adding Cumberland County (East TN by statute) swaps Hendersonville for
Highpoint Sumner. Next outside the cut: TriStar Horizon 158, Highpoint
Winchester 152, Nashville General 150.

## Policy comparison (the 7 policies covering the 13)

| Policy | Free care | Discount tiers | Residency / assets | Window | Other |
|---|---|---|---|---|---|
| VUMC (approved Sep 2026; tables eff. 7/1/2026) | <= 300% FPG | 85% for 300-350%; catastrophic above if VUMC bills > 100% of income | none stated / none in FAP | 240 days (definition) vs 120 (operative) | TennCare = automatic 100%; SNAP/WIC/homeless presumptive; AGB 24% (Wilson 17%); "does not engage in any" ECAs |
| VUMC Clarksville (Appendix C) | <= 350% FPG | none | same | same | AGB 12% |
| Ascension Saint Thomas (2025-07-01) | <= 250% FPL | 86/81/79% to 400%; means test above | 13 counties; asset test at 250% ("may") | 240 days from first discharge bill | uninsured must apply to Medicaid; presumptive scoring; AGB capped at 20% |
| HCA TriStar (system page, undated) | 0-200% FPL | 201-400% if balance > $1,500; HCA page caps at 4% of income | not stated | not published | uninsured discount ~92%; for-profit, 501(r) does not apply; HCA says no credit reporting or lawsuits |
| Williamson (updated 2026-02-18) | <= 100% FPL | 90/80/70/60% at 150/175/200/250% | 60 miles for scheduled care; assets considered | 20 days to complete an incomplete app | catastrophic: pay 15-30% of income; 47% automatic uninsured discount |
| Cookeville (web page, undated) | <= 100% FPL | 75/50/25% at 150/200/300% | 14 counties; $500 minimum balance | not stated | liability capped at 10% of income at <= 200% FPL; must apply to Medicaid |
| Maury (2024; printed expiry 9/13/2025, still the linked file) | <= 100% FPL | discounted to 250% FPL | citizens and legal immigrants; limited assets | not read | catastrophic route; AGB <= most favored commercial rate |
| Highpoint Sumner (eff. 04/2025) | <= 200% FPG (uninsured only) | 100% to 60% sliding, 200-300% | undocumented may apply | 60 days from service | about 30 business days to decide |

## Findings that matter for BillScan

1. **One engine, many rule shapes.** Tiers are expressed as FPL or FPG
   multiples, income bands, asset tests, residency lists, balance minimums,
   catastrophic rules and income caps. The current policy JSON schema
   (synthetic) holds tiers and a window; residency, minimum balance,
   catastrophic and "insured patients excluded" (Highpoint) do not exist
   yet. Encoding real policies is schema work, not just data entry.
2. **Window anchor differs.** "From first statement" (Ascension, VUMC
   definition) vs "from service" (Highpoint, 60 days). A wrong anchor gives
   a wrong "Apply by" date - the one number a family acts on.
3. **Stale and self-contradicting documents exist.** Maury links an
   expired policy; VUMC's 120 vs 240; Ascension's summary predates its FAP
   and lists a different mailing address. Any real-policy feature needs a
   `review_by` date and a human check per policy.
4. **For-profit HCA is outside 501(r).** Collections-protection text
   (features brief candidate 4) must be off for 4 of the 13 hospitals.

## Conflicts between agent reports (unresolved)

- Stones River: Ascension agent lists it as a separate hospital (43
  staffed beds); census treats it as folded into Rutherford's license #100
  by arithmetic (418 + 60 = 478). No state document says so in words.
- Midtown + West: Ascension agent gives staffed beds 396 + 643 (Wikipedia)
  vs the state's 1,184 licensed. Use the state number for ranking.
- VUMC beds: VUMC's own disclosure 1,723 (2025-03-31) vs HFC licenses
  summing to 1,983 incl. Stallworth and the new tower. Unreconciled.
- Cookeville: state row has an odd field (269 in Swing Beds); 309 total
  corroborated by local news only.

## Thin / missing

- No re-fetch by the orchestrator; no cold assessment (stage 10.5 skipped).
- Practice vs policy: approval rates, denial reasons, screening-vendor data
  use - none published.
- HCA: no policy document, effective date, application form or window.
- Maury: no current (unexpired) policy found; pages 6-11 not read.
- Tennessee statute text (TCA 68-11-262, the 175% of cost cap): only
  secondary sources; Justia blocked.

## What would change this

A newer HFC bed report (Oct 2026 not yet posted); the Williamson sale
closing (moves it under Ascension's FAP); a newer Maury policy; an HCA
policy PDF with hospital-level differences.
