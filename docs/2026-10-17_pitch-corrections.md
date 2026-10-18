# Pitch corrections - what rev2 says vs what the build does (DRAFT for Evan)

> **2026-10-18 08:51 CDT - THE DEMO NOW USES REAL POLICIES (bdc76df, live 08:48 CDT).**
> The app holds the real published financial assistance policies of Vanderbilt
> University Medical Center and Ascension Saint Thomas, read from their PDFs and
> cited by page. Every bill is still SYNTHETIC ("NOT ISSUED BY <hospital>"). A bill
> from any other real hospital, or with no hospital name, gets no estimate (bill-10 is the fictional Cumberland, with its own fictional policy), only a warning and a "Want a person to
> help?" card. The rows below were updated for this. Say "real published policy,
> synthetic bill". NEVER say or imply the hospitals reviewed, endorsed or signed off
> on anything: they did not.
>
> **2026-10-18 07:40 CDT - body rewritten to match the LIVE app (5af2f1f, deployed
> 2026-10-18 00:07 CDT; audit 3 finding 3).** Every row below is true for what is live
> now. Live: 32 language options (English + 31; Spanish, Arabic and both Chinese
> scripts were drafted with AI and are marked for native-speaker review - NOT yet
> reviewed by a fluent person; the other 27 are machine-translated by Oracle and
> labelled so), the Home screen with 5 synthetic bills, reminders + calendar file, the QR on
> synthetic bill-02, /dashboard.html, 10 synthetic test bills. NOT yet checked on a
> real phone: the QR scan, photo upload, the https padlock. Earlier banners (20:52,
> 23:52) are folded in; git history has the old text.


Written 2026-10-17 by Claude from the full audit (docs/2026-10-17_full-audit.md,
finding A1). The pitch, demo script and judge answers live in
docs/2026-10-17_HackTN26_Health_Access_Plan_rev2.txt, which is kept as written.
Present from rev2 WITH this sheet applied. Each row: the rev2 line, why it is
wrong, and a replacement that is true today. Replacement wording is a draft:
Evan or a teammate should say it in their own words.

## Pitch (rev2 lines 343-348)

| rev2 | Problem | Say instead |
|---|---|---|
| 343 "only 29% ... learn about this help, apply, and get it. More than half say their hospital never told them." | Both numbers are one Dollar For patient survey; "never told" overstates it | "A Dollar For patient survey found only 29% of patients with unaffordable hospital bills got financial assistance, and 52% got no information from their hospital." |
| 344 "Spanish or Arabic, Nashville's top two languages after English" | Not verified as a ranking (cold assessment: margins of error may erase it; data from 2017/ACS) | "a parent who speaks Spanish or Arabic" - drop "Nashville's top two languages after English" |
| 347 "About 2,984 US nonprofit hospitals must run programs like this, and Dollar For estimates at least $14 billion..."; "Hospitals and community groups pay per completed application" | $14B: do NOT say (built on Dollar For's own estimates). Per-application pricing contradicts our sustainability brief. 2,984 approximates the covered count | "About 2,984 US nonprofit community hospitals must run financial assistance programs (AHA). BillScan is free for families, always. We'd start with a free, grant-funded pilot: one Nashville hospital and one community partner; how hospitals would pay is not decided." |
| 345 "The hospital prints a code on its statement. She scans it and photographs the bill." | No real hospital prints our code. Our synthetic bill-02 does carry a QR that opens the app with that hospital selected (real-phone scan not yet checked) | "In a pilot, the hospital prints a code on its statement. On our synthetic bill, she scans it and photographs the bill." Rehearse the scan; if it fails, open the address instead |
| 345 "checks her answers against the hospital's own published policy, page cited" | TRUE now for VUMC and Ascension Saint Thomas: the rules are their published policies, each with its page; the bill is synthetic | Keep it. Add: "This is VUMC's real published policy; the bill is synthetic. VUMC has not reviewed this tool." |
| 346 brackets [result of task 1], [N], [x], [y] | No V1/V2/V3 result exists yet | Fill each from a measured result or cut the sentence (rev2's own rule, line 342) |
| 348 "nothing a family enters is stored" | TRUE for what she enters (bill fields, answers): the app keeps none of it. The web server's standard access log does keep IP address, time and page (audit 3 A2, Evan deciding). Do NOT use F9 fix 1 ("bills stay on their own phone"): there is no save feature | Keep rev2's sentence; if asked: "the web server keeps a standard access log, never your bill or answers" |

## Demo script (rev2 lines 350-398)

| rev2 | Problem | Say / do instead |
|---|---|---|
| 0:00 "Scan the QR code"; "VUMC already selected"; "The hospital prints this code" | The QR on synthetic bill-02 now opens the app with VUMC shown (reprint bill-02: the QR changed at 08:3x). The hospital does not print this code | Scan the QR on the NEW bill-02 (rehearse first; fallback: open http://207.211.181.174/ - https also works). "This is running live on Oracle Cloud. The bill is synthetic; the policy is VUMC's real published one." |
| 0:14 "It left the blurry date blank instead of guessing." | Do NOT say it. On the re-rendered bill-02 (2026-10-18 08:49, n=1) the model read the blurred date of service as 2026-11-04, the payment due date. The old render (2026-10-17) left it blank | Say: "Nothing is used until she confirms it" - and show her checking each field. If a date is wrong, fix it on screen: that is the point of the confirm step |
| 0:56 "VUMC's policy opens at the cited page" | TRUE now: the citation links to VUMC's own policy PDF with the page (some phone PDF viewers ignore the page jump; the page number is also printed) | "Here is the cited page of VUMC's own policy." Rehearse on the presenting phone |
| 1:06 packet; rev2 345 "a finished packet: the application filled in" | NOT an application: the packet lays out her answers for the hospital's own form, the documents, the deadline and a cover letter; its banner says "Do not send this packet; apply on the hospital's own form" | Tap "Create my application packet", then show it: "her answers laid out for VUMC's own form, the documents to bring, the deadline and a cover letter. She fills in VUMC's form - the link is right there." |
| 1:24 "Save to Dad's bills", five bills, "Up to $X", reminders | LIVE, but nothing is saved: Home shows 5 synthetic demo bills for the household just entered; with a free-care household it reads "Up to $8,837.65 could be reduced"; reminders + calendar file appear only for eligible families | Keep the beat. Say "five synthetic bills" and "an estimate - the hospital decides". Do not say "saved" |
| 1:42 partner dashboard | LIVE at /dashboard.html: anonymous counts only (values under 10 shown as "<10"), no personal data | Show it; say "counts only, nothing about any family" |

## Slides (rev2 lines 402-408)

| Slide | Problem | Instead |
|---|---|---|
| 1 "in Arabic or Spanish" | The app offers 32 language options; none has been reviewed by a fluent speaker | "in 32 language options" (Spanish, Arabic and both Chinese scripts drafted with AI and marked for native-speaker review; 27 more machine-translated by Oracle and labelled "Machine translated"). If asked who translated: "AI drafts; a native-speaker review is our next step." |
| 5 "Starts from a QR code"; "four Oracle services" | The QR is on our synthetic bill only. MySQL HeatWave was never used and is deleted | "Starts from a photo of the bill (in a pilot, from a QR on the statement)." Oracle Cloud: one compute VM, Generative AI (Cohere Command A Vision reads the bill, Command A phrases), OCI Language (translates). No database: rules are a policy file |
| 6 "at least $14 billion a year undelivered (Dollar For)"; "9.3% of Tennesseans uninsured in 2023" | $14B: do NOT say (cold assessment: built on Dollar For's own estimates). 9.3% is stale | "2,984 nonprofit community hospitals must run financial assistance programs (AHA)"; "9.7% of Tennesseans uninsured (Census ACS 2024)". See the numbers section |
| 7 "one hospital's policy, two languages" | Now two real Nashville systems' published policies; bills synthetic | "VUMC's and Ascension Saint Thomas's published policies, 32 language options, the packet. Next: hospital staff check our encoding, then more hospitals." |

## Judge answers (rev2 lines 412-421)

| Q | Problem | Instead |
|---|---|---|
| 3 "Each rule is a database row with ... who verified it" | No database, no verifier field | "Each rule is a record in the hospital's policy file with its source document, page and effective date, and the app shows that citation next to the result." Then rev2's pilot sentence |
| 4 "On our 10 synthetic test bills, it read [x] of 10" | 10 synthetic bills exist (9 now VUMC- or Ascension-named; bill-10 fictional), but the 10-bill accuracy run was never done; the re-rendered blur-3 bill gave a wrong date (row 0:14) | "On our synthetic test bills it reads the hospital, amount and dates; nothing is used until the person confirms each field, because the model can misread a blurry date. That is a few runs, not a benchmark." |
| 4 "every number ... is checked" | Half true: the check makes sure every number in the AI text is one the rules engine produced, not that each sits in the right place (audit 3 A1: a swapped income and guideline would pass). Words are not checked | "Every number in the AI text must be one our rules engine produced. The English version is one tap away, and the policy table and deadline are always shown in English." |
| 6 "Tennessee requires all hospitals to post their charity care policies and limits what uninsured patients can be charged" | Not verified: the statute (TCA 68-11-262) was never read, and the research found no Tennessee screening law | Cut the Tennessee sentence; keep "we'd encode HCA's policy from HCA's own documents" |
| 7 "hospitals pay per completed application" | Contradicts our sustainability brief, which advises against per-application and contingency pricing (conflict of interest) | "Never families. First a grant-funded pilot with a community partner; how hospitals would pay is not decided yet." |
| 7 "$7 billion a year ... bad debt" | Do NOT say, even attributed: the cold assessment found $7B is built from KFF's $2.7B plus Dollar For's own estimates | Cut it |
| 9 "The hospital prints a QR code" | Present tense is false (F9 fix 2) | "In a pilot, the hospital would print a QR code that opens our tool with that hospital selected." |
| (new) "Did VUMC / Ascension approve this?" | No | "No. We read their public policies with AI, checked them page by page with a second AI pass, and cite every page; no person at either hospital has reviewed it. A pilot would start with the hospital checking our encoding." |
| (new) "What about above the income limits?" | Both policies have a second route the app names but does not compute: VUMC catastrophic assistance, Ascension's means test | "Above the tiers we do not say no: the app names the hospital's other route and keeps the deadline on screen." |
| (missing) prior art B.A.R.S. | PRD F8 says to name it; rev2 has no answer | "Yes, B.A.R.S. at hackUMBC 2026 built a bill-photo-to-application tool for Maryland and placed second overall. They also cite pages and use a rules engine. Our difference: every number in the AI text must come from the rules engine, a person confirms every field the AI read, it offers 32 language options including Arabic and Hebrew right to left, and it names each hospital's other routes (catastrophic assistance, means test) instead of saying no. Both are prototypes." |

## Numbers on slides that nobody has re-opened (pre-mortem T7)

**2026-10-18 09:46 CDT (audit 4):** "VUMC 24%" is now verified on VUMC's own policy (p.23, AGB 24% = 76% discount); "175% of cost" may be said only as "Ascension's policy states it" (Ascension FAP p.5). The product is called BillScan ("[Name]" in rev2). "Save to Dad's bills" is the button "All bills from this visit". V1 grid: use "gives an eligibility estimate: 0/13".

29%, 52%, $14B, 2,984, 95,000 (already listed), plus $7 billion bad debt,
Tennessee 175% of cost, VUMC 24% of charges, 9.3% uninsured, 282,294
renewals. Open each source before it goes on a slide, or cut it.
**2026-10-17 23:52 CDT update - most of these were re-opened in
docs/research/2026-10-17_presentation-stats-brief.md (agent brief, not yet
cold-assessed).** In short: 95,000 -> 91,000 (CBPP 2026-03-19); 9.3% ->
9.7% (ACS 2024); 29% / 52% / $7B / $14B are all Dollar For (an interested
source with an unpublished survey method), so say "Dollar For found..." and
keep $14B off the market slide; "52% never told" -> "52% got no information
from their hospital"; 2,984 verified (AHA 2026); 175%, VUMC 24% and 282,294
still unverified there. VUMC's current policy (agent report
docs/research/raw/2026-10-17_mtn-vumc.md) gives AGB 24% and free care at or
below 300% FPG.
**2026-10-18 00:13 CDT update - cold assessment (docs/research/2026-10-18_cold-assessments.md, section 1):**
do NOT say $7B or $14B even with attribution ($7B is built from KFF's $2.7B
plus Dollar For imputations, so $2.7B is not independent support either);
"34% ... forms hard" must keep "in the past three years"; 91,000 could not be
re-fetched by the assessor (Cloudflare 403) - say "CBPP estimates"; "2,984
nonprofit hospitals" does not cover HCA TriStar (for-profit); do NOT say
"Arabic is Davidson's #2 language", 66.5% bankruptcies, "80% of bills have
errors", 175%, VUMC 24%, 282,294.
Verified 2026-10-17 by Claude against the Federal Register notice
(2026-00755, published 2026-01-15, effective 2026-01-13): the 2026 poverty
guidelines $15,960 for 1 person, $33,000 for 4, +$5,680 per person (the
engine's formula matches the table for every size 1-8).

## V1 result (Evan's runs, scored 2026-10-17 18:03 CDT; experiments.md)

Slide 3 grid: rows Gemini / Claude / ChatGPT; columns "mentions financial
assistance", "estimates eligibility", "gives the application window",
"invents the hospital's rules", "ready-to-send letter"; cells from the
experiments.md table. Bracket fills (draft wording):

- rev2 346 [result of task 1]: "all 13 answers told her to ask for financial
  assistance, but none estimated whether her dad qualifies, none gave the
  application window - 10 of the 13 pointed at the payment due date instead - and none
  handed her a finished application or letter."
- Judge Q1 [task 1 result]: same sentence; add "13 answers from three free
  assistants, English and Arabic, one synthetic bill."
- Pre-mortem E1 is half true: chatbots DO raise financial assistance, so do
  not claim they don't. The pitch line "Any chatbot can explain a bill.
  Nobody hands you the next step" holds.

## Judge Q&A card (2026-10-18 08:51 CDT; from docs/research/ briefs and their cold assessment)

Numbers here are from the cold assessment's SAFE / SAY-WITH-ATTRIBUTION list, except our own derivations: $0.04-$0.15 per journey (our estimate from Oracle list prices), "7 policies", "5 of 13", and the Oregon line (read from the OHA report).
- "How big is the problem?" - "About 20 million US adults owe over $250 in medical debt, at least $220 billion (KFF/Peterson, 2021 data). Dollar For's own patient survey found only 29% of patients with unaffordable hospital bills got financial assistance, and 52% got no information from their hospital."
- "Why language?" - "34% of adults with limited English say it made health care forms hard to fill out in the past three years (KFF 2024)."
- "Why these two hospitals?" - "In Middle Tennessee, 13 hospitals hold 76.7% of licensed acute beds, and they run on only 7 policies; VUMC and Ascension Saint Thomas run 5 of the 13; the app encodes 4, because Vanderbilt Clarksville has different terms (state bed report, July 2026). Their free-care limits differ: VUMC up to 300% of the poverty guideline, Ascension up to 250%."
- "Doesn't the hospital already screen people?" - "Some hospitals use vendor tools that estimate income from credit and census data; in Oregon, hospitals estimated those tools at about 85% accurate and complained they over-award help (OHA, Jan 2025). We use the family's own numbers and the hospital's own rules, and show every page."
- "HCA / TriStar?" - "HCA is for-profit, so the nonprofit 501(r) rules do not bind it, and we found no HCA policy PDF to cite, only a web page. We only encode what we can cite."
- "Who pays?" - "Never families. A grant-funded pilot first; the cloud cost is cents per family (about $0.04-$0.15 per non-English journey, Oracle list prices). Hospital pricing is undecided; no contingency fees."
- "What if the family has insurance?" (added 2026-10-18 10:08 CDT, Evan) - "For insured families it estimates help on what you owe after insurance: the amount due on the statement." Then: Ascension's help covers the part "for which the Patient is responsible following payment by an insurer" (Ascension FAP p.2). VUMC's help is for "uninsured or underinsured" patients (VUMC FAP p.6), and "underinsured" means insured patients whose services are "noncovered" or have "limited benefit coverage" (p.4, definition Y), so an ordinary deductible or copay on covered care may not qualify at VUMC; the app lists this as a VUMC condition. Do NOT say an insured VUMC patient gets free care.
- "Is this legal or medical advice?" - "No. It explains a published policy and drafts the paperwork; the hospital decides, and we never diagnose."
