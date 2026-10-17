# ui - TNHacks26

- 2026-10-17 - No UI yet. Accessibility is named in the track's responsible-innovation list; design it in from the start. Arabic needs right-to-left layout.
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
