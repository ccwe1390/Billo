# ui - TNHacks26

- 2026-10-17 - [SUPERSEDED: the 5-screen UI is built and live] No UI yet. Accessibility is named in the track's responsible-innovation list; design it in from the start. Arabic needs right-to-left layout.
- 2026-10-17 - Website-profile rows that apply (project-memory
  profiles/website.md): keep approved wireframes/mockups dated in
  `docs/design/`; keep an asset inventory WITH a license per asset (fonts for
  Arabic/Chinese/Vietnamese included); keep the actual accessibility audit
  output at demo time, dated - never just a claim of compliance.

## Hard UI rules (2026-10-17 15:24 CDT; adapted from Dipayan's
## frontend/CLAUDE.md on origin/feature/frontend, merged with our own rules)
Every screen, string and agent obeys these. A change that breaks one is a bug.
1. Never a promise: results are an *estimate*; always "the hospital makes the
   final decision". Never the word "saved" about money.
2. No medical advice, diagnosis or triage (important.md 1).
3. Never ask for name, immigration status, SSN or ID; the server rejects
   extra answer fields (AnswersIn extra="forbid").
4. Keep nothing: no localStorage/sessionStorage/cookies/IndexedDB holding
   bill or household data; state lives in memory only. (An opt-in "save to
   this phone" for the home page needs Evan's explicit OK first - PRD F9.)
5. Synthetic data only; the SYNTHETIC DEMO badge stays visible.
6. No placeholder copy ("Content pending", "TODO", lorem) on any screen;
   tests/test_api.py enforces it.
7. Policy text, citations, phone, email, dates and money stay English and
   left-to-right inside RTL pages (`dir="ltr"`, `<bdi>`).
8. Every number shown in generated or translated text passes the number
   lock, or the English template is shown with a note.
9. Loading states name the step ("Reading the bill...", "Checking the
   policy...", "Writing your explanation...", "Building your packet...").
10. Tap targets >= 48px; visible focus ring; no colour-only meaning.
11. No runtime third-party requests (fonts, icons, scripts are vendored);
    no tracking or analytics.

## Asset inventory with licenses (2026-10-17 15:29 CDT)
All fetched from cdn.jsdelivr.net (npm mirror) with Evan's OK; every file's
sha256 and size checked against jsDelivr's package listing; no runtime
third-party requests.
| Asset | Version | Files | Bytes | License | Where |
|---|---|---|---|---|---|
| Web Awesome element styles | @awesome.me/webawesome 3.14.0 | 13 CSS (native.css, themes/default.css and their full @import graph) | 104,458 | MIT (LICENSE.md). native.css embeds 3 Font Awesome Free 7.0.0 SVGs under fontawesome.com/license/free - terms not read (page needs JS); UNVERIFIED | app/static/vendor/webawesome/ |
| IBM Plex Sans | @fontsource/ibm-plex-sans 5.3.0 | 8 woff2 (latin, latin-ext, vietnamese, cyrillic x 400/700) | 123,384 | OFL-1.1 | app/static/fonts/ |
| IBM Plex Sans Arabic | @fontsource/ibm-plex-sans-arabic 5.3.0 | 2 woff2 (400/700) | 87,128 | OFL-1.1 | app/static/fonts/ |
| IBM Plex Sans Devanagari | @fontsource/ibm-plex-sans-devanagari 5.3.0 | 2 woff2 (400/700) | 151,580 | OFL-1.1 | app/static/fonts/ |
| Phosphor icons (regular) | @phosphor-icons/core 2.1.1 | 6 SVG (camera, check, calendar, file, printer, globe) | 2,927 | MIT | app/static/icons/ |
- fonts/fonts.css (written by Claude) maps all 12 faces to one family
  'BillPlex' with Fontsource's unicode-range values.
- The design brief said Web Awesome needs 7 files; following the @import
  graph showed 13 (color/variants.css and 5 variant files were missing).
- Chinese and Korean: system fonts, nothing vendored.
- 2026-10-17 16:50 CDT - `docs/design/` was never created. Mockups live in
  docs/research/2026-10-17_design-directions.html; the dated accessibility
  audit is docs/2026-10-17_accessibility-audit.md. Use those paths.

## 2026-10-17 19:21 CDT - UI port: new design system (record AF, commit efe50f0)
- Design system = Dipayan's feature/frontend tokens (PR #1) ported into
  app/static: dark theme = his palette, light theme derived in the same
  tokens (contrast computed: text >= 4.5, non-text >= 3); the phone's
  prefers-color-scheme picks, a header toggle (Auto/Light/Dark) overrides
  in page memory only. Component contract: plan in record AF.
- Web Awesome: NO page loads it since efe50f0 (files kept on disk under
  app/static/vendor/webawesome/; the 15:29 table row above is history).
- Base size 17px (html 106.25%); controls 3rem = 51px, so rule 10 (>= 48px)
  still holds. Focus ring 3px solid --ring, offset 2px, on buttons too.
- Fonts: new family 'BillScan' in fonts/fonts.css = Atkinson Hyperlegible
  (latin, latin-ext) + Plex Arabic + Plex Devanagari. 'BillPlex' (all 12
  Plex faces) is kept for :lang(vi) and :lang(ru), which Atkinson lacks.
| Asset | Version | Files | Bytes | License | Where |
|---|---|---|---|---|---|
| Atkinson Hyperlegible | @fontsource/atkinson-hyperlegible 5.3.0 | 4 woff2 (latin, latin-ext x 400/700) + LICENSE | 53,488 | OFL-1.1 (Braille Institute) | app/static/fonts/ |
| qrcode-generator (missing from the 15:29 table; added 2026-10-17 F10) | 2.0.4 | dist/qrcode.js + LICENSE | 56,694 (js) | MIT | app/static/vendor/qrcode-generator/ |
  Hashes for both: NOTICE.md.
