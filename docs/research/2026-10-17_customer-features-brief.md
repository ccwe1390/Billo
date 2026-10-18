# Customer base: which features belong in BillScan (research-features)

> Raw subagent report, saved verbatim (non-ASCII transliterated) on 2026-10-17.
> Not yet reviewed or cold-assessed by the orchestrator; numbers are as the agent reported them.
> Source transcript agent id: a53d7914a36473b92

Brief done; no project file written. ASCII check passed (grep found no non-ASCII bytes). A scratch copy, there only for that check, is at <session scratchpad>\rb_customer_brief.md. Stage 10.5 skipped as instructed.

Notes for the orchestrator:
- The browser pane is shared, and another agent navigated my tab mid-read. Verbatim reads therefore used raw HTTP text (urllib/curl stripped, pdftotext, eCFR API). Only the LII 501(r)-6 read used the browser.
- Two of my three sub-agents gave wrong verdicts that verification corrected. Dollar For's 67%/45% figures had been marked "snippet only", and the same applied to the Health Affairs Scholar Medicaid-denial count. Both are now VERIFIED-VERBATIM.

FULL BRIEF TEXT FOLLOWS.

# Research brief - Customer base: which features belong in BillScan

**Date:** 2026-10-17 (collection 23:23-23:44 CDT, UTC-5)
**Question:** What do people facing hospital bills they cannot pay actually need from a tool like BillScan? The people are low-income patients, limited-English-proficiency (LEP) patients, adult children helping parents, and caseworkers, navigators and financial counselors. Which features are missing, and which should be cut or never built?
**For:** Evan and the team. The brief feeds two decisions: (a) what goes into the post-hackathon roadmap (PRD F11 is a DRAFT), and (b) what to say honestly in judge Q&A about who the app serves. It is not for the Sun 2026-10-18 build: the feature freeze has passed.
**Claims under test:** HANDOFF.md (2026-10-17 20:52 CDT), PRD_ROADMAP.md F9/F10/F11, and app/static/app.js plus app/main.py as of the f10 working tree.

## TL;DR

**The rival hypothesis mostly won.** The evidence says people's biggest unmet needs come after the eligibility check that BillScan does well. Policies vary hugely between hospitals. Documents and follow-through sink applications. Collections keep going after people apply or are approved, and people want a human to help. Three of the five predicted missing features survived: collections protection, a human handoff, and an over-income path. One survived only in a smaller form: a "do you already get TennCare / SNAP / WIC?" shortcut instead of a Medicaid screener. In Tennessee, adults without children get no TennCare at all. Itemized-bill requests survived weakly, because that space is crowded.

**The single most concrete gap is in the engine.** BillScan tells over-limit households "not eligible, no packet". Yet Nashville's largest nonprofit system (VUMC) has a catastrophic-assistance route above its income cap, and most nonprofit hospitals have a hardship rule (median cutoff: bills at 20% of income).

**The biggest product gap is coverage.** BillScan knows one synthetic hospital, while free-care income limits nationally range from 41% to 600% of the poverty line.

**Source concentration (disclosed up front):** the patient-barrier figures (29%, 52%, 67%, 45%, 24%) all come from ONE Dollar For survey of its own patients. The policy-variation study (Health Affairs 2024) also uses Dollar For's policy database. Two pillars of this brief therefore share one organization's data. Government and law sources (26 CFR 1.501(r), 45 CFR 92, CFPB, KFF) carry the rest.

## Method

- **Design (stage 4):** three parallel desk-research sub-agents, one per stage-4 theme: (1) competitors and tool documentation, (2) rules and application processes (501(r), TennCare, CFPB, Section 1557), (3) published user research, LEP and literacy guidance. Claude meanwhile read primary sources directly and then re-read every load-bearing claim itself. Re-reads used raw page text: curl/urllib HTML stripped to text, pdftotext on downloaded PDFs, a DSpace metadata API, eCFR's renderer API, and one browser in-page text read (Cornell LII). Claude also read the app's own code and data to say what is already built.
- **Source types run:** federal regulation text (eCFR/LII), agency reports (CFPB, Census via the Nashville study), peer-reviewed papers (Health Affairs, Health Affairs Scholar, AJMC, JCO Oncology Practice, NBER/QJE), survey research (KFF, KFF/NYT), advocacy reports (Dollar For, Community Catalyst, NCLC via agent), hospital policy PDFs (VUMC, Ascension Saint Thomas, HCA), and tool pages (Dollar For, CareRoute, Goodbill, Resolve, Cedar, MyChart, Benefit Kitchen, Single Stop, mRelief).
- **Limitations:**
  - **No primary user research.** No interviews, surveys or usability tests were run. Every "users need X" below is inferred from published studies of other people, not from BillScan's own users. A human would close this gap with:
    - 6-10 semi-structured interviews per persona (LEP patient, adult child, caseworker), recruited through Tennessee Justice Center, Siloam Health or the VUMC financial counselors;
    - a moderated task-based usability test on phones (PRD F11.10's 5-person test is the minimum);
    - a diary study following 3-5 real applications from bill to decision, to see where follow-through breaks.
  - The browser pane was shared with other agents (one read was hijacked mid-session), so most verbatim reads used raw HTTP text, not the browser.
  - Several tn.gov pages, unduemedicaldebt.org, ahrq.gov and HHS returned 403. The TennCare presumptive-eligibility and retroactive-eligibility details below are therefore agent search-summary only.
  - The Nashville language data is from 2017 (ACS 2015).
  - Stage 10.5 (cold assessment) was skipped by instruction: the orchestrator runs one for both briefs.
- **Hypotheses (stage 3):** written in the working notes at 23:23 CDT, before any sub-agent launched or deep collection began. See the next section.

```
Phase effects (2026-10-17):
  8.5 verify  - upgraded 3 claims from agent/snippet to VERIFIED-VERBATIM.
                Caught 1 false negative: Dollar For's 67%/45% figures, which an
                agent flagged "snippet only, do not use", are on the page.
                Added 1 finding: Nashville's top LEP languages are missing from the
                app's 32.
                Killed 0 load-bearing claims; no verdict flipped.
  10.5 assess - skipped by instruction (orchestrator runs one for both briefs)
```

## Stage 3 - hypotheses (23:23 CDT, before collection)

- **H1 (expected): the top 5 missing features are**
  1. a collections-protection layer: 501(r) rights plus a "hold collections while I apply" request;
  2. a public-coverage screen first (TennCare/Medicaid, presumptive eligibility);
  3. an itemized-bill request and dispute letter;
  4. a human-help handoff (211, navigators, legal aid, interpreter);
  5. a not-eligible path (payment plan, negotiation, appeal).
  - *Would be refuted by:* 501(r) not pausing collections on application; TennCare covering few BillScan users; no evidence that users want or benefit from human help; hospitals rarely having over-income routes.
- **H0 (rival):** the main gaps are not missing features. They are (a) policy coverage (one synthetic hospital) and (b) documents and follow-through after the packet. Adding rights or dispute features adds liability with little use.
  - *Would be refuted by:* evidence that understanding and eligibility, not documents or follow-through, is where applications fail.
- **H2 (null for the caseworker persona):** caseworkers need a fast-reset batch mode and a print summary, not consumer features.

**Verdicts:**
- **H1 partly survived:**
  - Item 1 SURVIVED. The regulation text confirms the hold, but it applies to nonprofit hospitals only.
  - Item 2 DIED as a screener and SURVIVED as a shortcut question.
  - Item 3 survived WEAKLY (cheap, but a crowded space).
  - Item 4 SURVIVED.
  - Item 5 SURVIVED STRONGLY and sharpened: the gap is the over-income path inside the engine.
- **H0 mostly SURVIVED.** Policy variation, documentation and follow-through carry the strongest evidence.
- **H2 SURVIVED but thin.** There is one workflow study and no tool-requirements study.

## Findings

### F1. What the app already does, as built (claims under test, read from code)

- Start screen with 32 languages. Photo, then extracted fields, which the user confirms.
- Three questions: household size, income, and "do you file a tax return?"
- A cited tier result and a deadline (240 days from the statement date), plus the document list and a payment-plan contact when not eligible.
- An English cover letter with a translation. Home shows 5 seeded bills plus one-approval coverage. Reminders, with an .ics download.
- The QR chip and a counts dashboard.
- **Not in the app:**
  - any collections language (the letter asks only for a written decision: app/main.py `_letter_en`);
  - an itemized-bill request;
  - any over-income route (`build_packet` raises 422 when not eligible);
  - any benefits shortcut, human referral, interpreter-rights card, appeal step, or real hospital policy.
- **F11 DRAFT already plans:**
  - installable shell, navigation, "keep on this phone", case tracker plus documents checklist (F11.4);
  - read aloud and text size (F11.5), share packet (F11.6);
  - push reminders with a server DB (F11.7), a guarded Q&A box (F11.8);
  - a translation-review programme (F11.9).

### F2. The rules: what an application process actually demands

- **Collections must stop when someone applies (nonprofit hospitals only).**
  - 26 CFR 1.501(r)-6(c)(5)(i)(A): for an incomplete application the hospital must "Suspends any ECAs to obtain payment for the care".
  - (c)(6)(i)(C)(2)-(3): for an eligible applicant it must refund overpayments and "Takes all reasonably available measures to reverse any ECA".
  - (b)(1)(ii) lists credit reporting as an ECA. (c)(3)(i) bars ECAs "for at least 120 days" from the first post-discharge statement. (c)(4)(iii)(A) sets the 240-day deadline floor.
  - Source: LII text read in the browser, plus the eCFR renderer. The rule covers only "tax-exempt hospital organization[s]". Nashville's TriStar hospitals are HCA, which is for-profit. No official TriStar policy page was reachable (404).
- **Hospitals may make people apply for Medicaid first:**
  - The rule: 1.501(r)-6(c)(6)(iv) lets a hospital postpone the decision until a Medicaid application is decided.
  - How common it is: Messac et al. (Health Affairs 2024) call a government-program-first requirement "almost universal".
  - A secret-shopper study found 15 of 204 hospitals volunteered that they need a Medicaid rejection (Health Affairs Scholar 2024, PMC11132125).
  - Nashville varies. Ascension Saint Thomas "will require the uninsured to work with a financial counselor to apply for Medicaid". VUMC instead makes anyone "enrolled in TennCare ... automatically qualified for a 100% discount" (both policy PDFs read with pdftotext).
- **TennCare covers few adult BillScan users.**
  - The TennCare eligibility-categories page lists children, pregnant women (250% FPL), parents/caretakers (a 100% FPL table: $15,960 for 1 person), aged, blind and disabled people, and medically needy children/pregnant women. It lists no category for non-disabled adults without children.
  - KFF (agent, via WebFetch) puts "other adults" in Tennessee at 0% FPL.
  - Hospital presumptive eligibility in TennCare covers children, pregnancy and caretaker categories only, and retroactive coverage is limited to pregnant women and under-19s. Both points are agent search-summary only; tn.gov returned 403.
  - **Consequence:** a full Medicaid screener would screen most adult users out. A "do you already have TennCare?" question is what matters, because at VUMC it means 100% free.
- **Documentation rules.**
  - 1.501(r)-4(b)(3)(i): a hospital "may not deny financial assistance ... based on an applicant's failure to provide information or documentation unless that information or documentation is described in the FAP or FAP application form" (eCFR raw text).
  - In practice (Messac et al., 2,277 hospitals with non-income data), hospitals require proof of income (98.4%), assets (54.4%), a tax return (53.6%), residency (17.7%) and identity (12.6%). 8.4% required or investigated citizenship/legal residency (PMC full text).
- **The real Nashville forms ask what BillScan refuses to ask.**
  - VUMC's application asks for a Social Security Number for the patient and spouse, two years of tax returns and 3 months of pay stubs. It asks for permission "to obtain credit reports" and says "In 4 to 6 weeks, you will receive a letter". It has a separate appeal application.
  - Ascension's asks for 3 months of bank statements (SSN optional, per the agent's local PDF read) and applies an asset test.
  - **Consequence for the packet:** it must tell the user which fields the hospital's own form will ask for, without BillScan collecting them.
- **Over-income routes exist at real hospitals.**
  - VUMC: if income exceeds 3.5x FPG, the patient "may still be eligible for Catastrophic Financial Assistance" when unreimbursed VUMC expenses in a year exceed 100% of household income. VUMC also gives every uninsured patient an "Uninsured Patient Discount" regardless of finances.
  - HCA (Florida Lake Nona summary page, raw text): "medically indigent" means bills exceed 10 percent of annual gross income, with discounts up to 500% FPL.
  - Nationally (Messac et al.): "The median hospital required a bill to amount to 20 percent" of income for hardship.
  - Tennessee law caps what any hospital can charge uninsured patients at 175% of cost (TCA 68-11-262). Source: a Hilltop Institute profile from June 2016, read via pdftotext; the statute itself was not read.
  - The same Hilltop profile says Tennessee "does not require hospitals to adopt or implement financial assistance policies".
- **Presumptive eligibility exists but is opaque.**
  - VUMC's "Alternate Charity Process" qualifies people at 100% on SNAP, WIC, homelessness, subsidized housing or a bankruptcy discharge. Its External Screening Process sends the patient's name, SSN, DOB, address and phone number to a vendor.
  - Oregon OHA (Jan 2025, pdftotext): hospitals using vendor prescreening tools "estimate an overall accuracy rate of 85%".
  - CFPB (blog 2024-10-01): vendor software "often employs third-party data that may be inaccurate".
- **Language access is the hospital's legal duty.** 45 CFR 92.201(b) says language assistance "must be provided free of charge, be accurate and timely". (e)(1) bars requiring an LEP person "to provide their own interpreter". (c)(3) requires human review of machine translation of critical text. 92.11(c)(5)(ix) puts the language-availability notice on "medical billing and collections materials" (eCFR raw text).

### F3. What users experience (published evidence)

- **Information never reaches them.**
  - Dollar For survey (over 1,600 patients, press release, read raw): "only 29% of patients with hospital bills they cannot afford are able to learn about, apply for, and receive charity care". 52% got "no information whatsoever" from the hospital.
  - Washington test calls (2017): 28% of Spanish-language calls vs 90% of English calls got financial-assistance information.
- **The application is the wall, and documents are the brick.**
  - CFPB (2024-10-01, raw): "The burdensome application process often results in few patients completing the application and receiving assistance". It also says at least $2.7B of eligible bills were still billed to patients.
  - Dollar For's report: denials are mainly for the age of the bill (28%) and "paperwork issues (24%)". "Nearly a quarter" call the process somewhat or very hard.
  - UVM Vermont Act 119 study (2025 student presentation, repository abstract read raw): "over 50% of denials were due to incomplete documentation".
  - AJMC 2026 (336 hospitals): financial policy documents average at least 10th-grade readability, while "a slim majority of Americans read below a 6th-grade level" (raw text).
- **Help changes outcomes, and most people lack it.**
  - Dollar For: approval is highest (67%) with help from Dollar For or the hospital, and 45% of applicants get no help (VENDOR-SELF-REPORTED: this is Dollar For's own service).
  - KFF 2022 (2,375 adults): seven in ten adults with health care debt think a state consumer assistance program "would be helpful to them personally".
  - JAMA Health Forum 2024, via Healthcare Dive (agent WebFetch, CLOSE-PARAPHRASE): people without a high-school diploma had about a 20% predicted probability of contacting the billing office, vs over 60% with higher education.
- **Collections hit even approved applicants.**
  - CFPB FDCPA report (Sept 2024, pdftotext): "many complaints from consumers being pursued for debts the consumer alleges have been fully or partially paid through hospital financial assistance"; "the burden falls on the consumer to prove that they do not owe the debt".
  - KFF: 47% of adults with medical/dental debt (or a household member) were contacted by a collection agency in 5 years.
  - CFPB 2022 bulletin: "nearly half" of medical debt collection complaints say the debt is not owed.
- **Bill doubt is common.** KFF: 44% of adults with health care debt did not pay a bill in full because "they weren't sure the bill was accurate".
- **Fear and trust.**
  - KFF/NYT 2025 (1,805 immigrants): avoiding applying for food, housing or health programs over immigration status rose from 8% to 12%, and from 27% to 46% among the likely undocumented.
  - Of those who answered in a non-English language and skipped care, 24% cited language access.
  - **Consequence:** BillScan's "never ask name/SSN/status; store nothing" stance is evidence-backed, and the F11 rule relaxations push against it.
- **Caseworkers.**
  - JCO Oncology Practice 2022 (83 stakeholders, 10 NC sites): staff track applications "using calendars, binders, and sticky notes". Review takes two weeks to over 100 days.
  - No published study of what tools navigators want was found.
- **Debt relief after the fact is weak.** Kluender et al. (NBER w32315; QJE 2025): relieving $169M of medical debt for 83,401 people had "no effects on survey measures of mental and physical health, healthcare utilization, and financial wellness".
  - Inference (not the paper's claim): help before collections is where a tool can matter.

### F4. Language fit for Nashville specifically

- Metro Nashville Language Access Study (Feb 2017, ACS 2015): 9.6% of residents speak English less than "very well". Community respondents named the most common languages as "Spanish, Arabic, Burmese, Kurdish, Nepali, and Somali" (pdftotext).
- BillScan's 32 codes (app/data/languages.json) include Spanish and Arabic but **not Burmese, Kurdish, Nepali or Somali**. They do include Danish, Finnish, Slovenian, Slovak, Norwegian and Croatian.
- **Consequence:** the list follows what Oracle Translate offers, not local need. The 2017 data is stale. Re-check with ACS table C16001 for Davidson County (not run here).

### F5. Competitors and adjacent tools (what they do that BillScan does not)

- **Dollar For (free, EN/ES):** "We'll prepare your application for you and send it to the hospital", then follows up and helps with appeals. Other languages: "find someone to be your translator ... or will do our best using Google Translate" (FAQ, raw). Agent (annual report pdftotext): a self-service portal to track case status and upload documents; 11,119 applications in 2024.
- **CareRoute (paid, Bill Defense at 25% of savings capped at $1,000, per agent):**
  - Free letter templates generated "in your browser". Its charity-care cover letter "Requests temporary billing hold during review" and cites 501(r) (raw).
  - Per-hospital Nashville pages (e.g. TriStar, "Verified July 2026").
  - Its Tennessee page wrongly says a medical-debt credit-reporting ban took effect: the agent found SB 402 still in committee. Accuracy is not assured.
- **Goodbill and Resolve:** human negotiators on a success fee (agent, via WebFetch).
- **Cedar Cover:** hospital-bought Medicaid/marketplace matching (vendor claims).
- **MyChart:** the financial-assistance application in the portal asks for assets and expenses, then "A financial counselor will contact you" (agent, via WebFetch).
- **Benefit Kitchen:** "never asks for Social Security numbers or immigration status" (agent). Closest to BillScan's privacy stance; it screens multiple programs.
- **mRelief:** income ranges, few questions, biased against false negatives (agent).
- **Single Stop:** caseworker dashboard (agent).
- **Not found anywhere:** a state-run charity-care web screener in NJ, WA, OR, CO, MD or CA (agent); a production tool combining bill photo, rules and many languages (prior brief 2026-10-17).

## Ranked feature candidates (top 10)

Effort assumes FastAPI + vanilla JS as built: S is under half a day, M is 1-3 days, L is more than 3 days. "Rule risk" is risk to the hard rules: no diagnosis, synthetic data, nothing stored, never ask name/status/SSN.

**1. Real Nashville policies (VUMC first, then Ascension Saint Thomas and Nashville General).** Encode each public FAP as policy JSON with citations, page numbers and a `review_by` date. Serves every persona.
- **Evidence:**
  - free-care limits range from 41% to 600% FPL (Messac, PMC12230784);
  - VUMC's 300%/350% FPG tiers, catastrophic rule and TennCare auto-qualify;
  - Ascension's 250%/400% tiers, asset test and Medicaid-first rule (both PDFs read).
  - Today's estimate is "not about your bill" for any real user (app.js r_mismatch).
- **Effort:** L.
- **Rule risk:** medium. Real policies are public documents, not patient data, but they break the F10 rule "nothing imitates a real hospital". A wrong threshold misleads real people, so a reviewer is needed. Needs Evan's call.
- **Status:** not in the app; not in F11. It was the original F3 plan, gated out at 3:00 PM.
- *This is the precondition that makes every other candidate matter.*

**2. Over-income path ("you may still qualify").** Replace "not eligible, no packet" with policy-driven checks:
- catastrophic/hardship (VUMC: expenses over 100% of income; median hospital: 20%);
- the uninsured discount;
- "ask for an interest-free payment plan in writing";
- a packet that requests a hardship review.

Serves low-income patients and adult children.
- **Evidence:** VUMC FAP; HCA 10% medically indigent; Messac hardship median 20%; Community Catalyst guide 4 ("make sure that it says that interest, late fees, and other penalties will not apply").
- **Effort:** M (policy JSON fields, an engine rule with tests, strings x 32).
- **Rule risk:** low. The engine still decides, from income and bills the user already confirms. It needs a "total medical bills this year" question.
- **Status:** not in the app (build_packet 422); not in F11.

**3. Human-help handoff + interpreter-rights card.** On Result and Packet, add a short "Want a person to help?" card:
- Dollar For (free, EN/ES, submits for you);
- the hospital's financial counselor;
- Tennessee Justice Center (TennCare families, 615-255-0331);
- 211 (dial 211 or text a ZIP to 898-211).

Plus a card in the user's language with an English line to show staff: "I need a free interpreter. Hospitals must provide one."

Serves LEP patients, adult children and low-literacy users.
- **Evidence:** 45 CFR 92.201(b) and (e)(1); KFF 7 in 10 want consumer assistance; Dollar For 67% approval with help (vendor); Washington 28% vs 90% call test.
- **Effort:** S.
- **Rule risk:** low. Static text; no data leaves the phone. The phone numbers need a dated check.
- **Status:** not in the app; not in F11.

**4. Collections protection (nonprofit hospitals only).** Three parts:
- (a) add to the cover letter: "Please pause any collection activity while you review this application, as your policy and federal rules require";
- (b) a rights card: 120 days before collections; applying pauses them; approval means refunds and reversal;
- (c) a one-page "I was approved but a collector contacted me" letter template.

Serves all patients and adult children.
- **Evidence:** 1.501(r)-6 (c)(3)(i), (c)(5)(i)(A), (c)(6)(i)(C) (LII browser read); CFPB FDCPA 2024 "the burden falls on the consumer"; KFF 47% contacted by collectors. CareRoute already ships (a), so it is table stakes, not a differentiator.
- **Effort:** S.
- **Rule risk:** low-medium. It must not read as legal advice. It is shown only when the policy JSON marks the hospital tax-exempt, because 501(r) does not cover HCA/TriStar.
- **Status:** not in the app; not in F11.

**5. "Do you already get TennCare, SNAP or WIC?" shortcut.** One optional yes/no question per program. Where the policy has a presumptive route, the result says "this may qualify you for 100% without income papers" and the document list shrinks to the benefit letter. Serves low-income patients and caseworkers.
- **Evidence:** VUMC TennCare auto-qualify and its Alternate Charity Process (SNAP, WIC, homelessness, subsidized housing); Community Catalyst model policy; 2 of 204 hospitals in the secret-shopper study accepted SNAP as automatic.
- **Effort:** S-M.
- **Rule risk:** low-medium. It is benefit status, not immigration status, but it is sensitive: keep it optional, never sent beyond /evaluate, never stored.
- **Status:** not in the app; not in F11.

**6. Per-policy "government program first" step.** When a policy requires a TennCare decision first (Ascension), the checklist gets "Apply to TennCare first (TennCare Connect or 855-259-0701); bring the decision letter". When it does not (VUMC), the step is omitted. Serves low-income patients and caseworkers.
- **Evidence:** Messac "almost universal"; 15 of 204 hospitals need a Medicaid rejection; 1.501(r)-6(c)(6)(iv). The Ascension vs VUMC contrast is from both PDFs.
- **Effort:** S (a policy flag plus a checklist line).
- **Rule risk:** low. It is not an eligibility screener: no pregnancy or disability questions.
- **Status:** not in the app; not in F11.

**7. Document help: hospital-form preview, substitutes, self-attestation.**
- Per policy, list exactly what the hospital's own form will ask for, with the note "BillScan does not collect these: you fill them on the hospital's form". VUMC's asks for SSN, credit-report permission, 2 years of tax returns and 3 months of stubs.
- List accepted substitutes, plus a "no income / cash income" self-statement template where the policy allows one.

Serves all personas.
- **Evidence:** UVM "over 50% of denials" from incomplete documentation (single-source student work); Dollar For 24% paperwork denials; Messac documentation shares; 1.501(r)-4(b)(3)(i); Community Catalyst model policy on self-attestation.
- **Effort:** S-M once item 1 exists.
- **Rule risk:** low, but it must state honestly that the hospital form asks for an SSN even though BillScan never will. The self-statement must be signed by the person, and BillScan must not word facts for them.
- **Status:** partly built (a 3-item synthetic checklist); F11.4 adds check-offs.

**8. Follow-through: proof of sending, decision wait, denial and appeal.**
- A dated "I sent it on ___ by ___" record and "keep a copy and your approval letter".
- The hospital's stated decision time (VUMC: "4 to 6 weeks").
- An "If you are denied" card: VUMC has an appeal application; a hospital must say what is missing before denying an incomplete application.

Serves adult children and caseworkers.
- **Evidence:** CFPB FDCPA 2024; JCO OP 2022 ("calendars, binders, and sticky notes"; 2 weeks to 100+ days); VUMC application text; 1.501(r)-6(c)(5)(i)(B).
- **Effort:** S in page memory; M with F11.3/F11.4 persistence.
- **Rule risk:** medium if persisted (that is F11.3's opt-in question); low in memory.
- **Status:** partly built (the day-30 follow-up reminder plus .ics); F11.4 has status chips; no appeal step anywhere.

**9. Itemized-bill request letter.** A one-page request in English with a translation beside it; useful before paying or applying. Serves patients and insured users too.
- **Evidence:** KFF 44% unsure the bill was accurate; CFPB 2022 "nearly half" of medical collection complaints say the debt is not owed; Community Catalyst: "Always ask for an itemized bill so you can check for errors"; Minnesota AG (agent, via WebFetch).
- **Effort:** S.
- **Rule risk:** low.
- **Status:** not in the app; not in F11. Do NOT grow it into an error-checking engine: see Cut list.

**10. Local-language priority: Burmese, Kurdish, Nepali, Somali + reviewed Spanish and Arabic.** Add Nashville's named community languages (via Command A with the existing placeholders, as Hindi does) and put F11.9 reviewers on Spanish and Arabic first. Serves LEP patients.
- **Evidence:** Metro Nashville Language Access Study 2017 (stale); 45 CFR 92.201(c)(3) human-review norm; AJMC 2026 (via the prior brief: 61.0% of hospitals posting a policy translate it).
- **Effort:** M (plus a native reviewer per language).
- **Rule risk:** medium. Machine translation into lower-resource languages has unknown quality. The number lock covers digits, not meaning (record AI already found 12 meaning-flipped strings).
- **Status:** not in the app (none of the four); F11.9 covers review but not language choice.

**Just outside the top 10:**
- F11.5 read aloud (supported by AJMC "slim majority read below a 6th-grade level" and agent-reported PIAAC 2023: 28% at Level 1 or below);
- a caseworker fast-reset / multi-household mode (H2; one workflow study only);
- F11.6 share packet (adult child to parent).

## Features to cut or not build

1. **F11.7 push reminders with a server-side database: cut, or defer indefinitely.**
   - It breaks "the server keeps nothing" for the users most likely to fear exposure (KFF/NYT: 46% of likely-undocumented immigrants avoided applying for programs).
   - It adds key management, a breach surface and state privacy-law work (F11.7 names these itself) for a benefit the .ics file already delivers.
   - Pew's finding that privacy concern rises once people learn app data lacks federal protection is agent search-summary only, so it carries no weight here.
2. **F11 optional nickname (amending hard rule 3): cut.** Zero task value. Any name field risks deterring the fear-sensitive group. Personalization is not a need any source surfaced.
3. **F11.8 "Ask about my result" box: do not build.**
   - General chatbots already raise financial assistance: record AC found 13/13 runs do. So a chat box is a commodity, not BillScan's job.
   - It is the highest-risk surface for invented numbers and legal or medical advice.
   - A human handoff (candidate 3) answers the same need more safely.
4. **A full TennCare/Medicaid eligibility screener: do not build.**
   - Tennessee gives non-disabled adults without children 0% FPL eligibility.
   - The useful categories need pregnancy, disability and age questions, which brush the no-diagnosis rule.
   - Cedar Cover and hospital financial counselors already do this.
   - Replace it with candidates 5 and 6.
5. **A bill-coding or error-detection engine: do not build** (prior brief: crowded; uninsured users have no EOB). Keep only the itemized-bill request (candidate 9).
6. **Submitting applications or negotiating for the user: do not build.** It requires storing documents, a human staff and legal exposure. Dollar For does it free (EN/ES), and Goodbill, Resolve and CareRoute do it for a fee. Refer instead (candidate 3).
7. **Credit-report-law claims (e.g. "Tennessee bans medical debt on credit reports"): never ship.**
   - SB 402 / HB 539 were not enacted (agent read the legislature page).
   - The CFPB rule was vacated in July 2025 (agent, search summary).
   - The bureaus' under-$500 and paid-debt policies are voluntary and can change.
8. **More machine-translated languages chosen by vendor availability:** stop, and stop leading with "32" as the claim. It is a count of what Oracle offers. Nashville's named community languages are not in it (F4).
9. **Deprioritize, not cut:**
   - F11.2 haptics and motion: no source ties it to completion.
   - F10.5 counts dashboard: no patient-side value; demo only; do not extend it.

## Verification table (stage 8.5)

| Load-bearing claim | Source | Verdict |
|---|---|---|
| A FAP application (even incomplete) suspends ECAs; approval brings refunds and ECA reversal; 120-day ECA bar; 240-day floor | 26 CFR 1.501(r)-6, LII (browser in-page text) | VERIFIED-VERBATIM |
| A hospital may postpone the decision until Medicaid is decided | 1.501(r)-6(c)(6)(iv), LII | VERIFIED-VERBATIM |
| No denial for missing documents not described in the FAP/form | 1.501(r)-4(b)(3)(i), eCFR raw | VERIFIED-VERBATIM |
| Free interpreters; no requiring your own; human review of critical machine translation; notice on billing materials | 45 CFR 92.201, 92.11, eCFR raw | VERIFIED-VERBATIM (in force: agent read HHS 2026-06-02 notice, CLOSE-PARAPHRASE) |
| Free-care limits 41-600% FPL; documentation shares; 8.4% citizenship; Medicaid-first "almost universal"; hardship median 20% | Messac et al., Health Affairs 2024, PMC full text raw | VERIFIED-VERBATIM |
| VUMC: TennCare auto-100%; Alternate Charity Process (SNAP/WIC...); catastrophic above 3.5x FPG; uninsured discount; form asks SSN and credit permission; appeal application | VUMC FAP and application PDFs, pdftotext | VERIFIED-VERBATIM |
| Ascension Saint Thomas requires uninsured patients to apply for Medicaid; 250%/400% tiers; asset test | Ascension TN FAP PDF, pdftotext | VERIFIED-VERBATIM |
| TennCare has no category for non-disabled adults without children | tn.gov eligibility categories page (raw) + KFF (agent) | CLOSE-PARAPHRASE: absence on the list read raw; KFF 0% via WebFetch |
| 29% learn/apply/receive; 52% no info; 1,600 surveyed | Dollar For press release, raw | VERIFIED-VERBATIM (VENDOR-SELF-REPORTED survey) |
| 67% approval with help; 45% no help; denials 28% bill age / 24% paperwork | Dollar For "Path to Charity Care", raw | VERIFIED-VERBATIM (agent had marked it snippet-only) |
| Over 50% of denials from incomplete documentation (Vermont) | UVM ScholarWorks abstract via DSpace API | VERIFIED-VERBATIM (student presentation, single-source) |
| Burdensome application; $2.7B eligible but billed | CFPB blog 2024-10-01, raw | VERIFIED-VERBATIM |
| Collections after approval; "burden falls on the consumer" | CFPB FDCPA annual report 2024, pdftotext | VERIFIED-VERBATIM |
| 7 in 10 want consumer assistance; 47% contacted by collectors; 44% unsure of accuracy | KFF Health Care Debt Survey, raw | VERIFIED-VERBATIM |
| Immigrant avoidance 8% -> 12%, 27% -> 46% | KFF/NYT 2025 survey, raw | VERIFIED-VERBATIM |
| Nashville top languages include Burmese, Kurdish, Nepali, Somali; 9.6% LEP | Metro Language Access Study 2017, pdftotext | VERIFIED-VERBATIM (data 2015) |
| CareRoute letter requests a billing hold; generated in the browser | careroute.ai template page, raw | VERIFIED-VERBATIM |
| Dollar For prepares and sends the application; EN/ES only | dollarfor.org home + FAQ, raw | VERIFIED-VERBATIM |
| HCA "medically indigent" = bills over 10% of income | HCA Lake Nona FAP summary, raw | VERIFIED-VERBATIM (Florida page; TriStar's own unreachable) |
| TN 175%-of-cost cap for uninsured; TN does not require FAPs | Hilltop Institute TN profile (2016), pdftotext | VERIFIED-VERBATIM for the profile; statute NOT read; stale |
| Staff track cases with binders and sticky notes; 2 weeks to 100+ days | JCO OP 2022, PMC raw | VERIFIED-VERBATIM |
| 15/204 hospitals require a Medicaid rejection; 2 accept SNAP | Health Affairs Scholar 2024, PMC raw | VERIFIED-VERBATIM |
| Debt relief: no effect on mental/physical health or financial wellness | NBER w32315, raw | VERIFIED-VERBATIM |
| TennCare hospital presumptive eligibility excludes general adults; retro coverage only for pregnant women / under-19 | agent search summaries (tn.gov 403) | UNREACHABLE - single-source, unverified |
| Tennessee credit-reporting ban not enacted | TN legislature bill page (agent, WebFetch) | CLOSE-PARAPHRASE |
| Low-education users rarely contact billing (20% vs 60%) | JAMA Health Forum via Healthcare Dive (agent) | CLOSE-PARAPHRASE |

**Structural checks:**
- **Same-source dependency:** the patient-side barrier numbers (29/52/67/45/28/24) are one Dollar For survey of Dollar For's own patients (selection bias toward people who found help). Messac et al.'s policy data comes from "the 2024 Dollar For database". The headline "documents and help matter" therefore leans on one organization twice. Independent counterweights exist: CFPB (government), UVM (a different state; small, student), the JCO OP workflow study and the KFF surveys.
- **Interest concentration:** about 6 of 24 load-bearing numbers are VENDOR/ADVOCACY-SELF-REPORTED (Dollar For). That is under half, but it is disclosed in the TL;DR because it is concentrated in one organization.

## Numbers register

| Number | What it claims | Source | Date | Interest class | Verdict |
|---|---|---|---|---|---|
| 41%-600% FPL | range of free-care income limits, 2,770 nonprofit hospitals | Messac, Health Affairs 43(11) | 2024-11 | INDEPENDENT (uses Dollar For data) | VERIFIED-VERBATIM |
| 98.4 / 54.4 / 53.6 / 17.7 / 12.6% | hospitals requiring proof of income / assets / tax return / residency / identity | Messac | 2024-11 | INDEPENDENT | VERIFIED-VERBATIM |
| 8.4% | hospitals requiring or investigating citizenship/legal residency | Messac | 2024-11 | INDEPENDENT | VERIFIED-VERBATIM |
| 20% | median hardship threshold, bill as share of income | Messac | 2024-11 | INDEPENDENT | VERIFIED-VERBATIM |
| 29% | patients with unaffordable bills who learn about, apply for and receive charity care | Dollar For survey, n > 1,600 | 2024 | VENDOR-SELF-REPORTED (advocacy) | VERIFIED-VERBATIM |
| 52% | got no FA information from the hospital | Dollar For | 2024 | VENDOR-SELF-REPORTED | VERIFIED-VERBATIM |
| 67% / 45% | approval with help / applicants with no help | Dollar For | 2024 | VENDOR-SELF-REPORTED (own service) | VERIFIED-VERBATIM |
| 28% / 24% | denials for bill age / paperwork | Dollar For | 2024 | VENDOR-SELF-REPORTED | VERIFIED-VERBATIM |
| > 50% | Vermont FA denials from incomplete documentation | UVM student presentation | 2025 | INDEPENDENT (unreviewed) | VERIFIED-VERBATIM |
| $2.7B | eligible bills still billed to patients | CFPB blog (underlying source not traced) | 2024-10-01 | INDEPENDENT (gov) | VERIFIED-VERBATIM |
| 7 in 10 | adults with health care debt who think consumer assistance would help them | KFF, n = 2,375 | 2022-06 | INDEPENDENT | VERIFIED-VERBATIM |
| 47% | adults with debt contacted by a collector in 5 years | KFF | 2022-06 | INDEPENDENT | VERIFIED-VERBATIM |
| 44% | adults with debt who did not pay because unsure the bill was accurate | KFF | 2022-06 | INDEPENDENT | VERIFIED-VERBATIM |
| 12% / 46% | immigrants / likely-undocumented who avoided applying for programs | KFF/NYT, n = 1,805 | 2025-11 | INDEPENDENT | VERIFIED-VERBATIM |
| 24% | non-English respondents who skipped care citing language access | KFF/NYT | 2025-11 | INDEPENDENT | VERIFIED-VERBATIM |
| 10th grade | mean readability of hospital financial policy documents, n = 336 | AJMC 32(7) | 2026-07 | INDEPENDENT | VERIFIED-VERBATIM |
| 28% vs 90% | Spanish vs English calls getting FA information | Columbia Legal Services / The Stranger | 2017-08-30 | ADVOCACY test | VERIFIED-VERBATIM (prior brief) |
| 15 / 204; 2 / 204 | hospitals requiring a Medicaid rejection; accepting SNAP as automatic | Health Affairs Scholar 2(5) | 2024-05 | INDEPENDENT | VERIFIED-VERBATIM |
| 85% | hospital-estimated accuracy of vendor presumptive screening (Oregon) | OHA interview summary | 2025-01 | INDEPENDENT (gov; hospital self-estimates) | VERIFIED-VERBATIM |
| 9.6% | Nashville residents speaking English less than "very well" | Metro Language Access Study (ACS 2015) | 2017-02 | INDEPENDENT (gov) | VERIFIED-VERBATIM; stale |
| 3.0x / 3.5x FPG; > 100% of income | VUMC free-care cap / discount cap / catastrophic trigger | VUMC FAP (effective 7/1/2026) | 2026 | PRIMARY (hospital policy) | VERIFIED-VERBATIM |
| 250% / 400% FPL | Ascension Saint Thomas free / discount caps | Ascension TN FAP | 2025-07-01 | PRIMARY | VERIFIED-VERBATIM |
| 10% of income | HCA "medically indigent" trigger (Florida page) | HCA Lake Nona | read 2026-10-17 | PRIMARY | VERIFIED-VERBATIM |
| 175% of cost | TN cap on uninsured charges | Hilltop profile citing TCA 68-11-262 | 2016-06 | INDEPENDENT (secondary) | statute NOT read |
| 83,401 / $169M | people / debt relieved in the RCTs | Kluender et al., NBER w32315 | 2024-04 | INDEPENDENT | VERIFIED-VERBATIM |
| 0% FPL | TN eligibility for "other adults" | KFF state indicator (agent) | data 2026-01 | INDEPENDENT | CLOSE-PARAPHRASE |

## Thin / missing

- **BillScan's own users:** zero interviews, usability tests or completion data. PRD F5 V2/V3 and F11.10 were planned; record AC has only the chatbot test (V1). MISSING.
- **LEP-specific evidence on medical bills or financial assistance:** no study measures application or approval rates by language. Searches: agent "limited English proficiency adults medical debt OR problems paying medical bills"; Claude '"limited English proficiency" OR "non-English" patients "financial assistance" OR "charity care" ... disparities application'; the prior brief (2026-10-17) found none by language either. Closest: the Washington call test, the AJMC translation study, KFF/NYT. Negative held across 3 searches.
- **What navigators and counselors want from tools:** no published requirements study. Agent query "application counselors navigators needs tools survey study". Only workflow evidence (JCO OP).
- **A completed RCT of financial navigation for hospital bills:** none with results found (agent, two queries). Only protocols and a 19-patient pilot.
- **Dollar For's screener questions:** not published (agent; the form was not opened).
- **Official TriStar/HCA Nashville policy:** 404 on tristarhealth.com. Only CareRoute's third-party page, unverified.
- **Tennessee statewide LEP share and current Davidson County languages:** the Census API call returned nothing in this run and MPI returned 403. Pull ACS C16001.
- **TennCare presumptive/retroactive rules from tn.gov itself:** 403. Agent search summaries only.
- **A state-run web charity-care screener:** none found in 6 states (agent). One route only; not re-run a second way. Treat as provisional.
- **Evidence for app-like features** (motion, haptics, installability) improving completion for this population: none sought or found. That is why F11.2 is deprioritized, not supported.

## What would change this conclusion

- **Interviews show users fail at understanding, not documents or follow-through.** H0 would weaken and explanation features (read aloud, Q&A) would rise. This is the untested falsifier: the evidence above is about other people's applications, mostly through Dollar For.
- **A caseworker partner adopts BillScan.** H2 becomes the main persona, and the multi-household mode and print summary move into the top 5.
- **Evan keeps the synthetic-only scope permanently.** Candidates 1, 6 and 7 collapse to demo value, and the app stays a pitch, not a tool.
- **A Tennessee statute** (e.g. a charity-care mandate or a credit-reporting ban) passes. Candidate 4 extends to for-profit hospitals and the rights card changes.
- **Native reviewers find the Burmese/Kurdish/Nepali/Somali machine output unusable.** Candidate 10 becomes "human-translated short cards only".

## Sources (all accessed 2026-10-17)

Primary law and government
- 26 CFR 1.501(r)-6: https://www.law.cornell.edu/cfr/text/26/1.501(r)-6
- 26 CFR 1.501(r)-4: https://www.ecfr.gov/api/renderer/v1/content/enhanced/current/title-26?part=1&section=1.501(r)-4
- 45 CFR 92.201: https://www.ecfr.gov/api/renderer/v1/content/enhanced/current/title-45?part=92&section=92.201
- 45 CFR 92.11: https://www.ecfr.gov/api/renderer/v1/content/enhanced/current/title-45?part=92&section=92.11
- 45 CFR 164.510 (HIPAA family/payment disclosure, background): https://www.ecfr.gov/api/renderer/v1/content/enhanced/current/title-45?part=164&section=164.510
- TennCare eligibility categories: https://www.tn.gov/tenncare/members-applicants/eligibility/categories.html
- CFPB blog, Medical Debt and Non-Profit Hospital Billing Practices (2024-10-01): https://www.consumerfinance.gov/about-us/blog/medical-debt-and-non-profit-hospital-billing-practices/
- CFPB FDCPA Annual Report (2024-09): https://files.consumerfinance.gov/f/documents/cfpb_fdcpa-2024-annual-report_2024-09.pdf
- CFPB Complaint Bulletin, medical billing (2022-04): https://files.consumerfinance.gov/f/documents/cfpb_complaint-bulletin-medical-billing_report_2022-04.pdf
- Oregon OHA, Hospital Prescreening Implementation Interview Summary (2025-01): https://www.oregon.gov/oha/HPA/ANALYTICS/HospitalReporting/Hospital%20Prescreening%20Implementation%20Interview%20Summary.pdf
- Metro Nashville Language Access Study (2017-02): https://filetransfer.nashville.gov/portals/0/sitecontent/Human%20Realations%20Commission/docs/publications/MetroLanguageAccessStudy.pdf
- Hilltop Institute, Tennessee community benefit profile (2016-06): https://www.hilltopinstitute.org/wp-content/uploads/hcbp/hcbp_docs/HCBP_CBL_TN.pdf

Hospital policies
- VUMC FAP (effective 7/1/2026): https://files.vanderbilthealth.com/sites/default/files/2026-10/financial-assistance-policy-english.pdf
- VUMC application: https://files.vanderbilthealth.com/sites/default/files/2026-10/financial-assistance-application-english.pdf
- Ascension Saint Thomas FAP (2025-07-01): https://healthcare.ascension.org/-/media/healthcare/financial-assistance/tennessee/tnnas/fap/runningfile_tnnas_english_financial-assistance-policy.pdf
- HCA UCF Lake Nona FAP summary: https://www.hcafloridahealthcare.com/locations/ucf-lake-nona-hospital/for-patients/financial-assistance-policy-and-application

Research and surveys
- Messac et al., Health Affairs 2024, DOI 10.1377/hlthaff.2023.01615: https://pmc.ncbi.nlm.nih.gov/articles/PMC12230784/
- Randall et al., Health Affairs Scholar 2024, DOI 10.1093/haschl/qxae062: https://pmc.ncbi.nlm.nih.gov/articles/PMC11132125/
- Randall et al., Readability of Hospital Patient Financial Policy Documents, AJMC 2026: https://www.ajmc.com/view/readability-of-hospital-patient-financial-policy-documents
- JCO Oncology Practice 2022, DOI 10.1200/OP.21.00894: https://pmc.ncbi.nlm.nih.gov/articles/PMC9509146/
- Kluender et al., NBER w32315: https://www.nber.org/papers/w32315
- KFF Health Care Debt Survey (2022-06): https://www.kff.org/health-costs/kff-health-care-debt-survey/
- KFF/NYT 2025 Survey of Immigrants: https://www.kff.org/immigrant-health/kff-new-york-times-2025-survey-of-immigrants-health-and-health-care-experiences-during-the-second-trump-administration/
- Hart et al., Early Impacts of VT Act 119 (UVM, 2025): https://scholarworks.uvm.edu/items/16148068-479b-4ca2-85d5-e1121ce9d14c

Advocacy and tools
- Dollar For home, FAQ, press release, Path to Charity Care: https://dollarfor.org/ ; https://dollarfor.org/faq ; https://dollarfor.org/press/press-release-14-billion-gap/ ; https://dollarfor.org/the-path-to-charity-care/
- Community Catalyst Guide 4 (2026-01-13): https://communitycatalyst.org/resource/guide-4-i-received-a-medical-bill-i-cannot-afford-to-pay/
- Community Catalyst model FA policy (2024-03): https://communitycatalyst.org/wp-content/uploads/2024/03/Non_Profit_Hospitals_Model_Financial_Assistance.pdf
- CareRoute charity-care cover letter and TriStar page: https://www.careroute.ai/medical-bill-letter-templates/charity-care-cover-letter ; https://www.careroute.ai/hospital-financial-assistance/tristar-health
- Agent-read, not re-read by Claude (CLOSE-PARAPHRASE at most):
  - Goodbill, Resolve, Cedar Cover, MyChart help, Benefit Kitchen, Single Stop, mRelief (Digital Government Hub), United Way 211 Nashville, Tennessee Justice Center, Legal Aid Society of Middle Tennessee, NJ charity care, CA HCAI;
  - TN legislature SB0402 page, KFF Medicaid adult-eligibility indicator, JAMA Health Forum via Healthcare Dive, Dollar For Annual Report 2024.
- Prior project brief: docs/research/2026-10-17_bill-decoder-crowding.md.
