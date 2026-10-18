# Pitch corrections - what rev2 says vs what the build does (DRAFT for Evan)

> **2026-10-17 20:52 CDT - PARTLY SUPERSEDED (audit 2 #3). Do not use the rows
> below that say QR, the five-bill Home or the dashboard are "not built", or that
> 2 bills / 11 languages exist.** Since record AH (19:41) these are LIVE: the
> Home screen with all 5 bills and "Up to $8,837.65 could be reduced", reminders
> + calendar file, the ?hospital= chip and a QR on synthetic bill-02 (it encodes
> the app address with ?hospital=; a real-phone scan is NOT yet checked), and
> /dashboard.html. 10 synthetic bills
> exist. Live has 11 languages; 32 codes are built on f10, not deployed. Keep the
> 1:24 and 1:42 beats, but say "synthetic" and "the hospital decides". The other
> rows (VUMC, brackets, prior art) still stand.


Written 2026-10-17 by Claude from the full audit (docs/2026-10-17_full-audit.md,
finding A1). The pitch, demo script and judge answers live in
docs/2026-10-17_HackTN26_Health_Access_Plan_rev2.txt, which is kept as written.
Present from rev2 WITH this sheet applied. Each row: the rev2 line, why it is
wrong, and a replacement that is true today. Replacement wording is a draft:
Evan or a teammate should say it in their own words.

## Pitch (rev2 lines 343-348)

| rev2 | Problem | Say instead |
|---|---|---|
| 345 "The hospital prints a code on its statement. She scans it and photographs the bill." | No QR code exists; no hospital prints one (PRD F9 fix 2) | "She opens [Name] on her phone and photographs the bill." |
| 345 "checks her answers against the hospital's own published policy, page cited" | The demo hospital is fictional (Cumberland General, SYNTHETIC); we wrote its policy page | "checks her answers against the hospital's financial assistance policy, page cited. Today that is a fictional hospital whose policy has the same structure as Nashville's; encoding a real hospital's policy is the next step, with that hospital's sign-off." |
| 346 brackets [result of task 1], [N], [x], [y] | No V1/V2/V3 result exists yet | Fill each from a measured result or cut the sentence (rev2's own rule, line 342) |
| 348 "nothing a family enters is stored" | TRUE. Keep it. Do NOT use F9 fix 1 ("bills stay on their own phone"): there is no save feature | Keep rev2's sentence |

## Demo script (rev2 lines 350-398)

| rev2 | Problem | Say / do instead |
|---|---|---|
| 0:00 "Scan the QR code"; "VUMC already selected"; "The hospital prints this code" | No QR; the hospital is the synthetic Cumberland General | Open http://207.211.181.174/ on the phone. "This is running live on Oracle Cloud. Demo uses synthetic bills only." |
| 0:14 "It left the blurry date blank instead of guessing." | True only for the blurred bill-02 (blur 3 and 5 left the date null, n=1 each; experiments.md) | Say it only if you photograph bill-02-blur3 or blur5 and the date is blank in rehearsal; otherwise "Nothing is used until she confirms it." |
| 0:56 "VUMC's policy opens at the cited page" | The citation opens our synthetic policy page | "Here's the cited page of the hospital's policy." (it opens /policy-cumberland.html) |
| 1:06 packet | TRUE; it is a printable page, printed or saved as PDF from the browser | Tap "Create my application packet", then Print |
| 1:24 "Save to Dad's bills", five bills, "Up to $X", reminders | Not built (PRD F9, never started) | Cut the beat. End the demo on the packet (about 1:10) |
| 1:42 partner dashboard | Not built; F9 says a labeled mockup on a slide only | Cut from the demo; if shown, on a slide labeled "mockup" |

## Slides (rev2 lines 402-408)

| Slide | Problem | Instead |
|---|---|---|
| 1 "in Arabic or Spanish" | The app explains in 11 languages | "in 11 languages" (interface translated in English, Spanish, Arabic, Simplified and Traditional Chinese) |
| 5 "Starts from a QR code"; "four Oracle services" | No QR. MySQL HeatWave was never used and is deleted | "Starts from a photo of the bill." Oracle Cloud: one compute VM, Generative AI (Cohere Command A Vision reads the bill, Command A phrases), OCI Language (translates). No database: rules are a policy file |
| 7 "one hospital's policy, two languages" | 11 languages; the one policy is synthetic | "one synthetic hospital's policy, 11 languages, the packet" |

## Judge answers (rev2 lines 412-421)

| Q | Problem | Instead |
|---|---|---|
| 3 "Each rule is a database row with ... who verified it" | No database, no verifier field | "Each rule is a record in the hospital's policy file with its source document, page and effective date, and the app shows that citation next to the result." Then rev2's pilot sentence |
| 4 "On our 10 synthetic test bills, it read [x] of 10" | 2 synthetic bills exist | "On our synthetic test bill it read all 6 fields; on the blurred versions it left the unreadable date blank instead of guessing. That is one run each, not a benchmark." |
| 4 "every number ... is checked" | TRUE for numbers. Words are not checked | Add: "Numbers are checked; the wording is AI-written, so the English stays on screen as the version that counts." |
| 7 "$7 billion a year ... bad debt" | Source not opened (pre-mortem T7) | Cut unless someone opens the Dollar For source first |
| 9 "The hospital prints a QR code" | Present tense is false (F9 fix 2) | "In a pilot, the hospital would print a QR code that opens our tool with that hospital selected." |
| (missing) prior art B.A.R.S. | PRD F8 says to name it; rev2 has no answer | "Yes, B.A.R.S. at hackUMBC 2026 built a bill-photo-to-application tool for Maryland and placed second overall. Our focus: a rules engine decides and every rule is cited, every number in AI text is checked, and it explains in 11 languages including Arabic right to left. Both are prototypes." |

## Numbers on slides that nobody has re-opened (pre-mortem T7)

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
  application window - they all pointed at the payment due date - and none
  handed her a finished application or letter."
- Judge Q1 [task 1 result]: same sentence; add "13 answers from three free
  assistants, English and Arabic, one synthetic bill."
- Pre-mortem E1 is half true: chatbots DO raise financial assistance, so do
  not claim they don't. The pitch line "Any chatbot can explain a bill.
  Nobody hands you the next step" holds.
