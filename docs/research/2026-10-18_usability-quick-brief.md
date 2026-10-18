# Usability: what improves it, applied to Billow (very quick brief)

**Date:** 2026-10-18 (written ~11:53-11:55 CDT). **Question:** which proven usability practices matter most for Billow,
a phone-first web app that walks a family through a hospital bill, and which can still be done before the 13:05 CDT
showcase? **For:** Evan and the team, deciding what (if anything) to change in the last hour.

## TL;DR
The working hypothesis held: the gains come from a small set of well-established practices (Nielsen's 10 heuristics,
WCAG 2.2 AA target size, GOV.UK "one thing per page", inline validation done gently, plain language). Checked against
Billow's code, Billow already does most of them: named loading steps, a confirm-before-use step, a reason shown when
Continue is disabled, 48 px buttons, a help card. The rival hypothesis (that a big redesign is needed) has no support. The
one structural gap is the Bill screen asking many things on one page (6 fields + charge lines), against GOV.UK's
one-thing-per-page advice; that is not a minutes-scale fix. In the time left: deploy the two finished UI changes
(Remove photo, closed Sources dropdown; commit a0684aa, not live) and do not start anything structural.

## Method
Hypotheses (before collecting): H1 a few established heuristics cover most usability gains; H2 (rival) Billow needs new
flows. Sources: the four primary references below (NN/g, W3C, GOV.UK, Baymard), one secondary sweep on health-literacy
reading level; Billow's own code (style.css, app.js) for the "Billow today" column. Limits: no user testing was possible
(that needs real families on phones - a human method, not desk research); no readability score was computed.
Phase effects (2026-10-18):
  8.5 verify   - 3 load-bearing citations re-fetched by WebFetch (a summarizing tool): all CLOSE-PARAPHRASE at best;
                 no verdict flipped; Baymard's "22% faster" figure downgraded to unverified (secondary only).
  10.5 assess  - SKIPPED (Evan asked for "very quick"); this brief has had no cold read.

## Findings, mapped to Billow
| Practice (source) | What it says | Billow today (checked in code unless noted) | Doable before 13:05? |
|---|---|---|---|
| Visibility of system status (NN/g heuristic 1) | Keep users informed through timely feedback | Yes: named spinner steps ("Reading the bill..."), step bar | - |
| User control and freedom (NN/g 3) | Easy undo and exits | Back on every screen; Remove photo built in a0684aa, NOT live | Yes: deploy a0684aa |
| Error prevention (NN/g 5) | Prevent problems before they happen | Yes: nothing is used until each field is confirmed; Continue disabled with the reason shown | - |
| Recognition rather than recall (NN/g 6) | Show options rather than make people remember | Partly: citations now sit in a closed "Sources" dropdown (a0684aa); each footnote mark opens it | Already built |
| Aesthetic and minimalist design (NN/g 8) | Show only what is needed | Result screen is long (hero, tiers, conditions, deadline, documents, contacts, card, sources); the dropdown trims one block | No (structural) |
| Recover from errors (NN/g 9) | Plain error text with a way out | Yes: every failure path has a message and a help card; photo read failure falls back to typing | - |
| Target size (WCAG 2.2 SC 2.5.8, AA) | Pointer targets at least 24 x 24 CSS px | Buttons min-height 3rem = 48 px (style.css:229, :236); footnote marks use a padding hack (style.css:410), not measured | Measure only |
| One thing per page (GOV.UK Design System) | Start with one question per page; helps focus, mobile, low-confidence users | Questions screen: a few questions together; Bill screen: 6 fields + lines on one page | No (structural) |
| Inline validation (Baymard) | Validate inline, but not before the user finishes; clear the error once fixed | Income hint exists (app.js q-income-hint); premature-validation behaviour not checked | Not checked |
| Plain language (secondary: 6th-8th grade for patient materials) | Write at a 6th-grade level or lower | Not measured; policy text is shown in the hospital's own English on purpose | Not measured |

## Ranked for the last hour
1. Deploy a0684aa (Remove photo + closed Sources) - minutes, already tested (76 JS tests); needs Evan's word.
2. Leave the Bill-screen layout as is; mention "one thing per page" as a next step if asked.
3. If time: run a readability score over the 10 most-seen English strings - minutes, no code change.

## Verification (stage 8.5)
| Load-bearing claim | Source | Verdict |
|---|---|---|
| The 10 heuristic names, incl. visibility of status and error prevention | nngroup.com/articles/ten-usability-heuristics | CLOSE-PARAPHRASE (WebFetch) |
| 2.5.8 is Level AA, minimum 24 x 24 CSS px | w3.org/WAI/WCAG22/Understanding/target-size-minimum | CLOSE-PARAPHRASE (WebFetch) |
| GOV.UK: start by asking one question per page, and why | design-system.service.gov.uk/patterns/question-pages | CLOSE-PARAPHRASE (WebFetch) |
| Baymard: avoid premature inline validation | baymard.com/blog/inline-form-validation (search summary only) | UNVERIFIED (not re-fetched) |

## Numbers register
| Number | Claim | Source | Interest class | Verdict |
|---|---|---|---|---|
| 24 x 24 CSS px | WCAG 2.2 AA minimum target | W3C | INDEPENDENT | CLOSE-PARAPHRASE |
| 44 x 44 CSS px | WCAG AAA enhanced target | secondary (DAISY KB summary) | INDEPENDENT | UNVERIFIED |
| 31% | sites with no inline validation (Baymard 2024) | Baymard via search summary | VENDOR-SELF-REPORTED (research firm selling access) | UNVERIFIED |
| 22% | faster completion with inline validation | Reform blog, attributed to Baymard | UNVERIFIABLE | UNVERIFIED - do not cite |
| 6th grade | target reading level for patient materials | secondary summaries of AMA/NIH | UNVERIFIABLE here | UNVERIFIED |
| 48 px | Billow button height | style.css:229, :236 | INDEPENDENT (our code) | VERIFIED (read on disk) |

## Thin / missing
- No usability test of Billow with real families on phones exists; that is the evidence that would settle priorities.
- No readability measurement of Billow's strings.
- No primary AHRQ/CDC page read for the reading-level number (searched "health literacy plain language ... AHRQ CDC": only
  secondary summaries came back).

## What would change this conclusion
A 5-person phone test showing people stuck on the Bill screen (would raise "one thing per page" to priority 1), or a
readability score far above grade 8 (would raise plain-language rewrites).

## Sources (all accessed 2026-10-18)
- Nielsen Norman Group, "10 Usability Heuristics for User Interface Design": https://www.nngroup.com/articles/ten-usability-heuristics/
- W3C, Understanding SC 2.5.8 Target Size (Minimum): https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html
- GOV.UK Design System, Question pages: https://design-system.service.gov.uk/patterns/question-pages
- GOV.UK Service Manual, Structuring forms: https://www.gov.uk/service-manual/design/form-structure
- Baymard Institute, inline form validation: https://baymard.com/blog/inline-form-validation
- Health-literacy reading level (secondary): https://www.aafp.org/pubs/afp/issues/2005/0801/p463.html
