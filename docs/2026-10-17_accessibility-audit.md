# Accessibility audit - Bill to Help (Paper Trail UI)

- **Date:** 2026-10-17, ~15:58-16:00 CDT
- **Build audited:** commit c689291 (the live UI at the time), served locally
  in FAKE_OCI mode (same HTML/CSS/JS as the server)
- **Tool:** axe-core 4.14.0 (MPL-2.0), downloaded from jsDelivr with a
  sha256 check, run in the desktop browser pane (Chromium), never deployed
- **Rule tags:** wcag2a, wcag2aa, wcag21a, wcag21aa, wcag22aa, best-practice
- **Viewport:** 375 x 812 CSS px (phone width)
- **Who ran it:** Claude (Opus 5.5)

## Result

**0 critical, 0 serious, 0 moderate, 0 minor violations on the 5 app
screens in English and Arabic (10 audits). The printable packet page has
2 moderate violations.**

| Screen | English | Arabic (RTL) |
|---|---|---|
| 1 Start | 0 | 0 |
| 2 Bill (fields confirmed) | 0 | 0 |
| 3 Three questions | 0 | 0 |
| 4 Result | 0 (47 rules passed, 0 needing review) | 0 |
| 5 Packet screen (app chrome) | 0 | 0 |
| Packet page itself (the printable letter) | 2 moderate | 2 moderate + 1 to check by hand |

**Check that axe really ran:** on the Result screen, 47 rules passed and 44
did not apply. A planted `<img>` without `alt` was reported as `image-alt`,
**critical**, then removed.

**Packet page:** it is shown in a sandboxed iframe with scripts off, so axe
cannot run inside it. It was audited by loading the same HTML (from
POST /packet) as its own page.
- `landmark-one-main` (moderate, 1 node): the page has no `<main>`.
- `region` (moderate, 17 nodes): content sits outside any landmark.
- Arabic only: 1 `color-contrast` item axe could not decide (text over a
  background it cannot measure). It needs a manual check.

Fix for both moderate items: wrap the packet body in `<main>` in
`render_packet_html()` (`app/main.py`). It is not applied yet: the plan
only allowed fixes to critical or serious items in `app/static/`.

## What this audit does NOT cover

- Screen readers (NVDA, VoiceOver, TalkBack): not tested.
- Real phones: not tested (pre-mortem T3). Browser zoom and text resize
  were not tested.
- Keyboard-only walk-through: not done by hand; focus styles were only
  checked in code (`:focus-visible` ring in style.css).
- Cognitive load and plain-language quality, including the AI-written
  explanations: axe cannot judge these.
- Translation quality: see the reviewer screenshots (Arabic, Simplified
  and Traditional Chinese).

## Problems found by looking, not by axe (same session)

axe passed these; they were seen on the reviewer screenshots.
1. **Misleading tick:** each bill field shows a decorative check icon next
   to the real checkbox. It looks ticked even when the field is not
   confirmed.
2. **RTL inputs:** English values in Arabic-page inputs (for example the
   hospital name) are right-aligned, so the start of the text is cut off.
   They need `dir="ltr"` or `dir="auto"`.
3. **RTL English paragraphs:** the deadline sentence and the document names
   are English inside Arabic paragraphs, so the footnote markers land
   mid-sentence. They need `dir="ltr"` on those paragraphs.
4. **Packet at phone width:** the English and translated letters sit side
   by side and the translated column overflows (351 px of content in a
   276 px column).
5. **Translation of the hospital name:** OCI Language turned "(SYNTHETIC)"
   into "(MONOETIC)" (Arabic, Traditional Chinese) and "CETIC" (Simplified
   Chinese). The number lock cannot catch words.
6. **zh-TW letter:** it dropped "Financial Assistance Office" from the
   greeting.
7. **Ambiguous source text:** "this application" was translated as "this
   app" in all three languages.
