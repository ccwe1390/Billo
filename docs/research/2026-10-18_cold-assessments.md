# Cold assessments (research-brief stage 10.5) of the four 2026-10-17/18 briefs

> Run 2026-10-18 00:08-00:12 CDT by four fresh agents (one per brief), each given
> only its brief (and, for the policies and sustainability briefs, their raw
> reports in docs/research/raw/). Read-only; each re-fetched a few load-bearing
> sources itself. Findings below are the assessors' reports, condensed by the
> orchestrator; line numbers are the briefs' as of 5a7fd84. No brief has been
> edited in response yet (the skill allows exactly one more collection round).

## 1. presentation-stats brief (docs/research/2026-10-17_presentation-stats-brief.md)

**Headline:** the $2.7B figure (KFF Health News) is called "independent
support" (L16, L72) but is the starting input of Dollar For's $7B estimate:
$7B = $2.7B + $2.2B (imputed to the other 1,336 nonprofit hospitals) + $2B
(Bridging the Chasm PDF, read with pdftotext from the untracked
docs/Dollar_For.Bridging_the_Chasm.pdf; the brief's L41 says the PDF was
unreadable).

- Shared sources: $2.7B inside $7B/$14B; America's Health Rankings 9.7% is
  built on ACS, so it does not corroborate ACS 9.69% (L100, L172).
- Interests: about 10 register rows are advocacy or trade groups (Dollar For
  x4, NCLC x2, CBPP, AARP, AHA, Himmelstein); only Dollar For is disclosed up
  front; CBPP, AARP and AHA are labelled INDEPENDENT (L196, L210, L216).
- Never given a chance to die: H2's "80% of bills have errors" rests on the
  prior brief (L109, L140); 66.5% bankruptcy is snippet-only (L219).
- Not run: primary report PDFs (Dollar For method declared UNREACHABLE at L41
  though pdftotext was available); CFPB research reports; Pew (L42).
- Missing: share of Nashville beds that are for-profit (HCA TriStar, outside
  501(r)); 2,984 counts nonprofits only. Presumptive-screening vendors as the
  real competition. Charity care vs bad debt (Schedule H Part III).
- Over-confident: L124 "VERIFIED-VERBATIM unless noted" covers L130, whose
  numbers are COMPUTED (L167); "Arabic next-largest" stated as fact though
  L241 says margins may erase the ranking; L108 (43%/53%) not re-read.

**Re-fetch:** 20M / $220B (KFF-Peterson) FOUND-VERBATIM; 29% / 52% (Dollar
For) FOUND-VERBATIM; 2,984 (AHA, "Nongovernment Not-for-Profit Community
Hospitals") FOUND-VERBATIM; 34% LEP forms (KFF) FOUND-VERBATIM but the page
says "in the past three years", which the slide line drops; 91,000 (CBPP)
FETCH-FAILED (Cloudflare 403), not checked by the assessor.

**Slide safety (assessor's verdict):**
- SAFE: "20 million US adults owe over $250 in medical debt - at least $220
  billion" (KFF/Peterson 2024, 2021 data); "34% of adults with limited
  English say it made health care forms hard to fill out in the past three
  years" (KFF 2024); "2,984 nonprofit community hospitals" (AHA 2026) - do not
  imply it covers HCA/TriStar.
- SAY WITH ATTRIBUTION: "Dollar For's late-2023 patient survey found only 29%
  ... get financial assistance, and 52% got no information from their
  hospital"; "CBPP estimates about 91,000 Tennesseans are in the coverage gap
  (2024 data)"; "9.7% of Tennesseans uninsured (Census ACS 2024)"; "about
  75,000 Davidson County residents speak limited English (Census ACS 2024,
  our calculation)".
- DO NOT SAY: $14B or $7B as fact; $2.7B as independent corroboration; 66.5%
  medical bankruptcies; "80% of bills have errors"; "100 million with medical
  debt"; "Tennessee banned medical debt on credit reports"; 95,000; 9.3%;
  24%; "Arabic is Davidson's #2 language"; 31% of caregivers managing
  finances; 175%; VUMC 24%; 282,294.

## 2. customer-features brief (docs/research/2026-10-17_customer-features-brief.md)

- Shared sources: Messac 2024 (41-600% FPL, 20% hardship median,
  "Medicaid-first almost universal") uses Dollar For's 2024 policy database
  yet is labelled INDEPENDENT (L355-358) and offered as a counterweight
  (L348); Dollar For's press release (29/52) and "Path to Charity Care"
  (67/45/28/24) are one survey; the secret-shopper study (L111) and the AJMC
  readability study (L146) are the same research group (undisclosed).
- Interests: 8 of 26 register rows lean on Dollar For (the brief says 6 of
  24); Dollar For is both a key source and the top referral target (L215,
  L306) - undisclosed.
- Never given a chance to die: H0 (falsifier "users fail at understanding",
  L68); evidence pointing that way was collected but not weighed (52% got no
  information, 10th-grade readability, bill age 28% > paperwork 24% as a
  denial reason). H2 has no falsifier.
- Not run: NCLC (named L35, never used); Census ACS C16001; HCA source is a
  Florida web page, not TriStar's policy.
- Missing (counsellor's view): physician/group bills outside the hospital
  FAP (501(r) covered-provider list); insured/underinsured patients; bill-age
  deadline feature; Medicare Savings Programs; a deceased parent's bills.
- Over-confident: TennCare "0% FPL" stated flatly (CLOSE-PARAPHRASE, L327;
  presumptive/retro UNREACHABLE, L343); "help changes outcomes" (L147) is
  causal on correlational data; SB 402 "not enacted" (CLOSE-PARAPHRASE, L344).
- On Evan's 23:59 calls: the brief's case against the nickname is OPINION;
  against the F11.8 Q&A box it is WEAK (one internal data point; risk is
  reasoning, and L397 says Q&A rises if understanding is the failure point).
- Re-fetch: Dollar For 67/45/28/24 FOUND-VERBATIM; Messac 20% median
  FOUND-VERBATIM but only "among those hospitals that defined such a limit",
  so the TL;DR's "most nonprofit hospitals have a hardship rule" (L26) is
  broader than the source; "almost universal" FOUND-VERBATIM as an aside, not
  a measured share. Also: L53 "no verdict flipped" vs L11 "corrected two
  verdicts".

## 3. sustainability brief (docs/research/2026-10-17_sustainability-brief.md)

**Headline:** the 0.7% figure is "at most 0.7% on average" across all
hospitals in Dollar For's BottomLine.pdf; the brief (L135-138) drops "on
average" and applies it to a single Tennessee hospital as a verdict. The
handoff's "up to 0.7% of revenue" has the same problem.

- Shared sources: H1 "mostly died" (L146-147) and Oregon over-awarding
  (L155-157) are one Oregon episode in three documents (raw money2 L243);
  0.7% loss and unmeasured collection savings are the same Dollar For PDF.
- Interests: ~60% of load-bearing numbers are self-reported (990s, vendor
  pages; L162-163); the "advocacy source" label in the raw report is dropped
  at L135; the TL;DR (L33-35) is stale and mentions neither.
- Never given a chance to die: H2 grants (ranked #1, L175) - its kill test
  (L45, funders do not back software-only tools without outcome data) was
  never sought; comparables (L284-304) are human-advocate or debt-buying orgs;
  contrary evidence unanswered (no RWJF/Arnold/Commonwealth grant to a similar
  tool, L333-334; Dollar For's two largest donors left, L293-294).
- Not run: discovery interviews (L66-68, L245); OCI Usage API (L67-68,
  L193-194). VUMC Schedule H is MISSING in one raw report and VERIFIED in the
  other; the brief cites it (L158-159) without settling it.
- Missing: VUMC's FAP-eligible bad debt $4.05M vs $233M financial assistance
  (raw money2 L134-137) - the addressable leak, which cuts against H1; cost of
  doing nothing (501(r), 120-day collection exposure); owner and staff cost
  (L111-114 MISSING); an outcome baseline for "applications per 100 scans".
- Re-fetch: Large Cohere $0.0156 per 10,000 transactions FOUND-VERBATIM
  (Oracle price-list JSON, lastUpdated 2026-10-08, part B108077); OCI
  Language first 1,000 free then $10.00 per 1,000 FOUND-VERBATIM (B95920);
  E5 $0.03 OCPU-h and $0.002 GB-h FOUND-VERBATIM (B97384, B97385); 0.7%
  FOUND-DIFFERENT (scope: "on average").

## 4. Middle TN hospital policies brief (docs/research/2026-10-18_middle-tn-hospital-policies.md)

**Headline:** the four load-bearing facts hold on re-fetch, but three claims
are wrong or overstated, and licensed beds were never tested as a proxy for
where patients go. Orchestrator re-read L35-41, L63 and L100-101 on disk: the
"Same county" and "4 of the 13" findings below are confirmed.

- Shared sources: the census robustness check (L25-27, L66-68) compares two
  Tennessee HFC/health-department files that hospitals self-report;
  HCA's tiers (L79) are two pages by HCA.
- Interests: every policy number is the hospital's own document (100%
  self-reported); stated in Status (L12-14), not in the TL;DR.
- Never given a chance to be wrong: licensed beds as the proxy (discharges or
  patient days never pulled; Nashville General 150 licensed vs 60 staffed);
  the 75% cut; excluding Trustpoint (217 psychiatric beds) - if counted it
  ranks #12 and Hendersonville drops out.
- Not used: IRS Schedule H; CMS cost-report S-10 charity data; TCA 68-11-262
  statute text (L122).
- Errors a Nashville counsellor would flag:
  - L35-37 "Same county" is false: VUMC (Davidson), Cookeville (Putnam), Maury
    (Maury). The 220% example also ignores Ascension's 13-county residency rule
    and 250% asset test.
  - VUMC tests AGI; the others gross household income - not noted.
  - HCA's 4% cap applies to emergency services only (L79 drops this).
  - L100-101 "4 of the 13" outside 501(r) should be 5: Highpoint Sumner is
    Lifepoint-majority (for-profit), L63.
  - Physician bills and each FAP's covered-provider list are not mentioned;
    Nashville General (safety net) sits outside the bed cut.
- Over-confident: "VUMC's own policy contradicts itself (240 vs 120)" (L40-41,
  L76, L97) - 240 days is the defined Application Period; 120 is only
  "encouraged". Ascension's 240 is not a hard cut-off either (later
  applications get aid on the unpaid balance).

**Re-fetch:** 13 hospitals = 76.7% of 8,149 beds (HFC July 2026 xlsx; 6,249 /
8,149) FOUND-VERBATIM; VUMC free at or below 3.0x FPG, 85% to 3.5x, Clarksville
100% to 3.5x FOUND-VERBATIM; VUMC window FOUND-DIFFERENT (see above); Ascension
<= 250% FPL (2025-07-01) FOUND-VERBATIM; Ascension 240th-day window
FOUND-VERBATIM (with the late-application carve-out).

**Assessor's fixes, in order:** L36 "same county"; VUMC 120/240 wording
(L40-41, L76, L97); 4 -> 5 outside 501(r) (L100-101); HCA 4% cap emergency
only (L79); add AGI vs gross income to Findings item 1.

## Phase effects (stage 10.5, 2026-10-18)

- stats: caught a shared input ($2.7B inside $7B) and a misread "unreadable"
  PDF; downgraded $14B/$7B to DO-NOT-SAY; added a dropped time window (34%).
- features: added a limitation (Messac uses Dollar For data; 8 of 26 rows);
  downgraded the hardship-rule TL;DR; graded the nickname/Q&A evidence
  opinion/weak.
- sustainability: downgraded the 0.7% claim (average, not per hospital);
  flagged H2's kill test never sought.
- policies: found 3 factual errors (same county, 4 -> 5, VUMC 120/240) and
  1 scope error (HCA 4% emergency only); not yet corrected in the brief.
