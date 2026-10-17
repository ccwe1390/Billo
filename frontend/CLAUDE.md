# Frontend context

Source of truth for the product: `../HANDOFF.md` and `../docs/contracts.md`. This file was rewritten 2026-10-17
to match them; the earlier "bill + EOB error checker" version (`/audit`, rules R1-R6) is SUPERSEDED and dropped.

## Project
Hackathon project for Oracle Hackathons International, track #2 "Health Access, Equity & Experience" (TNHacks26).
"Bill to Help" (placeholder name): a photo of a Nashville hospital bill becomes that hospital's financial assistance
packet: eligibility estimate against the hospital's own published policy (every rule cited), pre-filled application
fields, document checklist, deadline and cover letter, explained in the family's language, for the family member
helping a parent. **The AI reads and phrases; a rules engine decides; the family submits; the hospital decides.**

## Architecture
- **Backend:** Python FastAPI (repo root: `app/`). It owns ALL OCI calls (Command A Vision reads the bill, Command A
  phrases, OCI Language translates) and the deterministic rules engine. Run locally in fake mode:
  `$env:FAKE_OCI = "1"; py -m uvicorn app.main:app --port 8000` from the repo root (see `../README_RUN.md`).
- **Frontend (this folder):** Vite + React + TypeScript, Tailwind v4 + shadcn/ui. Owner: Dipayan. Branch: `feature/frontend`.
- **Reference implementation:** `../app/static/app.js` already does all five screens in plain JS. Port its behavior
  (field confirmation, required fields, language tiers, RTL, citations, fallback notes); don't reinvent it.
- The frontend **never** calls OCI and **never** holds keys. It only calls the backend.
- Everything is hosted on OCI.

## Frontend setup status
- Done: Vite 8 + React 19 + TypeScript 6 + Oxlint; Tailwind 4.3 via `@tailwindcss/vite`; `@` alias -> `./src`
  (vite.config.ts + `paths` in both tsconfigs, no `baseUrl`); shadcn init (style `radix-nova`, neutral, lucide,
  `rtl: true`, Geist font); components button, card, badge, tabs, select, input, label, checkbox, alert.
  `src/lib/utils.ts` re-exports `cn` from the `cn` package (shadcn's own replacement for clsx + tailwind-merge).
- To do: dev proxy to :8000 for /extract /evaluate /explain /packet; shadcn RTL direction provider
  (https://ui.shadcn.com/docs/rtl/vite) so Radix Select/Tabs behave in Arabic; accent color (teal or blue).
- Oxlint `only-export-components` warnings in `src/components/ui/*` are expected (generated files); leave them.
- Windows + PowerShell. Run npm commands from inside `frontend/`.

## Backend API (implemented in `../app/main.py`; shapes in `../docs/contracts.md`)
Rules for all shapes: money is integer cents (never floats); dates `YYYY-MM-DD`; `contract_version: 1`.

- `POST /extract`: multipart, field `file`, PNG or JPEG, max 8 MB -> **BillFields**:
  `{contract_version, fields: {hospital_name, statement_date, account_number, amount_due_cents, date_of_service,
  insurance_status}}`, each `{value, confidence, confirmed: false}`. `value: null` = unreadable: ask the user, never
  guess. `insurance_status` is `"self_pay" | "insured" | "unknown"`. 502 = photo reading unavailable: show the blank
  fields for manual entry.
- `POST /evaluate`: `{bill: BillFields, answers: HouseholdAnswers}` -> **EngineResult** (percent_of_fpl, tier with
  `eligible`, deadline, documents, contacts, every item with a `citation`). 422 if any field is unconfirmed or
  `statement_date` / `amount_due_cents` is missing.
- `POST /explain`: same body -> `{language, text_en, text, numbers_match, fallback_used, ai_written}`.
  If `fallback_used`, show English and the "did not pass the number check" note.
- `POST /packet?format=html|json`: same body -> printable HTML page (show in a sandboxed iframe) or JSON.
  422 when not eligible (no packet; show the payment-plan contact instead).
- **HouseholdAnswers:** `{contract_version, language, for_whom: "self"|"family", household_size: 1-12,
  annual_income_cents, files_tax_return: bool}`. The server rejects any extra key.

## Screens (one journey, must run in under 90 seconds)
1. **Start:** language picker (native names), "This bill is for: me / a family member", notice "Nothing you enter is
   saved. Demo uses synthetic bills only."
2. **Bill:** upload/photo; extracted fields beside the image; every field editable and must be confirmed; blank
   fields highlighted and asked for.
3. **Three questions:** household size, yearly household income, files a tax return.
4. **Result:** percent of the poverty guideline, policy tier, deadline, documents, contact, each with its citation;
   explanation in the chosen language with an English toggle; "the hospital decides"; Tennessee protections card.
5. **Packet:** the `/packet` HTML in an iframe, with Print.

## Languages
- Tier 1, translated interface: en, es, ar (RTL), zh-CN, zh-TW.
- Tier 2, English interface; only the explanation and the letter are translated: vi, fr, ko, ru, de, hi.
  Hindi is not back-checked (OCI Language has no Hindi).
- Arabic: `dir="rtl" lang="ar"`. Policy text, citations, phone and email stay English and `dir="ltr"`.
- UI strings live in `../app/static/app.js` (`T`); non-English ones are drafts for a human reviewer.

## UI look
Mobile-first (the family member photographs the bill on a phone). Calm, trustworthy: one accent color (teal or
blue), generous whitespace, shadcn components, lucide-react icons. Loading states that name the step
("Reading the bill...").

## Hard rules
- Never a promise: it is an *estimate*; "the hospital makes the final decision". Never the word "saved" for money.
- No medical advice or diagnosis.
- Never ask for name, immigration status, SSN or ID.
- Keep nothing: no localStorage/sessionStorage/cookies of bill data; state lives in memory only.
- Fake/synthetic data only.
- Never commit `.env*` files.

## How the user likes to work
Make the changes directly (edit files, run commands, verify with a build) instead of handing over instructions to
type. Briefly explain what was done and why. Be direct and accurate.
