# Research brief - Design system and frontend architecture for Bill to Help

**Date:** 2026-10-17 (research 14:31-15:30 CDT; revised 15:11 CDT onward
for two changed facts and the stage-10.5 cold assessment, see section 14)

**Question:** Which design system and frontend architecture should Bill to
Help use? It has to:
- look trustworthy and distinctive, without the marks of "AI slop";
- work on a phone in the tier-1 interface languages (English, Spanish,
  Arabic (RTL), Simplified Chinese zh-CN, Traditional Chinese zh-TW) and
  show tier-2 explanation text (Vietnamese, French, Korean, Russian,
  German, Hindi in Devanagari) inside the English interface;
- be buildable by AI coding agents before the feature freeze at about
  23:00 CDT tonight, Sat 2026-10-17 (the eve of Sun 2026-10-18; hacking
  ends Sun 2026-10-18 1:00 PM CDT). Source for the freeze: `HANDOFF.md`
  and `docs/2026-10-17_pre-mortem.md` ("the Sat 23:00 freeze").

**For:** Evan and the team, deciding three things:
- (a) which visual direction to build;
- (b) which premade component source to vendor;
- (c) whether to change the frontend architecture.

The judges are Oracle executives, Vanderbilt faculty, an HCA Healthcare
application-services director and an internal-medicine physician.

**Companion file:** `docs/research/2026-10-17_design-directions.html`. It
shows three directions, each with the Result screen in English and Arabic,
plus a Simplified Chinese (zh-CN) Result screen for the recommended
direction only. All are labelled SYNTHETIC DEMO, and the page makes no
network requests (checked in a browser, section 14).

## TL;DR

**Recommendation: build Direction 1, "Paper Trail".**
- Keep `app.js` as vanilla JS.
- Vendor Web Awesome's native element styles (MIT, built on logical
  properties) and re-theme them with our own tokens.
- Use one type family: IBM Plex Sans, Plex Sans Arabic and Plex Sans
  Devanagari. It is chosen for coverage from one design programme, not for
  distinctiveness (see the source caveat below); the distinctiveness has to
  come from the policy-table layout. Noto Sans + Noto Sans Arabic is the
  equal-cost swap if Evan wants a font with no AI-prompt association.
- Chinese (now tier 1) and Korean use the phone's own CJK font through
  per-language stacks, with no CJK webfont: a webfont would add 342-445 KB
  per weight for the zh interface strings alone, against 0 B (section 5.4).

The signature of Paper Trail is the product's own mechanism made visible: the
hospital's policy table, with the family's row highlighted and every claim
footnoted to a policy page. That shows "a rules engine decided, not the AI"
without a word of explanation. It is the credibility point the physician and
faculty judges will probe.

**Three findings changed the plan:**

1. **The obvious premade bases fail on Arabic.**
   - USWDS, GOV.UK Frontend and NHS.UK frontend have essentially no RTL
     support.
   - GOV.UK's shipped CSS has 0 logical properties against 346 physical ones.
   - USWDS's RTL issue has been open since 2023. Its maintainer wrote on
     2026-09-18 that "The next step is a working right-to-left example".
2. **The usual escapes from the AI look are now tells themselves.**
   - Pico (archived; last push 2026-10-04, final release v2.1.1 on
     2025-03-15) and Shoelace (sunset) are dead.
   - Anthropic's frontend-design guidance (updated 2026-09-02) says
     AI-generated design "clusters around" cream + serif + terracotta,
     broadsheet hairlines and template chrome such as ALL-CAPS eyebrows.
     ("Anti-purple" is this brief's label, not the source's.)
3. **Copying the government look does not transfer.**
   - The only trust evidence for it, GDS testing in 2024, shows people trust
     it *because they recognise it as government*.
   - GOV.UK's typeface is for service.gov.uk only.

**Source caveat (moved up from section 9 after the cold assessment):** 7 of
the 12 AI tells in section 5.1, and 3 of its 5 "Strong" ratings, rest on
two Anthropic documents ([A1], [A2]). This brief was written by an
Anthropic model, and [A1] is a skill installed in its own toolset, so the
tell list is one interested organisation's view. The same source cuts
against this brief's font choice: [A2]'s typography prompt lists "IBM Plex
family" among the "Impact choices" it steers the model toward, so Plex is
a likely AI default, not a distinctive pick (section 5.4).

**Lead flaw:** the redesign now competes with the feature freeze, not the
gate. The 5:00 PM gate passed at 14:53 CDT and the app is live with real OCI
at http://207.211.181.174/ (`.claude/project-memory/experiments.md`). That
leaves about 7.8 wall-clock hours (15:11 to 23:00 CDT), shared with three
other launch-blocking pre-mortem items (submission rules, validation, the
phone-photo test); a fourth, T5, is the redesign's own deploy safety. The recommended direction is estimated
at about 6.0 agent-hours (a judgment, not a measurement; section 6). Three
rules make it safe:
- one agent owns `style.css`, the vendored files and a fixed list of
  `app.js` markup changes; no API call changes (pre-mortem T5);
- the tier-table data is a separate decision for Evan (section 7), because
  the clean version touches `app/engine.py`, which T5's wording rules out;
- go/no-go at 21:00 CDT: if the done-check is not passing, ship only the
  1.5-hour subset in section 11 and roll back the rest.

## 1. Problem (stage 1)

The current UI works but is anonymous: `app/static/style.css` is 34 lines,
with system fonts, one blue and bordered cards. Judges score "User
Experience: Is the workflow intuitive? Can a new user understand it
quickly?" from a 2-minute live demo on a projector and a phone. Evan wants it
eye-catching, with no tells of AI generation.

The hard constraints:
- Right-to-left Arabic is a first-class demo path (the demo taps Arabic at
  0:08).
- Script systems: Latin (incl. Vietnamese) and Cyrillic, Arabic, Chinese
  in both Simplified and Traditional forms as full interface text (tier
  1), Korean Hangul and Devanagari as explanation text (tier 2).
- No build step.
- Vendored assets only, for privacy.
- Originally about 20 hours left with the core gates open; as of 15:11 CDT
  the gates have passed and about 7.8 hours remain to the freeze.

Angles considered:
- **Optimistic:** a strong identity lifts the UX and Communication scores.
- **Pessimistic:** design time steals from the validation tasks and the
  phone-photo test, and a late restyle can break the working live demo
  (pre-mortem T5). Those carry Problem Validation and the
  working-prototype criterion. (Originally: "steals from the OCI gate";
  that gate passed at 14:53 CDT.)
- **Alternate:** keep the current look and fix only RTL, type and the Result
  hierarchy.

All three are priced: see section 6 (build cost) and section 11.

## 2. Survey of existing work (stage 2)

**Repo:**
- `.claude/project-memory/ui.md` asks for an asset inventory with a license
  per asset (fonts included) and a dated accessibility audit.
- `.claude/project-memory/languages.md` holds the language tiers.
- There is no prior design brief.
- `docs/research/2026-10-17_bill-decoder-crowding.md` covers competitors,
  not design.

**Current UI**, read end to end (`index.html`, `style.css`, and `app.js`: 375
lines when read; 371 at commit 145c8af, 15:05 CDT, because it is being
edited in parallel; renders by function through an `el()` helper). Five
observations:

1. **Language picker.** It already uses endonyms (language names in their
   own language) and no flags. That matches the guidance in section 5.5, so
   keep it.
2. **Bidi bug (observed, not fixed; `app/` is out of scope).**
   - `cite()` builds "Source: ... page N" from translated words (`t("src")`,
     `t("page")`).
   - It then wraps the whole string in an element forced to `lang="en"
     dir="ltr"`.
   - In Arabic, the translated words for "Source", "page" and "effective"
     (`t("src")`, `t("page")`, `t("effective")`; three words, not two as
     first written) therefore end up inside an LTR English run.
   - Fix: put the translated label outside the element, and the English
     citation inside `<bdi lang="en">`. The mock does this.
3. **CSS direction.** `style.css` uses no physical left/right properties, so
   little breaks in RTL today. It also uses no logical properties, so a
   redesign must add them on purpose.
4. **Result screen hierarchy.** These items all get equal visual weight as
   same-styled cards: the poverty-line sentence, tier, deadline,
   explanation, documents, contact and TN card (the TN card was hidden at
   15:05 CDT, commit 145c8af, pre-mortem T4). That is the "identical
   cards" pattern (section 5.1, tell 3). It hides the one answer the family
   came for.
5. **Status message.** One `#msg` element doubles as both info and error
   style. A redesign should give "Reading the bill..." its own calm status
   style, separate from errors.

## 3. Hypotheses, written before deep collection (stage 3)

- **H1 (direction):** a document/civic-plain direction built from the
  product's own artifacts (policy table, citations) beats a warm
  consumer-health direction for these judges and users.
  - Rival H1b: a warm consumer-brand look (One Medical / Oscar style) serves
    stressed families better.
  - Null H1-0: the visual direction barely matters next to a working demo.
- **H2 (slop tells):** primary designer or critic sources exist for concrete
  AI-UI tells, not just listicles.
  - Rival: it is mostly opinion.
- **H3 (library):** a government design system (USWDS or GOV.UK Frontend) is
  the best premade base.
  - Rival H3b: those lack RTL, so a web-component or native-element kit is
    better for an Arabic-first demo.
- **H4 (fonts):** the Noto family is the best multiscript choice.
  - Rival H4b: IBM Plex gives a matched and more distinctive family.
- **H5 (architecture):** stay with vanilla JS.
  - Rival H5b: adopt Lit, Alpine or htmx, vendored.

**Outcome:**

| Hypothesis | Result |
|---|---|
| H2 | Survived, with a caveat on how concentrated the sources are |
| H3 | Died; H3b survived |
| H4 | Split: Noto is the safest, Plex the best matched; the rival won the recommendation. Revised after the cold assessment: the "more distinctive" half of H4b DIED ([A2] lists "IBM Plex family" as a font it steers the model toward), and "matched" is weaker than first stated (only the bundled Latin metrics were measured). Plex stays for coverage |
| H5 | Survived |
| H1 | Untested by evidence; it is a judgment (section 10). The cold assessment found a counter-signal never sought: the GDS post cited in 5.2 also says testers "much preferred online forms to PDFs and other document-based versions". That is about format (PDF vs web form), not visual style, but it is the nearest evidence against a "document" look |

## 4. Research design, audience, method (stages 4-7)

**Sources: primary where possible.**
- Design-system docs: GOV.UK, USWDS, NHS, Canada.ca, Material, Wikimedia
  Codex.
- W3C i18n articles and the clreq font mappings.
- Anthropic's published design guidance, and NN/g.
- Shipped files: package.json and LICENSE files, and the actual dist CSS/JS
  on jsdelivr.
- google/fonts METADATA and font binaries (cmap and OS/2 tables, read in
  memory).
- GitHub issues and the repo API via `gh`.

**Analysis:**
- **Libraries:** one comparison table with measured CSS bytes and a count of
  logical vs physical properties per library.
- **Fonts:** a glyph-coverage table. (Not delivered as a table; coverage
  is stated in prose in 5.4, from cmap reads and Fontsource subsets, which
  share one upstream: Fontsource's Google-font packages are built from
  google/fonts.)
- **Contrast:** a WCAG ratio computed for every token pair. The script uses
  the standard WCAG 2.x relative-luminance formula. Sanity check: #777 on
  white computes to 4.48:1, the known value.

**Collection:**
- Three parallel collector agents:
  - A: AI slop and exemplars;
  - B: component libraries and architecture;
  - C: fonts and screen patterns.
- Each tagged every claim RAW (read the page's own text or bytes) or FETCH
  (a summarizer's paraphrase).
- I then re-read every load-bearing claim through a different call (curl and
  grep, `gh`, or the browser's page text). Section 8 has the results. One
  exception: the Plex x-height measurement was never re-run.

**Audience:** Evan, plus whoever builds the frontend tonight. Ranking
criteria, in order:
1. accessibility and RTL correctness;
2. credibility with the named judges;
3. distinctiveness;
4. build hours.

**Limitations:**
- **No user testing.**
  - Whether families or judges trust Direction 1 more than 2 or 3 is
    untested.
  - The method a human would use is already in the plan: the 5-minute task
    comparison (rev 2, Validation task 3), run once as an A/B of two
    directions with 4-6 attendees.
- No screen-reader pass, and no test on a real iPhone or Android.
- The Arabic copy in the mock was written by me and needs a fluent
  reviewer.

**Phase effects (2026-10-17):**
- **8.5 verify:**
  - **Caught one design error.** I first mirrored the sliding-scale chart in
    RTL. Material's verbatim text says "Charts and graphs" are not mirrored.
    The Arabic mock now keeps that chart left-to-right while the step bar
    mirrors.
  - **Downgraded 2 claims.**
    - The Tailwind indigo-500 origin story for AI purple is secondhand only.
    - The Plex x-height match is a single, un-rerun measurement.
  - **Added 2 limitations.**
    - clreq labels PingFang "Downloadable", so check system CJK on the demo
      phone.
    - Web Awesome's accessibility record is a commitment statement, not a
      conformance report.
- **10.5 assess:** flipped a verdict (H4b "distinctive" died); downgraded
  4 claims (Plex "matched metrics", Web Awesome "Ready", [S1] as
  AI-specific corroboration, "avoids every tell"); caught 5 factual errors
  that I confirmed by re-fetch (Pico archive date, Lit single-file builds,
  Plex designer credit, Web Awesome file count, the CJK `:lang()` tags);
  added 6 limitations. Details in section 13.

## 5. Findings

### 5.1 What marks a UI as AI-generated (H2 survived)

Four primary sources:
- [A1] Anthropic's frontend-design skill (SKILL.md, last commit 2026-09-02);
- [A2] Anthropic's cookbook "Prompting for frontend aesthetics";
- [N1] NN/g on the sparkles icon;
- [S1] shadcn's own changelog.

Most other "tell" lists are practitioner blogs or vendors: Impeccable,
Superdesign, pixelslop, prg.sh, DEV posts. The table rates each tell's
strength.

| # | Tell | Best source (provenance) | Replace with | Strength |
|---|---|---|---|---|
| 1 | Purple/indigo-to-blue gradients on white | [A2] "Cliched color schemes (particularly purple gradients on white backgrounds)" (VERIFIED-VERBATIM; the source spells it with an e-acute, transliterated here) | A palette derived from the subject: 4-6 named hex values, one dominant plus one sharp accent [A1][A2] | Strong as a tell. The "Tailwind indigo-500" origin story is secondhand (prg.sh, DEV posts) |
| 2 | Inter / Roboto / Arial / plain system fonts everywhere | [A2] "Overused font families (Inter, Roboto, Arial, system fonts)" (VERIFIED-VERBATIM). It also warns that Space Grotesk becomes the next default | A typeface chosen for a stated reason. Here: a matched multiscript family (IBM Plex, section 5.4) | Strong for Inter/Roboto. No source names Geist |
| 3 | Identical rounded cards: one radius on everything, the same soft grey shadow (rgba(0,0,0,.1)), gradient washes | [A1] "the SaaS-card kit" (VERIFIED-VERBATIM; the local plugin copy was read in full) | Radius and elevation that follow hierarchy. Rules, tables and space for structure; cards only for truly separate objects | Medium-strong |
| 4 | Template chrome: a tracked ALL-CAPS eyebrow above every heading, "A . B . C" meta strings, "WORD - fragment" labels, tinted near-black (#0B0B0B, #111) standing in for black, monospace for small data labels, an arrow appended to every button | [A1] (VERIFIED-VERBATIM; the near-black item was omitted from the first draft) | Plain sentence-case headings; labels only where they carry information | Medium-strong |
| 5 | The clusters [A1] says AI-generated design "clusters around": cream (#F4F1EA) + high-contrast serif + terracotta (#D97757); near-black + acid green; broadsheet hairlines with zero radius ("anti-purple overcorrection" is this brief's label) | [A1], VERIFIED-VERBATIM. Scope correction: "on a user's brief it reads as a tell" refers only to the #D97757 accent; for the clusters as a whole [A1] says they are "defaults rather than choices" | Don't spend design freedom on these defaults; derive from the subject's own vernacular | Strong as the model vendor's own list (an interested source, see TL;DR) |
| 6 | Sparkle / magic-wand icons for "AI" | [N1] the icon "suffers from ambiguity and lacks a standardized meaning" (VERIFIED-VERBATIM; 2024-09-20, modified 2025-09-19) | A text label such as "Read by AI, checked by you" | Strong |
| 7 | Big number + small label + gradient accent hero | [A1] "the default treatment" (VERIFIED-VERBATIM) | Open with the subject's most characteristic artifact: here, the policy-table row | Medium-strong |
| 8 | Centered hero + three icon feature cards | prg.sh 2025-10-26 and Superdesign 2026-07-13 (both RAW, but a blog and a vendor) | Sections sized by the job they do | Medium |
| 9 | Gradient text, glassmorphism, bento grids | Creative Boom 2026-04-21 (RAW); Impeccable (RAW, a tool author) | Emphasis by weight and size; blur only for real layering | Medium (bento is contested) |
| 10 | Emoji used as icons | Impeccable and Superdesign (RAW); the rest are listicles | One drawn SVG icon family with one stroke weight | Medium-weak |
| 11 | The shadcn/ui default look | [S1] "all apps started looking the same." (VERIFIED-VERBATIM, Dec 2025). Correction: the post is a product launch (it introduces shadcn create) and does not mention AI; it is about default sameness, and the link to AI output is this brief's inference | Our own tokens, set before any components | Medium (downgraded from Strong). Lucide as a tell is weak (a competitor's blog only) |
| 12 | A fade-and-slide-up entrance on every section | [A1] (VERIFIED-VERBATIM) | One motion that answers a user action (field confirmed, result revealed) | Medium |
| 13 | Accenting a single word or phrase in a headline (italic, bold or a different colour); all-caps labels | [A1] "Avoid these default typographic treatments" (VERIFIED-VERBATIM; omitted from the first draft) | Emphasis only where it carries meaning | Medium-strong. Direction 3's marigold underline on numbers in its headline is this tell; D1's SYNTHETIC DEMO badge is all caps, kept because it is a safety label |

**Calibration** (Creative Boom, RAW): the complaint is lack of intent, not
the technique. A plain, deliberate choice is not slop just because it
resembles one of these.

**A tension, stated openly:**
- [A2] calls system fonts a tell.
- Government systems, and Canada.ca with its Noto Sans body, choose plain
  faces on purpose, for legibility and coverage.
- For a four-script, low-literacy app, script coverage outranks novelty.
- So the recommendation picks a matched family (Plex), not an exotic display
  face.

### 5.2 Exemplars: what makes civic and health UI work

**GOV.UK Design System**
- **Colours (RAW):** text #0b0c0c, brand #1d70b8, focus #ffdd00, error
  #ca3535, success #0f7a52.
- **Type scale (RAW):** 80/48/36/27/24/19/16 px on large screens, line
  heights on a 5px grid.
- **Patterns (RAW):**
  - Question pages: "Start by asking one question per page".
  - Check answers: says it helps "reduce error rates as users are given a
    second chance to notice and correct errors".
  - Confirmation pages must offer a way to "save a record of the
    transaction, for example, as a PDF". This supports our printable packet.
- **Typeface (VERIFIED-VERBATIM):** "you must use the GDS Transport font" if
  the service is on service.gov.uk. Other domains "use an alternative
  typeface".
- **Accessibility claim (RAW, collector B):** the accessibility statement
  says the codebase "is fully compliant with WCAG 2.2 AA", based on a DAC
  audit in July 2024.

**USWDS**
- **Font:** Public Sans (OFL).
- **Colour grades (RAW):** a grade difference, the "magic number", of 50 or
  more meets AA and 70 or more meets AAA. Lightness is matched across hues,
  so contrast can be checked by arithmetic.
- **Neutrals:** ink #1b1b1b; ramp #565c65 / #71767a.
- **File input (RAW):** "Use hint text to highlight input restrictions". It
  also warns about large files on limited data plans.
- **Accessibility (FETCH):** an ACR/VPAT covers 3.11.0 and explicitly does
  not claim full conformance.

**NHS.UK**
- **Colours:** blue #005eb8, text #212b32.
- **Care cards (RAW):** three urgency levels, used sparingly so they
  "reassure people, not to scare them".
- **Font:** Frutiger, licensed to NHS organisations only. The compiled CSS
  even hotlinks it from assets.nhs.uk at runtime (RAW).

**Canada.ca**
- **Type (RAW):** Lato headings; Noto Sans body at 20px. This is precedent
  for Noto as a deliberate public-service body face.
- **Colours (RAW):** text #333, link #284162, accent #26374A.

**Code for America, GetCalFresh**
- **Principles (FETCH only):** "people-first language" and "mobile-first
  designs with one question per page".
- **Numbers:** participation figures exist, but they are not attributed to
  the design.

**Civilla, Project Re:form (Michigan DHS-1171)**
- **Results (Core77 RAW, GovTech RAW):**
  - the form became 80% shorter;
  - in the pilot, 90% felt confident completing it alone;
  - completion rose to 94%, from 72% before.
- **Caveats:**
  - These are pilot numbers reported by the agency and the designers, not a
    controlled trial.
  - The two sources disagree on the old form's word count (18,000 vs about
    8,000).

**Consumer health**
- Oscar uses Klim's Heldane Display and Text (RAW, foundry credit).
- Cityblock uses navy #1E1F42, blue #0064FA and a lime #E7FA85 (RAW, read
  from homepage CSS, not a published palette).
- One Medical: a deep green with watercolour illustration (FETCH).
- All of them use licensed brand fonts we cannot ship.

**Trust evidence**
- GDS testing (2024-01-12), VERIFIED-VERBATIM:
  - participants "recognised the visual style as being a government site
    and something that they could trust";
  - "Forms using the GOV.UK Design System all look the same, increasing
    their sense of trust and familiarity."
- Sample size is not stated, and the finding is qualitative.
- The same post also says testers "much preferred online forms to PDFs and
  other document-based versions" (curl, VERIFIED-VERBATIM, found by the cold
  assessment). That is about format, not look, but it warns that a
  "document" direction must still behave as a web form, not a PDF.
- That trust comes from *recognising the site as government*. **It does not
  support a non-government product imitating the look.**
- What does transfer are the patterns:
  - one question per page;
  - check answers;
  - plain language;
  - a saved record.

### 5.3 Premade component sources (H3 died; H3b survived)

Measured by me and collector B (RAW): curl of the shipped dist files on
jsdelivr, gzip -9, then grep counts. Two terms in the table:
- **logical:** occurrences of inline-start / inline-end / inset-inline /
  padding-inline / margin-inline;
- **physical:** occurrences of margin-left/right, padding-left/right,
  left:/right:.

These counts are a heuristic. A symmetric `left:0;right:0` counts as
physical but does not break RTL.

| Library (version, 2026-10-17) | License | Size raw / gzip (B) | Logical / physical / dir-rtl rules | RTL verdict | Status and look |
|---|---|---|---|---|---|
| **Web Awesome 3.14.0** (`@awesome.me/webawesome`) | MIT (package.json + LICENSE, RAW) | native.css 37,009 / 6,761; themes/default.css 16,772 / 2,597 | 22 / 1 / - (native.css); component chunks 166 logical / 5 physical (collector B) | **Likely ready, not proven (downgraded from "Ready").** The vendor docs cover the web *components*, which this plan does not load: (browser text, VERIFIED-VERBATIM) components "can be localized by importing the appropriate translation file and setting the desired lang and/or dir attributes on the <html> element". Translation files exist for ar, zh-cn, zh-tw, hi, ru, de, fr, es; none for vi or ko. For `native.css` the only evidence is the logical/physical count (22/1 mine, 23/0 collector B), and it is untested on a real RTL phone | Maintained (pushed 2026-10-16). Re-themable through `--wa-*` custom properties, no Sass. **Accessibility record: a commitment statement only, no WCAG claim or report (FETCH).** **Gotcha:** `<wa-icon>` fetches SVGs from ka-f.fontawesome.com at runtime, so do not use it. **Licence note:** `native.css` itself embeds 3 inline SVGs marked "Font Awesome Free 7.0.0 ... License - https://fontawesome.com/license/free", a separate licence from MIT (that page is script-rendered and its terms were not read; UNVERIFIED) |
| Oat 0.8.3 (`@knadh/oat`) | MIT (RAW) | CSS 31,287 / 7,064; JS 10,910 / 3,924 | 28 / 0 margin-padding (6 left:/right:) | CSS is RTL-clean. JS widgets untested; no RTL docs | Created 2026-01-15, "sub v1 ... likely to have breaking changes". Uses `light-dark()` (Baseline low only). Close to the shadcn look |
| Pico.css 2.1.1 | MIT | 83,319 / 11,617 | 16 / 39 / 11 | Partial, with open RTL bugs (breadcrumbs, dropdown, modal, blockquote) | **Archived; v2.1.1 is the final release** (`gh api`: archived=true). Very recognisable |
| Shoelace 2.20.1 | MIT | theme 19,536 / 4,160 | weak evidence | RTL detection had regressions (issues #773, #2188) | **Archived/sunset** (`gh api`: archived=true). Replaced by Web Awesome |
| USWDS 3.14.0 | Public domain (CC0) + bundled OFL/Apache/MIT | CSS 526,999 / 60,480; JS 78,904 / 22,604 | 15 / 2,446 / 3 | **Not ready.** Issue #5336, "CSS logical properties for multilingual support", open since 2023-06-15. Maintainer, 2026-09-18 (VERIFIED-VERBATIM via `gh`): "The next step is a working right-to-left example" | Reads as a US federal site. Colours and fonts are baked in by Sass |
| GOV.UK Frontend 6.6.0 | MIT code; Crown brand and GDS Transport restricted by guidance | CSS 136,349 / 16,051; JS 46,777 / 11,376 | 0 / 346 / 0 | **Not ready.** Issue #7303 (open, 2026-07-17); PR #7465 "[HACKY SPIKE] Convert Sass to use logical properties" (open, 2026-10-09) (both VERIFIED via `gh`) | Reads as gov.uk |
| NHS.UK frontend 10.6.1 | MIT code; NHS identity and Frutiger restricted | CSS 278,132 / 29,505 | 0 / 587 / 0 | **Not ready** | Reads as NHS; hotlinks a font at runtime |
| Material Web 2.5.0 | Apache-2.0 | no dist bundle; bare imports of `lit` and `tslib` | sampled: 0 / 0 | Unverified | "maintenance mode pending new maintainers"; needs an import map. Poor fit |
| Carbon Web Components 2.65.0 | Apache-2.0 | button style alone 104,128 | 112 / 0 (button) | Plausible, but no docs | Bare imports; CDN-only bundles; IBM look. Not a no-build fit |
| Lion 0.24.0 | MIT | 8.7 MB package, no dist | n/a | No docs | Unstyled, so all CSS is ours anyway. No |
| Fluent UI WC 3.1.3 | MIT | 274,342 / 66,094 | 99 / 3 | Good in code | Needs an import map plus vendored fast-element. Microsoft look |
| Open Props 1.7.23 | MIT | 29,566 / 7,645 | n/a | Direction-neutral (tokens only) | Invisible: we would write every component ourselves |

**Why Web Awesome's native styles fit this app specifically:**
- `app.js` builds plain elements through `el()`: `<button>`, `<input>`,
  `<select>`, `<label>`, `<details>`, `<iframe>`.
- `native.css` styles those same elements. Its selector list (RAW) includes
  button, label, fieldset, input[type=file], radio, checkbox, select,
  textarea, details and dialog.

So this is "premade elements" with zero JS changes, no Shadow DOM and no
runtime icon fetch:
- Vendor 7 files into `app/static/vendor/webawesome/`, keeping the
  `dist-cdn/styles/` folder layout so the relative `@import`s resolve (the
  first draft said 3 files; with 3 the imports 404 and palette variables
  are undefined). `native.css` imports `layers.css`, `utilities/size.css`
  and `utilities/variants.css`; `themes/default.css` imports `../layers.css`
  and `../color/palettes/default.css`, which imports `base.css`. Sizes
  (curl, 3.14.0): native.css 37,010; themes/default.css 16,773;
  layers.css 691; utilities/size.css 317; utilities/variants.css 2,964;
  color/palettes/default.css 8,537; color/palettes/base.css 2,754 B.
- Load our `tokens.css` and `style.css` after them, unlayered, so they win
  over the `@layer wa-*` rules.
- Do not load any `wa-*` web components.
- If native.css misbehaves on a real phone, the runner-up is Oat's CSS
  alone.

### 5.4 Multiscript typography (H4: the rival won the recommendation)

Collector C read the cmap and OS/2 tables of the google/fonts binaries
(RAW). I cross-checked the subset lists against api.fontsource.org (RAW).

**IBM Plex Sans + Plex Sans Arabic + Plex Sans Devanagari** (OFL-1.1, one
design programme)
- **Matched metrics (downgraded):** the three files report the same OS/2
  x-height / cap-height, 0.516 / 0.698 (single measurement, not re-run).
  Those fields describe the Latin glyphs each file bundles, so they show
  that the bundled Latin matches, NOT that the Arabic or Devanagari is
  proportioned to the Latin (Arabic has no x-height; Devanagari's
  relevant measure is the headline). Harmony across scripts is a design
  claim nobody here measured. Correction: METADATA does not show a single
  designer. Plex Sans and Plex Sans Devanagari credit "Mike Abbink, Bold
  Monday"; Plex Sans Arabic credits "Mike Abbink, Bold Monday, Khajag
  Apelian, Wael Morcos" (curl of the raw METADATA.pb files).
- **Not distinctive:** [A2]'s TYPOGRAPHY_PROMPT lists "Technical: IBM Plex
  family, Source Sans 3" under "Impact choices" it pushes the model toward
  (curl of the .ipynb, VERIFIED-VERBATIM). So Plex is itself a probable
  AI-generated default. It is kept for coverage, not novelty.
- **Coverage:** Plex Sans covers Latin, Vietnamese and Cyrillic (fontsource
  subsets confirm).
- **Formats:** Arabic and Devanagari are static files only.
- **Sizes per weight:**

| File | Size |
|---|---|
| Plex Sans Latin 400 | 22.6 KB |
| Plex Sans Vietnamese 400 | 8.2 KB |
| Plex Sans Cyrillic 400 | 14.8 KB |
| Plex Sans Arabic | about 43-44 KB |
| Plex Sans Devanagari | about 77 KB |

- **Korean:** Plex Sans KR is on Fontsource as 92 unicode-range slices at
  weight 400: median 12,480 B, max 15,664 B, 1,106,632 B in all (my
  script, 2026-10-17 15:0x CDT; the earlier "about 17 KB each" was wrong).
- **Chinese:** Plex Sans SC/TC are not on Google Fonts or Fontsource
  (google/fonts has no `ofl/ibmplexsanssc` or `ibmplexsanstc`;
  api.fontsource.org returns 404). They exist as IBM npm packages:
  `@ibm/plex-sans-sc` 1.1.0 is 123,861,375 B unpacked, `@ibm/plex-sans-tc`
  1.1.1 is 86,503,216 B (npm registry). Correction: the packages DO ship
  ready-made unicode-range split woff2 files plus CSS, so vendoring them is
  possible; section "CJK strategy" below prices it and rejects it.

**Noto Sans + Noto Sans Arabic**
- Noto Sans alone covers Latin, Vietnamese, Cyrillic and Devanagari
  (fontsource subsets confirm `devanagari`). Arabic is the only extra file.
- Noto Sans Arabic: the static 400 file is 48.8 KB. The variable file is 166
  KB, too heavy.
- Shared x-height: 0.536.
- The safest choice, and the most generic.

**Readex Pro**
- Latin, Vietnamese and Arabic in one variable family: 31 + 11 + 23 KB.
- The most distinctive single family.
- No Cyrillic or Devanagari, so Russian and Hindi fall back to Noto Sans.
- No description file exists, so its design intent is undocumented.

**Rejected**
- **Atkinson Hyperlegible Next:** Latin only, with no Vietnamese, Cyrillic,
  Arabic or Devanagari (cmap RAW; fontsource lists only latin and
  latin-ext). That rules out the "accessibility font" idea for a
  four-script app.
- **Rubik:** no Vietnamese.
- **Vazirmatn:** only partial Vietnamese.
- **Instrument Sans:** Latin only.
- **Public Sans:** no Cyrillic.

**CJK strategy (revised 15:11 CDT; Chinese is now tier 1): system CJK
fonts through explicit per-language stacks, no CJK webfont.**

What the options cost. All sizes are woff2 at weight 400 only, computed by
my script from the Fontsource API and the jsDelivr file listing on
2026-10-17 (~15:07 CDT). "UI strings" = every zh-CN or zh-TW string in
`app/static/app.js` at commit 145c8af (229 / 232 distinct characters above
U+2E7F); the slices counted are those whose unicode-range contains at least
one of them. app.js is being edited in parallel, so these counts are a
reading at that commit, not a constant.

| Option | On disk to vendor (one weight) | Downloaded for zh-CN UI strings | Downloaded for zh-TW UI strings |
|---|---|---|---|
| A. System fonts (recommended) | 0 B | 0 B | 0 B |
| B. Noto Sans SC / TC, Fontsource slices | SC 97 slices, 2,382,648 B; TC 104 slices, 2,270,144 B | SC: 11 slices, 341,740 B | TC: 12 slices, 445,048 B |
| C. IBM Plex Sans SC / TC, IBM split woff2 | SC 216 files, 5,654,132 B; TC 206 files, 4,327,152 B | SC: 11 slices, 436,732 B | TC: 80 slices, 1,764,548 B |
| D. One file per face | Plex SC 3,813,972 B; Plex TC 2,496,872 B (IBM "complete" woff2) | whole file | whole file |
| E. Subset to the UI strings only | not measured (no fontTools here; not installed by rule) | - | - |

Why A wins:
1. **Size.** For comparison, the whole Plex Sans Latin 400 file is 22,588
   B. Option B adds about 15x that (341,740 / 22,588) for zh-CN and about 20x
   (445,048 / 22,588) for zh-TW, per weight, before any explanation text.
   The design uses two weights (400 and 700), and the 700 set was not
   measured.
2. **Dynamic text breaks subsetting.** Tier-1 Chinese users also get the
   model's translated explanation and letter, whose characters are not
   known in advance. A static subset (option E) would show missing glyphs
   or fall back mid-sentence; only the full slice sets (B, C) are safe, and
   each new character can pull another 1-45 KB slice.
3. **Every target platform already ships a CJK face** (table below), so A
   costs nothing and renders native-looking text at once, with no
   font-display swap flash.
4. **The cost of A:** CJK glyphs do not share Plex's design. Latin and
   digits inside Chinese text still render in Plex because Plex is first in
   the stack, so the numbers (the part the number lock protects) stay
   matched.

Installed CJK fonts per platform:

| Platform | Simplified | Traditional | Korean | Evidence |
|---|---|---|---|---|
| Windows 11 | Microsoft YaHei | Microsoft JhengHei | Malgun Gothic | Microsoft "Windows 11 font list" (curl + grep, RAW); also detected as installed on this Windows 11 machine by a canvas width probe in the desktop app's Chromium 152 |
| iOS / macOS | PingFang SC | PingFang TC | Apple SD Gothic Neo | Apple developer "System Fonts" list (curl, RAW): Apple SD Gothic Neo is "system font" on iOS and macOS. PingFang SC/TC are labelled "downloadable" on iOS AND macOS, and Heiti SC/TC "downloadable" on iOS. clreq also says PingFang is "Downloadable". See UNVERIFIED in section 10 |
| Android | Noto Sans CJK (SC face) | Noto Sans CJK (TC face) | Noto Sans CJK (KR face) | AOSP `fonts.xml` (raw, main branch): unnamed fallback families `lang="zh-Hans"` (NotoSansCJK-Regular.ttc index 2), `lang="zh-Hant,zh-Bopo"` (index 3), `lang="ko"` (index 1) |

Rules for the stacks:
- **Use the app's own tags.** `applyDir()` sets `<html lang>` to `zh-CN`
  or `zh-TW`, and tier-2 explanation paragraphs get `lang="ko"` etc.
  (`app.js`). Write CSS as `:lang(zh-CN)` and `:lang(zh-TW)`. The earlier
  draft said `:lang(zh-Hans)` / `:lang(zh-Hant)`; those would NOT match:
  Selectors 4 defines `:lang()` as RFC 4647 extended filtering (w3.org
  selectors-4, RAW), and the range `zh-Hans` does not match the tag
  `zh-CN`. Do not change the app's tags.
- **The tags are enough for glyph choice on Android/Chrome.** Chromium maps
  `zh-tw` to Traditional Han and plain `zh` to Simplified Han
  (`locale_to_script_mapping.cc`, RAW), then asks Skia for `zh-Hant` or
  `zh-Hans`, matching the AOSP families above (`layout_locale.cc`, RAW).
  Because the Android families are unnamed, the name "Noto Sans CJK SC" in
  CSS is harmless but does nothing there; the `lang` attribute does the
  work.
- **Stacks:**
  - `:lang(zh-CN)`: "IBM Plex Sans", "PingFang SC", "Microsoft YaHei",
    "Noto Sans CJK SC", sans-serif;
  - `:lang(zh-TW)`: "IBM Plex Sans", "PingFang TC", "Microsoft JhengHei",
    "Noto Sans CJK TC", sans-serif;
  - `:lang(ko)`: "IBM Plex Sans", "Apple SD Gothic Neo", "Malgun Gothic",
    "Noto Sans CJK KR", sans-serif.
- **Han-unification probe.** On this Windows machine the same four
  characters tagged zh-CN and zh-TW rendered in YaHei and JhengHei
  respectively (screenshot inspected; scratch page, not committed).
- web.dev (RAW): "CJK fonts may have over 10,000 characters".
- Preload ignores unicode-range, so never preload CJK slices.

**Korean (tier 2) renders acceptably on the platforms checked.** It is
explanation text under an English interface, already tagged `lang="ko"`.
Hangul is its own script, so there is no Han-unification risk unless the
text contains Hanja. Windows: rendered in Malgun Gothic with no missing
glyphs (screenshot, this machine). iOS and Android: by the vendor lists
above only; not rendered on a device (section 10).

**Loading**
- One `@font-face` per script, each with `unicode-range`. A file downloads
  only when the page contains a matching character (web.dev, RAW). Hindi
  users pay for Devanagari; nobody else does.
- `font-display: swap` for body text (MDN, RAW).

**Digits**
- CLDR 48 defaults `ar` to Western digits (Intl in Node 24.20, RAW).
  Correction: not only `ar-EG` and `ar-SA` but also `ar-SY`, `ar-IQ`,
  `ar-YE`, `ar-LB` and `ar-JO` default to Arabic-Indic digits; `ar-MA` and
  `ar-US` default to Western (re-run 2026-10-17). Several of those are
  likely origins of US Arabic speakers, so Western digits are a choice that
  needs a fluent reviewer's sign-off, not a default.
- Keep Western 0-9. They match the bill, the phone numbers and the number
  lock, and they avoid the bidi "AN" class.
- Wrap every number, date and currency amount in `<bdi>`.

**Korean system font names:** previously unverified (the collector's
recollection); now verified against Microsoft's Windows 11 font list,
Apple's System Fonts list and AOSP `fonts.xml` (see the CJK table above).

### 5.5 Screen patterns

1. **Bill capture and field confirmation**
   - **Incode OCR review (RAW).** Fields are "pre-filled for the user to
     review and confirm". Do: "Highlight editable fields". Don't: "present
     ... low-confidence OCR results without prompting the user to retry".
   - **GOV.UK check answers (RAW)** adds a "Change" link per row and a
     submit button that names its action.
   - **USWDS (RAW)** warns about large files on limited data plans.
     Downscale the photo in the browser before upload.
   - The app's current pattern already matches: a blank field means "could
     not read", it is highlighted, and each field is confirmed.
   - **Design addition:** on wide screens, show the photo beside the field
     list. On a phone, show it above the list, sticky and collapsible.
   - **Not found:** any documented "per-field crop of the source image"
     pattern. Only highlight-on-source and side-by-side were found. Treat a
     per-field crop as our own unproven idea, and do not build it this
     weekend.
2. **Eligibility result**
   - **Prior art (all FETCH):**
     - Model results pages give three outcomes (eligible, not eligible, may
       be eligible), each with its own next step (Michigan WIC).
     - Results pages say they "are not intended to replace" the official
       notice (Medicaid model results, search snippet).
     - The Delaware screener gives estimates and explains why.
   - **Our order:**
     1. the answer, in one sentence;
     2. the evidence (the policy-table row);
     3. the deadline;
     4. the action.
   - "The hospital makes the final decision" stays on screen.
   - **No model confidence number.** An uncalibrated score erodes trust
     (practitioner post, FETCH, low quality), and the tier comes from the
     rules engine anyway.
3. **Printable packet**
   - Use `@page` margins, `break-inside: avoid` on tables, and
     `print-color-adjust: exact` only where colour carries meaning. Never
     rely on colour alone. (MDN, RAW, for the property definitions;
     tutorials FETCH.)
   - Keep the SYNTHETIC banner, the citations and the date in print.
4. **RTL mirroring**
   - **Material bidirectionality** (my browser read of m2.material.io,
     VERIFIED-VERBATIM).
     - Not mirrored: "Numbers", "Untranslated text (even if it's part of a
       phrase)", "Icons that don't communicate direction", "Charts and
       graphs".
     - Mirrored: "Progress bars fill in the same direction as content is
       read", and navigation order.
   - **Wikimedia Codex (RAW):** don't mirror check marks, clocks, calendars
     or media icons.
   - **W3C (VERIFIED-VERBATIM):** "Never use CSS to apply the base
     direction".
     - Use `dir` on `<html>`, which `applyDir()` already does.
     - Use logical properties.
     - Use `dir="auto"` on user-typed inputs.
   - **Applied in the mock:**
     - the step bar mirrors;
     - the sliding-scale chart does not;
     - English policy text stays LTR inside `<bdi>`.
5. **Language picker**
   - Hilton (2020-11-03, VERIFIED-VERBATIM): "national flags represent
     countries, not languages". Name each language in itself. Show the
     names rather than hiding them in a dropdown.
   - W3C (RAW): mark each name with `lang`.
   - The current app already does all three, so keep it.
   - flagsarenotlanguages.com returned only boilerplate, so it is not cited.

### 5.6 Frontend architecture (H5 survived)

**Recommendation: stay vanilla JS.**
- Keep `app.js` and its `el()` renderer.
- Add vendored CSS only: Web Awesome native styles, our tokens, and the Plex
  `@font-face` rules.
- Adopt no framework.

Every option was measured RAW by collector B. Their fit for this app:

| Option | License | Size | Fit for this app |
|---|---|---|---|
| htmx 2.0.11 | 0BSD | 52,182 / 16,826 B | **Poor.** It swaps server-rendered HTML fragments, but our API returns JSON. Adopting it means rewriting the endpoints' output |
| Alpine.js 3.17.4 | MIT | 55,891 / 19,895 B | **Neutral.** It would mean rewriting the 375-line `app.js`. The standard build needs unsafe-eval, so the CSP build (72,198 B) would be required |
| Lit 3.3.3 | BSD-3-Clause | about 16.5 KB raw (about 7 KB gz) for the core files | **Usable without a build, but still a poor fit.** Correction: official single-file bundles DO exist in the lit/dist GitHub repo (`cdn.jsdelivr.net/gh/lit/dist@3/core/lit-core.min.js`, 15,734 B; `.../all/lit-all.min.js`, 29,370 B; both HTTP 200, curl). The first draft looked only at npm paths, where they 404. The fit is unchanged: adopting it means rewriting `app.js` into components |

**Native platform features cover the gaps without a framework.** All are
"Baseline widely available", per the web-features dataset v3.43.0 (the
MDN/caniuse Baseline source, RAW):
- `<dialog>` and `<details>`;
- `:has()` (widely available 2026-06-19);
- logical properties;
- CSS nesting (widely available 2026-06-11);
- `@layer`;
- `:dir()`.

**Avoid** `light-dark()`, popover and `details[name]`. They are Baseline
"newly available" only.

## 6. The three directions

All ratios were computed with the WCAG 2.x relative-luminance formula (my
script). AA needs 4.5:1 for body text, and 3:1 for large text and UI
boundaries (WCAG 1.4.3 and 1.4.11).

### Direction 1 - Paper Trail (RECOMMENDED)

**Idea:** the result reads like a well-made document. It shows the
hospital's own policy table with your row highlighted, and every claim is
footnoted to its page.

**Signals trust to:**
- the physician and Vanderbilt faculty: sources first, the mechanism visible;
- the HCA application-services director: it looks like the artifact their
  staff already process;
- families who already trust paper.

**Colour tokens**

| Token | Hex | Pair | Ratio | Use |
|---|---|---|---|---|
| ink | #1B2430 | on paper #FFFFFF | 15.65:1 | body text |
| ink | #1B2430 | on desk #EEF1F4 | 13.81:1 | text on the page background |
| ink-2 | #4A5361 | on paper | 7.77:1 | secondary text |
| ink-2 | #4A5361 | on desk | 6.86:1 | secondary text on the background |
| pen (actions) | #1F4FA3 | white on pen | 7.76:1 | primary button |
| pen | #1F4FA3 | on paper | 7.76:1 | links, footnote markers |
| pen | #1F4FA3 | on desk | 6.85:1 | links on the background |
| highlighter | #FFE45C | ink on highlighter | 12.30:1 | your policy row, the deadline |
| rule | #8A93A0 | on paper | 3.11:1 | input borders, table rules (UI only, never text) |
| rule | #8A93A0 | on desk | 2.74:1 | decorative only (sheet edge, rules on desk-tinted cells). Below 3:1, so no input or control boundary may sit on desk |
| focus | #FFBE2E | ink on focus | 9.43:1 | focus halo outside a 2px ink outline (borrowed from Direction 2) |
| synthetic tag | #7A2E00 on #FFF4E5 | - | 8.71:1 | SYNTHETIC DEMO badge |

- Highlighter on white is only 1.27:1, and on desk 1.12:1. It is only ever
  a background behind ink text, never a foreground or a boundary. On a
  projector it may wash out, so the row must not depend on it (next point).
- The highlighted row also carries a "You: 115%" tag and a 4px ink bar, so
  colour is not the only cue. Under forced-colors mode (Windows High
  Contrast) backgrounds are dropped, so the build adds a 3px `CanvasText`
  border on the row and the deadline (in the mock).
- Focus on a highlighted row: gold on highlighter is 1.30:1, so the 2px ink
  outline (12.30:1 on highlighter) is what carries focus there; the gold
  halo is decoration.
- [A1] lists "tinted near-black (#0B0B0B, #111) standing in for black" as
  template chrome. Ink #1B2430 is a tinted near-black. Kept as one token in
  a subject-derived palette, but the claim that D1 "avoids every tell" is
  withdrawn (see the recommendation).

**Type**
- IBM Plex Sans (Latin, Vietnamese, Cyrillic), Plex Sans Arabic and Plex
  Sans Devanagari, weights 400 and 700 (changed from 400/600 to match the
  mock and the measured Arabic files, and because the system CJK fonts on
  Windows ship Regular and Bold faces, so 700 maps to a real face).
- CJK and Korean system stacks, set per `:lang()` with the app's own tags
  (`zh-CN`, `zh-TW`, `ko`); the full stacks are in section 5.4. The first
  draft keyed them to `zh-Hans` / `zh-Hant`, which would not match.
- Phone scale: 14 / 16 / 19 / 23 / 28 px (14 added for footnotes, table
  text and labels, which the mock needs).
- Line height 1.5 for body text, 1.7 for Arabic, because its tall ascenders
  and descenders crowd. Devanagari and Vietnamese (stacked diacritics) were
  not checked; no source was read (section 10).
- No serif display face (avoids tell 5).

**Spacing, radius, elevation**
- A 4px base spacing scale: 4 / 8 / 12 / 16 / 24 / 32.
- Radius 4px on the sheet and buttons; 0 on tables.
- No drop shadows (no elevation). Hierarchy comes from the white sheet on
  the grey-blue desk and 1px rules. The 4px row bar is a border, and the
  deadline mark is a flat fill (the mock was changed from an inset
  box-shadow and a gradient).
- Tap targets of at least 48px everywhere, footnote rows included.

**Icons**
- Phosphor (MIT; `@phosphor-icons/core` 2.1.1; license RAW from
  package.json), regular weight only.
- About 6 inline SVGs, copied into `app/static/icons/`: camera, check,
  calendar, file, printer, globe.

**Component base:** Web Awesome native.css plus its default theme (7 files,
section 5.3), with our tokens on top.

**Signature details**
1. **The policy-table excerpt with your row highlighted.** It turns "a rules
   engine decided" into something you can see. Markup: `<thead>`, a row
   header (`<th scope="row">`) per band, and `aria-current="true"` on your
   row, so a screen reader can find it (the mock now does this). Limit:
   the table text is the hospital's English; in Arabic and Chinese only the
   "You" tag and the sentence above it are translated.
2. **Numbered footnote citations that open the policy page.** The tappable
   element is the full-width footnote row (at least 48px), not the
   superscript. A superscript alone would fail WCAG 2.2's 24px target-size
   minimum (2.5.8). The preview mock still uses small superscript links,
   and the build must not copy that.
3. **A highlighter mark used in exactly two places:** your row and the
   deadline.

**Result screen:** see the HTML mock (English, Arabic and zh-CN). The
segmented step bar borrowed from Direction 2 is not drawn in the D1 mocks.

**Build cost: about 6.0 agent-hours (a judgment, not measured; was 5.5)**

| Task | Hours |
|---|---|
| Vendor fonts, the 7 Web Awesome files and icons; write the asset-license list (incl. the Font Awesome SVGs inside native.css) | 0.5 |
| Tokens, plus a restyle of the five screens | 1.5 |
| Tier-table rows for the Result screen: option A, an additive field from the engine (1.0); option B, rows hard-coded from the synthetic policy and labelled (0.5). Section 7 | 1.0 |
| Footnote citations | 0.5 |
| Print CSS for the packet | 0.5 |
| NEW: CJK and Korean `:lang()` stacks; zh-CN and zh-TW screen QA | 0.5 |
| RTL, phone (320px reflow), projector and forced-colors QA, plus the pre-mortem T5 deploy check, with fixes | 1.5 |

With option B the total is about 5.5. One agent at 6.0 hours uses about
77% of the 7.8 wall-clock hours left (6.0 / 7.8), so the tier-row task
should go to a second agent if option A is chosen.

**Risks**
- The tables must fit a 320px width (WCAG 1.4.10 reflow) in Arabic and
  Chinese. The three D1 mocks fit: at a 320px viewport the tables measure
  226 px of content in a 228 px box, with no page scroll (Chromium,
  2026-10-17). The real app screens are unchecked.
- The look can slide into "broadsheet" (tell 5) if someone adds
  hairline-only layouts, zero radius and dense columns. Keep the 4px radius,
  the white sheet and generous spacing.
- Option A touches tested code, so re-run all four test files, and it
  conflicts with the wording of pre-mortem T5 ("never the API calls").
- Plex Devanagari costs 77 KB per weight, but it loads only for Hindi.
- System CJK fonts differ by phone, so the zh screens will not look
  identical across devices; check the demo phone.
- The design mimics a hospital document. It needs a visible "not
  affiliated with the hospital" line (raised by the cold assessment; not
  researched).

### Direction 2 - Public Counter

**Idea:** a service-desk system in the GOV.UK/USWDS tradition.
- One decision per screen.
- The answer first, in very large type.
- A sliding-scale bar built from the policy's real bands.

**Signals trust to:**
- the HCA director and the Oracle executives: rigour, workflow clarity,
  accessibility;
- public-service users who already know government forms.

**Colour tokens**

| Token | Hex | Pair | Ratio |
|---|---|---|---|
| ink | #1B1B1B | on white | 17.22:1 |
| river (links, done steps) | #00597A | white on river, and river on white | 7.75:1 |
| go (primary button, free-care band) | #1B6B3A | white on go | 6.54:1 |
| ink-2 | #565C65 | on white | 6.74:1 |
| line | #71767A | on white | 4.59:1 |
| answer tint | #F1F8F3 | ink on it | 15.96:1 |
| band 3 | #3D4551 | white on it | 9.68:1 |
| soft | #F0F0F0 | ink on it | 15.11:1 |
| focus gold | #FFBE2E | ink on gold | 10.38:1 |

Gold on white is 1.66:1. The focus ring must therefore be gold *plus* a 2px
ink outline (the GOV.UK pattern), never gold alone.

**Type**
- Noto Sans (Latin, Vietnamese, Cyrillic and Devanagari in one family) plus
  Noto Sans Arabic static 400/700.
- CJK system stacks, as in Direction 1.
- Heavy 800 headings at 30-32px on a phone.

**Spacing, radius, elevation**
- An 8px grid.
- Radius 2px.
- No shadows, except a 3px solid "pressable" bottom edge on the primary
  button.

**Icons:** Material Symbols (Apache-2.0; `@material-symbols/svg-400` 0.48.0;
license RAW).

**Component base:** Web Awesome native.css with our tokens. **Not USWDS**,
because of RTL (section 5.3), even though the look borrows from it.

**Signature details**
- The sliding-scale bar, with a "You: 115%" pin.
- A segmented 5-step bar. It mirrors in RTL; the chart does not.
- An answer block with a 6px inline-start rule.
- No cards anywhere.

**Build cost:** about 4.5 agent-hours. It needs the same engine change for
the bands; the bar itself is about 40 lines of CSS.

**Risks**
- It reads as a government site. The GDS trust evidence is about
  recognising government, so judges may ask "is this a government service?"
- The [A2] generic-font critique applies to Noto.
- It is the least ownable of the three.

### Direction 3 - Front Porch

**Idea:** a warm community-clinic voice.
- The result is a sentence spoken to the helper ("For your father's bill").
- A three-item to-do list follows; only the deadline item is filled in.

**Signals trust to:**
- families and the adult child helping a parent.
- It is weaker with the executives and the physician, because it shows less
  evidence.

**Colour tokens**

| Token | Hex | Pair | Ratio |
|---|---|---|---|
| ink | #10302A | on white | 14.21:1 |
| ink | #10302A | on surface #F1F6F4 | 13.01:1 |
| green | #0F6B5C | white on green, and green on white | 6.41:1 |
| green | #0F6B5C | on surface | 5.87:1 |
| marigold | #F2B035 | ink on marigold | 7.47:1 |
| ink-2 | #4D615C | on white | 6.60:1 |
| ink-2 | #4D615C | on surface | 6.05:1 |
| edge (input borders) | #5F7A73 | on white | 4.65:1 |

- Marigold on white is 1.90:1, so it is used only as a fill behind ink.
- A first-draft border colour (#A9BDB7, 1.97:1) failed WCAG 1.4.11 and was
  replaced by #5F7A73.

**Type**
- Readex Pro (Latin, Vietnamese and Arabic in one variable file).
- Noto Sans as the fallback for Cyrillic and Devanagari.
- CJK system stacks.

**Spacing, radius, elevation**
- Radius by role: 16px on the result panel, 999px on pills and the primary
  button, 50% on the step numerals.
- No shadows.

**Icons:** Tabler (MIT; 3.49.0; license RAW), outline style.

**Component base:** Web Awesome native.css. `wa-radio-group` could make the
pill toggle. Avoid `wa-icon`, because it fetches from a runtime CDN.

**Signature details**
- A marigold underline under the key numbers.
- A numbered next-steps list where only the deadline item is filled.
- A pill language toggle.

**Build cost:** about 5 agent-hours.

**Risks**
- Pills and soft panels drift toward the "SaaS-card kit" tell.
- The gendered "your father" copy needs a neutral variant for the "me" path.
- The policy evidence is a single line, so the credibility story is weaker.
- Readex Pro's design intent is undocumented.
- Its marigold underline on numbers inside the headline is [A1]'s
  "accenting just a single word or phrase in a headline" tell (tell 13).

### Recommendation: Direction 1, Paper Trail

1. **It answers the judges' questions.**
   - Credibility and UX are rubric criteria. The pitch says "a rules engine
     applies the hospital's rules", and a highlighted policy row shows that
     rule in under two seconds of the demo (the 0:44 and 0:56 beats).
   - The physician and faculty judges get footnoted sources.
   - The HCA director sees an artifact their counsellors would recognise.
2. **It is easy for families to read.**
   - One sentence answer, one highlighted row and one highlighted date.
     Caveat (cold assessment): the table itself stays in the hospital's
     English in every language, and no source was read on how low-literacy
     or low-numeracy readers handle percentage tables. The translated
     sentence above the table carries the answer; the table is evidence.
   - One Plex family covers Latin, Arabic and Devanagari, and Chinese uses
     the phone's native CJK face, so no tier-1 screen falls back to a
     mismatched default. (The first draft claimed "matched metrics" across
     scripts; only the bundled Latin metrics were measured, section 5.4.)
3. **It is not AI-looking by construction, with two exceptions.**
   - Its distinctive elements (the policy table, footnotes, highlighter)
     come from the subject's own vernacular. That is the fix [A1]
     prescribes (an interested source; see the TL;DR caveat).
   - It has no gradients, card stack, eyebrows, cream-and-serif or
     sparkle. But it does NOT avoid every tell, as first claimed: ink
     #1B2430 is a tinted near-black ([A1] template chrome), and Plex is on
     [A2]'s list of fonts it steers the model toward.
4. **It borrows four patterns from Direction 2:**
   - the segmented step bar;
   - one question per page on screen 3;
   - a check-answers summary before "See my result";
   - the 2px ink plus gold focus ring.

   These are patterns, not looks, and they carry the GOV.UK evidence.

## 7. Build plan for the recommended direction (for the code agents)

**Timing (revised 15:11 CDT).** The 5:00 PM gate passed at 14:53 CDT and the
app is live with real OCI at http://207.211.181.174/. The redesign competes
only with the freeze at about 23:00 CDT tonight (Sat 2026-10-17) and with
the other pre-mortem launch-blockers. Order:
1. Evan decides the tier-row option (below). Until then, build everything
   else.
2. One agent restyles; it changes CSS and markup only and no API calls
   (pre-mortem T5).
3. 21:00 CDT go/no-go (a judgment, leaving 2 hours for the T5 deploy check
   and a rollback): if the done-check is not passing, ship only the
   1.5-hour subset in section 11 and revert the rest to the last good
   commit.
4. Deploy only after the T5 check: a scripted journey run plus a browser
   check in en, ar and zh-CN (T5), plus zh-TW (tier 1).

**Files.** One agent can own all of them:
- `app/static/vendor/webawesome/`: the 7 files listed in 5.3 in their
  `styles/` layout, plus the LICENSE and a note on the 3 Font Awesome Free
  SVGs embedded in native.css.
- `app/static/fonts/`: Plex woff2 files (Latin, Vietnamese, Cyrillic,
  Arabic, Devanagari; 400 and 700) plus `OFL.txt`. No CJK or Korean font
  files.
- `app/static/icons/`
- `app/static/style.css`: tokens, `@font-face` rules, the `:lang(zh-CN)`,
  `:lang(zh-TW)` and `:lang(ko)` stacks from 5.4, screen styles, a
  `forced-colors` block.
- `app/static/app.js`, markup only:
  - the footnote list;
  - `<bdi>` wraps;
  - the policy-row table (`<thead>`, `<th scope="row">`,
    `aria-current="true"` on your row);
  - the step bar;
  - the `cite()` bidi fix (all three translated words: source, page,
    effective).
  - Do NOT change the `lang` values `applyDir()` sets (`zh-CN`, `zh-TW`):
    the CSS and Chromium's font choice both key on them.

**Tier-table rows: a decision for Evan.** The Result screen needs every
band, but `/evaluate` returns only the matched tier (`app/engine.py`).
- Option A (recommended for honesty of the "rules engine" story): add an
  additive `tiers` list to the engine result, read from the same policy
  JSON the engine uses. No existing field changes, but it touches tested
  code (re-run the four test files) and conflicts with T5's wording ("never
  the API calls"). Do it as its own commit, before the restyle, so it can
  be reverted alone.
- Option B: hard-code the four rows in `app.js` from
  `app/data/policy_cumberland_synthetic.json`, labelled as copied from the
  synthetic policy. No API change, but two copies of the policy that can
  drift.
- Use the policy's own labels: the last band is "Not eligible under this
  policy - payment plan available", not "Payment plan" (the mock was
  corrected).

**Done-check:**
- The Result screen matches the mock in English, Arabic, zh-CN and zh-TW,
  with no horizontal scroll at 320px CSS width (WCAG 1.4.10) and at 375px.
- Chinese text renders in a CJK face (no missing-glyph boxes) on the demo
  phone, and a tier-2 Korean explanation renders on it too.
- An axe or Lighthouse accessibility run is saved, dated, in `docs/`.
- The asset-license list is written (`ui.md` requires it).
- All four test files pass.
- The pre-mortem T5 deploy check passed before deploying.

## 8. Verification table (stage 8.5)

Load-bearing claims only. Each was re-read through a different call than the
one that found it.

| Claim | Source | Verdict |
|---|---|---|
| Anthropic lists cream+serif+terracotta, the SaaS-card kit and template chrome as AI-generated clusters | frontend-design SKILL.md: the local plugin copy, read in full; the GitHub raw file, read by collector A | VERIFIED-VERBATIM |
| Purple gradients on white, and Inter/Roboto/Arial/system fonts, are named cliches | Anthropic cookbook notebook on raw.githubusercontent (curl + grep) | VERIFIED-VERBATIM |
| The sparkle icon "suffers from ambiguity" | nngroup.com (curl) | VERIFIED-VERBATIM |
| "all apps started looking the same" | ui.shadcn.com changelog, Dec 2025 (curl) | VERIFIED-VERBATIM as a quote; NOT evidence about AI (the post does not mention AI; cold assessment, re-checked by curl) |
| USWDS lacks RTL: issue #5336 is open, and the maintainer said on 2026-09-18 that the next step is a working RTL example | `gh issue view 5336` | VERIFIED-VERBATIM |
| GOV.UK Frontend lacks RTL | `gh`: issue #7303 open, PR #7465 open; my CSS count (0 logical) | VERIFIED-VERBATIM (issue and PR titles) + measured |
| GDS Transport is for service.gov.uk only | design-system.service.gov.uk/styles/typeface (curl) | VERIFIED-VERBATIM (it is guidance, not a license clause) |
| GOV.UK-style trust comes from recognising government | gds.blog.gov.uk, 2024-01-12 (curl) | VERIFIED-VERBATIM |
| Web Awesome supports `dir` via `<html dir>` and is MIT | webawesome.com/docs/localization (browser page text); package.json (curl) | VERIFIED-VERBATIM, but the quote covers the web components, not `native.css` |
| Web Awesome native.css uses logical properties | my measurement on jsdelivr dist-cdn: 22 vs 1; collector B: 23 vs 0 | Measured twice, and the two counts disagree slightly (heuristic count) |
| Web Awesome native styles need 7 files, not 3 | `@import` lines in native.css, themes/default.css and color/palettes/default.css (curl, 3.14.0; all 7 return 200) | VERIFIED (raw files); corrects the first draft |
| Pico and Shoelace are archived | `gh api repos/.../ --jq .archived` = true for both; Pico pushed_at 2026-10-04 | VERIFIED (raw API); the TL;DR's "archived 2025" was wrong (2025-03-15 is the last release) |
| Material: charts are not mirrored; progress bars follow reading direction | m2.material.io (browser page text, read twice: first pass, and again 2026-10-17 ~15:15 CDT via `document.body.innerText` after the assessor could not load it). The mdui.org mirror is the same source, not a second one | VERIFIED-VERBATIM (one source) |
| Flags represent countries, not languages | hilton.org.uk (curl) | VERIFIED-VERBATIM |
| "Never use CSS to apply the base direction" | w3.org/International/questions/qa-html-dir (curl) | VERIFIED-VERBATIM |
| Plex Sans, Plex Sans Arabic and Plex Sans Devanagari share x-height 0.516 | collector C's cmap/OS2 parse | Single measurement, not re-run; measures bundled Latin only |
| Plex is a model-steered font choice | [A2] TYPOGRAPHY_PROMPT, "Technical: IBM Plex family, Source Sans 3" (curl of the .ipynb) | VERIFIED-VERBATIM (cold assessment, re-checked) |
| Atkinson Hyperlegible Next is Latin-only | collector C's cmap + fontsource subsets (latin, latin-ext) | Two reads of ONE upstream (Fontsource's Google packages are built from google/fonts), not two independent methods |
| CJK webfont cost: Noto Sans SC/TC 341,740 / 445,048 B for the zh-CN / zh-TW UI strings at weight 400 | my script over the Fontsource API and woff2 downloads into memory (app.js at 145c8af) | Computed |
| Windows 11 ships Microsoft YaHei, Microsoft JhengHei, Malgun Gothic | learn.microsoft.com Windows 11 font list (curl + grep); canvas probe on this machine | VERIFIED (raw page) + observed |
| iOS/macOS: Apple SD Gothic Neo is a system font; PingFang SC/TC and Heiti (iOS) are "downloadable" | developer.apple.com/fonts/system-fonts (curl, parsed) | VERIFIED (raw page); what "downloadable" means for Safari rendering is UNVERIFIED |
| Android picks the CJK face by `lang`: families zh-Hans, zh-Hant, ko | AOSP fonts.xml (raw, main) | VERIFIED (raw file) |
| Chromium maps zh-TW to Traditional Han and zh / zh-CN to Simplified | locale_to_script_mapping.cc and layout_locale.cc (raw, main) | VERIFIED (raw source) |
| `:lang(zh-Hans)` does not match `lang="zh-CN"` | Selectors 4 (RFC 4647 extended filtering) on w3.org (curl) | VERIFIED (spec text) + reasoning from RFC 4647's rule |
| Noto Sans includes Devanagari; Plex Sans has Vietnamese and Cyrillic | api.fontsource.org subsets (curl) | VERIFIED (raw JSON) |

## 9. Numbers register

| Number | What it claims | Source | Date | Interest class | Verdict |
|---|---|---|---|---|---|
| 37,009 / 6,761 B | Web Awesome native.css, raw / gzip | jsdelivr dist-cdn, measured | 2026-10-17 | INDEPENDENT (my measurement) | measured |
| 136,349 / 16,051 B; 0 logical / 346 physical | GOV.UK Frontend CSS | jsdelivr, measured | 2026-10-17 | INDEPENDENT | measured twice (me, collector B) |
| 526,999 / 60,480 B; 15 / 2,446 | USWDS CSS | jsdelivr, measured | 2026-10-17 | INDEPENDENT | measured twice |
| 278,132 / 29,505 B; 0 / 587 | NHS.UK frontend CSS | jsdelivr, measured | 2026-10-17 | INDEPENDENT | measured |
| 83,319 / 11,617 B; 16 / 39 | Pico CSS | jsdelivr, measured | 2026-10-17 | INDEPENDENT | measured twice |
| 31,287 / 7,064 B | Oat CSS | jsdelivr, collector B | 2026-10-17 | INDEPENDENT | measured once |
| 52,182 / 16,826 B | htmx min.js | jsdelivr, collector B | 2026-10-17 | INDEPENDENT | measured once |
| 55,891 / 19,895 B | Alpine cdn.min.js | jsdelivr, collector B | 2026-10-17 | INDEPENDENT | measured once |
| 22,588 B | Plex Sans Latin 400 woff2 | fontsource via jsdelivr | 2026-10-17 | INDEPENDENT (collector measurement) | measured once |
| 42,848 / 44,280 B | Plex Sans Arabic 400 / 700 | same | 2026-10-17 | INDEPENDENT | measured once |
| 77,448 B | Plex Sans Devanagari 400 | same | 2026-10-17 | INDEPENDENT | measured once |
| 48,840 / 165,960 B | Noto Sans Arabic static 400 / variable | same | 2026-10-17 | INDEPENDENT | measured once |
| 0.516 / 0.698 | Plex x-height / cap-height across three scripts | google/fonts binaries | 2026-10-17 | INDEPENDENT | single measurement |
| 94% vs 72% | Civilla form completion, after vs before | GovTech | 2018 | VENDOR-SELF-REPORTED (agency + designer) | RAW by collector |
| 90% / 90% | Civilla pilot: confident alone / done in under 20 min | Core77 award entry | n.d. | VENDOR-SELF-REPORTED | RAW by collector |
| All ratios in section 6 | WCAG contrast | my script | 2026-10-17 | INDEPENDENT (computed) | computed; all 31 reproduced exactly by the cold assessor |
| 2.74:1; 9.43:1; 1.30:1; 1.12:1 | rule on desk; ink on focus gold; gold on highlighter; highlighter on desk | my script (re-run) | 2026-10-17 | INDEPENDENT (computed) | computed |
| 2,382,648 B (97) / 2,270,144 B (104) | Noto Sans SC / TC, all numbered slices at 400 (count) | Fontsource API + woff2 sizes, my script | 2026-10-17 ~15:07 CDT | INDEPENDENT | computed |
| 341,740 B (11) / 445,048 B (12) | Noto Sans SC / TC slices needed for the zh-CN / zh-TW UI strings at 400 | same; app.js at 145c8af | same | INDEPENDENT | computed; a reading, app.js is changing |
| 5,654,132 B (216) / 4,327,152 B (206) | Plex Sans SC / TC split Regular woff2, all files | jsDelivr file listing for @ibm/plex-sans-sc 1.1.0 / -tc 1.1.1 | same | INDEPENDENT | computed |
| 436,732 B (11) / 1,764,548 B (80) | Plex Sans SC / TC slices needed for the zh-CN / zh-TW UI strings | IBM split CSS unicode-ranges + file listing, my script | same | INDEPENDENT | computed |
| 3,813,972 / 2,496,872 B | Plex Sans SC / TC Regular, complete woff2 | jsDelivr file listing | same | INDEPENDENT | read |
| 123,861,375 / 86,503,216 B | @ibm/plex-sans-sc / -tc unpacked | npm registry | same | INDEPENDENT | read |
| 1,106,632 B (92); median 12,480 B | Plex Sans KR slices at 400 | Fontsource, my script | same | INDEPENDENT | computed; replaces "about 17 KB each" |
| 229 / 232 | distinct characters above U+2E7F in app.js zh-CN / zh-TW strings | my script, app.js at 145c8af | 15:07 CDT | INDEPENDENT | computed; a reading |
| 15,734 / 29,370 B | lit-core.min.js / lit-all.min.js from lit/dist on GitHub | curl via jsDelivr gh | 2026-10-17 | INDEPENDENT | measured |
| 691 / 317 / 2,964 / 8,537 / 2,754 B | the 5 extra Web Awesome files (layers, size, variants, palettes/default, palettes/base) | curl, 3.14.0 | 2026-10-17 | INDEPENDENT | measured |

**Interest concentration.** The load-bearing numbers are all my own or the
collectors' measurements and computations: sizes, property counts, contrast
ratios, font metrics. The vendor-reported numbers (Civilla) are context, not
load-bearing.

**Same-source dependency.** The AI-tell list leans on two Anthropic
documents, [A1] and [A2]: 7 of 12 tells and 3 of 5 "Strong" ratings
(counted by the cold assessor). They are one organisation's view, that
organisation makes a model that generates UIs, and this brief was written
by that model. This is now stated in the TL;DR. NN/g is independent
corroboration for one tell. shadcn is NOT: its post is about default
sameness and does not mention AI. Other pairs that looked independent but
share one source: Fontsource subsets and google/fonts cmap reads (same
upstream); the Plex x-height and METADATA (same repo); Material m2 and the
mdui.org mirror (same text).

## 10. Thin / missing

- **No evidence on which visual direction these judges or users trust
  more.**
  - Nobody has published a test of document-style vs consumer-brand health
    UI with low-income, limited-English families.
  - Collector A searched: GOV.UK completion, trust and "one thing per
    page"; NN/g and Baymard on plain-language forms.
  - Only GDS's qualitative recognition finding exists.
- **No source ties any visual style to better charity-care uptake.** The
  Aspen Institute 2026 screener report (FETCH snippet) says no one has
  systematically evaluated which screener design features work.
- **No documented "per-field image crop beside the OCR field" pattern.**
- **No primary source for the Tailwind indigo-500 origin of AI purple.**
  - Searches: "Adam Wathan sorry bg-indigo-500", "Wathan indigo-500 sorry
    tweet August 2025".
  - Only secondhand sources exist (prg.sh, DEV posts).
- **No accessibility conformance report** for Web Awesome, Oat, Pico,
  Material Web, Carbon, Lion or Fluent. Web Awesome has a commitment
  statement only (FETCH).
- **UNVERIFIED (could not be settled in this pass):**
  - how iOS Safari renders `font-family: "PingFang SC"` when Apple lists
    PingFang as "downloadable"; Chinese and Korean on a real iPhone and a
    real Android phone (only Windows was rendered);
  - Web Awesome native.css on a real RTL phone;
  - the Font Awesome Free licence terms for the 3 SVGs inside native.css
    (fontawesome.com/license/free is script-rendered; curl returned no
    licence text);
  - the 700-weight CJK webfont sizes (only 400 measured), and the size of
    a UI-strings-only subset (needs fontTools, not installed by rule);
  - layout of the real app at 320px CSS width (only the mocks were
    checked);
  - Plex x-height (never re-run), web-features Baseline dates, the
    Civilla figures, the Incode quotes, Canada.ca, the USWDS ACR and the
    Web Awesome accessibility statement (the cold assessor could not
    re-check these; they keep their section 8/9 verdicts);
  - all build-hour estimates (judgments).
- **Raised by the cold assessment and NOT researched (one collection round
  only):**
  - comprehension of percentage tables by low-literacy and low-numeracy
    readers;
  - line height and stacking for Devanagari and Vietnamese diacritics;
    CJK `line-break` / punctuation rules; Devanagari layout (W3C ilreq);
  - faux-bold risk for CJK at weights the system face lacks (700 chosen
    to reduce it; not tested on iOS/Android);
  - the IRS 501(r) Plain Language Summary that hospitals publish, as a
    model for the Result screen;
  - Section 1557 language-access tagline practice;
  - a "not affiliated with the hospital" notice, since D1 imitates a
    hospital document;
  - screen-reader behaviour (`<mark>` is not announced; the mock now uses
    row headers and `aria-current`, untested with a reader).
- **Listed but never cited:** W3C alreq (section 12; the digits decision
  came from Node Intl) and Shin et al. (a risk-analysis paper, not used in
  the body).
- **Not readable:**
  - flagsarenotlanguages.com (boilerplate only);
  - Stripe Identity capture docs (found only a support FAQ);
  - the Michigan DHHS press release (403).

## 11. What would change this conclusion

- **If the restyle is not passing its done-check by 21:00 CDT** (this
  replaces "if the 5:00 PM gate slips"; the gate passed at 14:53 CDT),
  revert to the last good commit and ship about 1.5 hours of work instead:
  - the `cite()` bidi fix;
  - the Plex fonts;
  - the answer-first Result hierarchy.
- **If the engine/API change for the tier rows is refused,** use option B
  in section 7: a policy table hard-coded from the synthetic policy,
  labelled as such. Direction 2's bar needs the same data.
- **If Evan wants no font with an AI-prompt association,** swap Plex for
  Noto Sans + Noto Sans Arabic (Noto covers Devanagari; Arabic 400 is
  48,840 B vs Plex Arabic's 42,848 B). Layout and tokens are unchanged.
- **If the demo iPhone does not render Chinese in PingFang,** nothing
  breaks (the stack falls through to the system fallback), but check that
  glyphs appear; if not, vendor Noto Sans SC slices (option B in 5.4) for
  zh-CN only.
- **If an A/B with attendees shows Direction 3 understood faster,** switch to
  it. UX is scored on "can a new user understand it quickly", not on
  credibility.
- **If Web Awesome native.css misrenders RTL form controls on a real phone,**
  swap to Oat's CSS, or hand-write about 150 lines on Open Props tokens.

## 12. Sources (all accessed 2026-10-17)

**AI-slop tells**
- [A1] Anthropic, frontend-design SKILL.md (last commit 2026-09-02): https://raw.githubusercontent.com/anthropics/claude-code/main/plugins/frontend-design/skills/frontend-design/SKILL.md
- [A2] Anthropic cookbook, Prompting for frontend aesthetics (last commit 2026-02-17, per the cold assessor's `gh api`): https://github.com/anthropics/claude-cookbooks/blob/main/coding/prompting_for_frontend_aesthetics.ipynb
- [N1] NN/g, The Proliferation and Problem of the Sparkles Icon (2024-09-20, modified 2025-09-19): https://www.nngroup.com/articles/ai-sparkles-icon-problem/
- [S1] shadcn changelog (2025-12): https://ui.shadcn.com/docs/changelog/2025-12-shadcn-create
- Impeccable, craft floor (undated): https://raw.githubusercontent.com/pbakaus/impeccable/main/.agent/skills/impeccable/reference/craft-floor.md
- prg.sh, purple gradient (2025-10-26): https://prg.sh/ramblings/Why-Your-AI-Keeps-Building-the-Same-Purple-Gradient-Website
- Superdesign (2026-07-13): https://superdesign.dev/blog/fix-generic-ai-landing-page
- Creative Boom (2026-04-21): https://creativeboom.com/insight/10-trends-creatives-are-so-over-in-2026/
- Shin et al., arXiv 2603.13036 (2026-03-13): https://arxiv.org/abs/2603.13036

**Exemplars and trust evidence**
- GOV.UK Design System (colour, typeface, question pages, check answers, confirmation pages, file upload, accessibility statement): https://design-system.service.gov.uk/
- GDS blog (2024-01-12): https://gds.blog.gov.uk/2024/01/12/how-were-making-it-easier-to-access-government-forms-online/
- GDS design notes, one thing per page (2015-07-03): https://designnotes.blog.gov.uk/2015/07/03/one-thing-per-page/
- USWDS (color overview, file input, accessibility): https://designsystem.digital.gov/
- NHS.UK care cards: https://service-manual.nhs.uk/design-system/components/care-cards
- Canada.ca typography and colours: https://design.canada.ca/
- Civilla, Project Re:form: https://designawards.core77.com/Service-Design/86102/Project-Re-Form and https://www.govtech.com/civic/a-blueprint-for-human-centered-change.html (2018)
- Klim, Oscar Health: https://klim.co.nz/in-use/oscar-health/

**Component sources and architecture**
- uswds#5336: https://github.com/uswds/uswds/issues/5336
- govuk-frontend#7303: https://github.com/alphagov/govuk-frontend/issues/7303
- govuk-frontend PR #7465: https://github.com/alphagov/govuk-frontend/pull/7465
- Web Awesome localization: https://webawesome.com/docs/localization ; package @awesome.me/webawesome@3.14.0 on jsdelivr
- Oat: https://github.com/knadh/oat ; Pico: https://github.com/picocss/pico ; Shoelace: https://github.com/shoelace-style/shoelace
- Packages on cdn.jsdelivr.net (versions as in sections 5.3 and 5.6): USWDS, GOV.UK Frontend, NHS.UK frontend, Open Props, Material Web, Carbon, Lion, Fluent, htmx, Alpine, Lit
- Lit single-file bundles: https://cdn.jsdelivr.net/gh/lit/dist@3/core/lit-core.min.js
- Project files: `HANDOFF.md`, `docs/2026-10-17_pre-mortem.md`, `.claude/project-memory/experiments.md`, `app/static/app.js`, `app/engine.py`, `app/data/policy_cumberland_synthetic.json`
- web-features dataset v3.43.0 (Baseline): https://cdn.jsdelivr.net/npm/web-features/data.json

**Typography**
- Fontsource API: https://api.fontsource.org/v1/fonts/<id>
- google/fonts METADATA: https://github.com/google/fonts
- IBM Plex: https://github.com/IBM/plex ; npm @ibm/plex-sans-sc and @ibm/plex-sans-tc
- W3C clreq system font mappings (verified 2026-09-03): https://w3c.github.io/clreq/others/system-font-mappings.html
- web.dev, font best practices: https://web.dev/articles/font-best-practices
- MDN (font-display, print-color-adjust, break-inside): https://developer.mozilla.org/
- W3C alreq, Arabic numerals draft (listed, not cited): https://github.com/w3c/alreq/wiki/Arabic-numerals-(Draft)
- npm registry, @ibm/plex-sans-sc / -tc / -kr latest: https://registry.npmjs.org/@ibm/plex-sans-sc/latest
- jsDelivr package listings (file sizes): https://data.jsdelivr.com/v1/packages/npm/@ibm/plex-sans-sc@1.1.0?structure=flat (and plex-sans-tc@1.1.1)
- Fontsource API, noto-sans-sc, noto-sans-tc, noto-sans-kr, ibm-plex-sans-kr: https://api.fontsource.org/v1/fonts/noto-sans-sc
- Microsoft, Windows 11 font list: https://learn.microsoft.com/en-us/typography/fonts/windows_11_font_list
- Apple, System Fonts: https://developer.apple.com/fonts/system-fonts/
- AOSP fonts.xml (main): https://android.googlesource.com/platform/frameworks/base/+/refs/heads/main/data/fonts/fonts.xml
- Chromium, locale_to_script_mapping.cc and layout_locale.cc (main): https://github.com/chromium/chromium/tree/main/third_party/blink/renderer/platform/text
- W3C Selectors Level 4, :lang(): https://www.w3.org/TR/selectors-4/

**Screen patterns**
- Material Design, bidirectionality: https://m2.material.io/design/usability/bidirectionality.html
- Wikimedia Codex, bidirectionality: https://doc.wikimedia.org/codex/main/style-guide/bidirectionality.html
- W3C i18n, base direction: https://www.w3.org/International/questions/qa-html-dir
- W3C i18n, language navigation: https://www.w3.org/International/questions/qa-navigation-select
- Peter Hilton, language selection (2020-11-03): https://hilton.org.uk/blog/language-selection
- Incode, OCR review design: https://developer.incode.com/design-and-ux/ocr-review-design/

**Icons** (licenses read from package.json)
- @phosphor-icons/core 2.1.1, MIT
- @tabler/icons 3.49.0, MIT
- @material-symbols/svg-400 0.48.0, Apache-2.0

## 13. Cold assessment (stage 10.5)

Run 2026-10-17 ~15:00-15:12 CDT by a fresh general-purpose agent that got
only this file's path, the companion HTML path and the six stage-10.5
questions (plus "list wrong claims" and "list inconsistencies"). It had not
seen the collection transcript. It edited nothing. It used curl, `gh`,
node, one WebFetch and one browser read. Every finding below marked
"confirmed" I re-fetched myself by a different call before changing the
brief (one collection round, then stop, per the skill).

**Q1 - claims that look independent but share a source.**
- Atkinson "two methods agree" = cmap + Fontsource, but Fontsource's
  Google packages are built from google/fonts: one upstream. (Accepted;
  section 8 relabelled.)
- Plex x-height and the METADATA designer credit: both from google/fonts.
  (Accepted.)
- Material m2 + the mdui.org mirror: one text. (Accepted.)
- [A1] + [A2]: one organisation; disclosed only in section 9. (Accepted;
  moved to the TL;DR.)

**Q2 - source-interest concentration.** 7 of 12 tells and 3 of 5 "Strong"
ratings rest on Anthropic; the author is an Anthropic model and [A1] is in
its own toolset; [S1] is a product launch that never mentions AI; Web
Awesome's RTL verdict rests on vendor docs. Not disclosed up front.
(Accepted: TL;DR "Source caveat"; tell 11 downgraded to Medium; Web Awesome
"Ready" downgraded.)

**Q3 - hypothesis never given a chance to die: H4b.** [A2]'s typography
prompt lists "IBM Plex family" among the fonts it steers the model toward;
the brief had read [A2] but not quoted this. Confirmed by curl. Result:
the "distinctive" half of H4b died; Plex is kept for coverage only. Runner
up: H1, where counter-evidence (low-literacy table comprehension; GDS
testers preferring web forms to "document-based versions") was never
sought. The GDS line was confirmed by curl and added to 5.2 and section 3;
the literacy question is listed in section 10 as not researched.

**Q4 - source types named but not run.** No glyph-coverage table (promised
in section 4); the x-height was never re-read; W3C alreq listed but never
cited; no Devanagari layout source (ilreq). (Accepted: section 4 now says
so; section 10 lists them.)

**Q5 - what a domain expert would call missing.** OS/2 x-height in the
Arabic and Devanagari files measures bundled Latin, so "matched metrics"
says nothing about Arabic or Devanagari harmony; the policy table is
English-only in Arabic; forced-colors mode drops the row cue; screen
readers get no row headers, caption or current-row marker; the highlighter
is 1.12-1.27:1 on a projector; gold focus on highlighter is 1.30:1; reflow
should be tested at 320px; `:lang(zh-Hans/zh-Hant)` will not match the
app's `zh-CN`/`zh-TW` (found independently in my CJK revision too); faux
bold on CJK; no CJK `line-break` rules; no Devanagari/Vietnamese line
height; no 501(r) Plain Language Summary, "not affiliated" notice or
Section 1557 tagline practice; `ar-SY`, `ar-IQ`, `ar-YE` (and, on my
re-run, `ar-LB`, `ar-JO`) default to Arabic-Indic digits. (Fixed in the
brief and mock: metrics wording, forced-colors block, row headers and
`aria-current`, focus note, 320px in the done-check, `:lang()` tags, weight
700, digits wording. Listed in section 10 as not researched: line-break,
Devanagari/Vietnamese line height, 501(r), 1557, "not affiliated",
literacy, screen-reader test.)

**Q6 - more confidence than the verdict supports.** Plex "matched metrics"
(single, un-re-run measurement, stated unhedged in the recommendation);
Web Awesome "Ready" (the quoted docs cover components the plan does not
load). (Accepted: both downgraded.)

**Spot-checks the assessor found WRONG; all confirmed by my re-fetch:**
1. Pico "archived 2025": archived after a push on 2026-10-04 (`gh api`);
   2025-03-15 is the last release.
2. Lit "no single-file build ships": `gh/lit/dist@3` bundles return 200
   (15,734 and 29,370 B, curl).
3. "Single designer credit in METADATA": Plex Sans Arabic credits four
   names (curl of METADATA.pb).
4. "Vendor 3 Web Awesome files": 7 are needed (curl of the `@import`s).
5. Web Awesome "MIT" is incomplete: native.css embeds 3 Font Awesome Free
   7.0.0 SVGs under a separate licence (grep). Licence terms UNVERIFIED.
6. Tell 5 quote scope: "reads as a tell" refers only to #D97757 (SKILL.md
   line 39); "anti-purple" is not in the source.
7. "Avoids every tell": [A1] also lists tinted near-black (D1's ink is
   one) and single-word headline accents (D3's underline is one); both
   were omitted from 5.1. Now tell 4 and new tell 13.
8. shadcn as AI corroboration: the post does not mention AI.
9. Minor: [A2] last commit 2026-02-17 (not "undated"); "Cliched" lacks the
   source's accent (kept ASCII, noted); `app.js` is 371 lines at 145c8af;
   `cite()` puts three translated words in the LTR run, not two.

**Assessor could not settle** (left as is, listed in section 10): Plex
x-height; web-features Baseline dates; Civilla figures; Incode quotes;
Canada.ca; USWDS ACR; Web Awesome accessibility statement. Material m2
quotes: it could not load the page; I re-read it in the browser pane
(`document.body.innerText`, 2026-10-17 ~15:15 CDT): "Charts and graphs",
"Untranslated text (even if it's part of a phrase)" and "Progress bars
fill in the same direction as content is read" are all present.

**Assessor-verified as correct:** all 31 contrast ratios; the GOV.UK,
USWDS, Pico and Web Awesome byte and property counts (within ~15 B);
Web Awesome MIT and its translation list; USWDS #5336 and the 2026-09-18
quote; govuk-frontend #7303 and PR #7465 (note: #7303 covers only the
details component); the [A1], [A2], NN/g, shadcn, GDS, W3C and Hilton
quotes; the font file sizes; clreq's date and its PingFang label.

**Internal inconsistencies it found, and the fix:**
- Brief vs HTML, D1 highlighter "only on the deadline" vs "two places":
  HTML fixed to two places.
- D1 weights 400/600 vs mock 700: brief changed to 400/700.
- Phone scale 16/19/23/28 vs mock 12.5-14.4 px text: 14 px added to the
  scale; mock text set to 14/16/19/23 px.
- "No shadows" / "no gradients" vs the mock's inset box-shadow bar and
  gradient mark: mock now uses a border and a flat fill.
- D1 "Signals trust to" omitted the HCA director in the HTML: added.
- Step bar borrowed but not drawn in the D1 mock: noted in the brief and
  the mock label (not drawn).
- Tap targets 48 vs 44 px: unified at 48 px.
- Widths 360 / 375 / 390 px: done-check now 320 px and 375 px.
- Lead flaw's "style.css + markup only" could not deliver the signature
  (needs tier rows): now an explicit decision (section 7, options A/B).
- `zh-Hans` advice missing from the build plan: replaced by `:lang(zh-CN)`
  / `:lang(zh-TW)` and added to section 7.
- Token pairs without ratios: rule on desk (2.74:1) added with a usage
  limit; unused D1 `--ok` removed from the mock. NOT fixed (non-recommended
  directions): D2 river-tint #E1F3F8 and button edge #0E3A1F, D3 mint
  #DCEFE8 have no computed ratios; D2's pin relies on an inline `left:23%`
  override in RTL; D3's underline is a box-shadow despite "No shadows".

**Side effect reported by the assessor:** it navigated the shared browser
pane to m2.material.io once; no work was lost (I reloaded my scratch page).

## 14. Change log (append-only; 2026-10-17, CDT)

15:11 - Fact change (a): the 5:00 PM gate passed at 14:53 CDT; live at
http://207.211.181.174/. Rewrote the TL;DR lead flaw, section 1 (pessimistic
angle, time left), section 7 (timing, 21:00 go/no-go, T5 deploy check) and
section 11 (first bullet). Freeze read as about 23:00 CDT tonight, Sat
2026-10-17 (HANDOFF and pre-mortem say "Sat 23:00").

15:11 - Fact change (b): tiers are now tier 1 en, es, ar, zh-CN, zh-TW;
tier 2 vi, fr, ko, ru, de, hi. Rewrote the question, section 1 constraints,
the 5.4 CJK strategy (options table with measured sizes; system-font
decision; per-language stacks; Android/Chromium tag mapping; Korean check),
D1 type, section 7 files and done-check, sections 8-10 rows.

15:11 - Corrections found during the CJK work: Plex Sans KR slices are
median 12,480 B, not "about 17 KB"; IBM's Plex SC/TC packages do ship split
woff2 (the "use system fonts" conclusion stands, now priced); `:lang(zh-
Hans)` would not match the app's `zh-CN`; the Korean font names are now
verified; Apple lists PingFang as "downloadable" on iOS and macOS.

~15:20 - Stage 10.5 findings applied (section 13): TL;DR source caveat and
Plex hedge; Pico date; Lit row; Plex METADATA; Web Awesome 7 files, file
sizes and Font Awesome SVG licence note; Web Awesome "Ready" downgraded;
tell 4 near-black added; tell 5 scope; tell 11 downgraded; tell 13 added;
H4b "distinctive" died; H1 counter-signal; Arabic digits list; recommendation
points 2 and 3 rewritten; D1 tokens (rule on desk, focus gold), weights
400/700, 14 px step, forced-colors, table semantics, 48 px targets, 320 px
reflow, "not affiliated" risk; build cost 5.5 -> 6.0 h (A) / 5.5 h (B);
section 8 verdicts relabelled; section 9 new rows; section 10 UNVERIFIED and
not-researched lists; section 11 two new bullets; section 12 new sources;
section 4 notes on the missing coverage table and the un-re-run x-height.

~15:20 - Companion HTML: added the zh-CN Paper Trail Result mock (system
CJK stack, policy table in English, SYNTHETIC DEMO badge, strings reused
from `app.js` zh-CN where they exist); filled the three "Intended type"
boxes; D1 signature text; D1 trust line; D1 tokens and sizes; table
semantics; flat mark; border row bar; forced-colors block; real last-band
label. Checked in the desktop app's Chromium (152, Windows 11), page
served from a scratch copy: at 375x812, no horizontal scroll, every phone
frame 341 px with no overflow, zero network resource entries, Arabic line
height 1.7 applied, D1 h3 23 px and notes 14 px, all three D1 tables have 4
row headers and an `aria-current` row; at 320x700, no page scroll and the
D1 tables fit (226/228 px). The zh-CN mock was inspected in a screenshot.
- 2026-10-17 16:57 CDT (audit, record Z/AA) - Errata (from record W and the audit): Web Awesome needs 13 CSS
  files, not the 7 this brief lists (sections 5.3, Direction 1, verification);
  Plex Devanagari and Arabic load for every visitor, not "only for Hindi",
  because the language buttons show those scripts; section 5.1 now has 13
  tells, not 12; native.css is 37,010 B and themes/default.css 16,773 B on disk.
