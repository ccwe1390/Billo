# Frontend context (handoff from claude.ai planning chat)

## Project
Hackathon project for Oracle Hackathons International, track #2 "Health Access, Equity & Experience" (TNHacks26).
The app helps immigrants and low-income patients, and the family member (often an adult son or daughter) who reads bills for them, understand hospital bills in their own language and spot charges that look wrong before paying. **It never decides anything; the person does.**

## Architecture
- **Backend:** Python (repo root: `app/`, `requirements.txt`). It owns ALL OCI calls:
  - OCI Document Understanding: OCR + table extraction, inline/synchronous only (nothing written to Object Storage)
  - OCI Generative AI: normalizes OCR text into JSON line items and writes plain-English explanations. It does NOT judge errors.
  - Deterministic rules engine (no AI) finds the errors
  - OCI Language: translation
- **Frontend (this folder, `frontend/`):** Vite + React + TypeScript, styled with Tailwind + shadcn/ui. My part (Dipayan). Branch: `feature/frontend`.
- The frontend **never** calls OCI directly and **never** holds keys. It only calls the Python backend API.
- Everything is hosted on OCI.

## Frontend setup status
- Done: scaffolded with `npm create vite@latest frontend -- --template react-ts` (Vite 8, Oxlint). Dev server runs at http://localhost:5173.
- In progress / verify: Tailwind v4 via `@tailwindcss/vite`; `@` alias -> `./src` in vite.config.ts, tsconfig.json, and tsconfig.app.json; `npx shadcn@latest init`; components button, card, badge, tabs, select.
- Windows + PowerShell. Run npm commands from inside `frontend/`.

## Backend API contract
NOT CONFIRMED yet. Ask the backend teammate for the exact endpoint and JSON shape. Working assumption, so the UI can be built against mock data:

`POST /audit` (multipart: `bill` file, `eob` file, `lang`) returns:
```json
{
  "billLines": [{ "date": "2026-10-02", "description": "Blood test", "code": "85025", "qty": 1, "amount": 300 }],
  "eobLines":  [{ "date": "2026-10-02", "description": "Blood test", "charged": 300, "allowed": 60, "insurancePaid": 60, "youOwe": 0 }],
  "billAmountDue": 2200,
  "eobYouOwe": 210,
  "gap": {
    "total": 1990,
    "explained": [
      { "rule": "R1", "label": "Duplicate charge", "amount": 300 },
      { "rule": "R3", "label": "Insurance discount not applied", "amount": 1690 }
    ],
    "unexplained": 0
  },
  "flags": [{
    "rule": "R1",
    "title": "Blood test listed twice",
    "amount": 300,
    "mightBeFineIf": "the test was actually done twice on that day",
    "lineRefs": [1, 2]
  }],
  "translations": { "lang": "es", "items": {} },
  "letterEnglish": "..."
}
```
The parts of the gap must always add up to the total (the UI shows this check). Anything not accounted for is shown as "unexplained — ask the hospital."

## Rules (v1)
- R1: exact duplicate line
- R2: math error (qty x price != line, or lines != total)
- R3: bill amount owed > EOB patient responsibility (for matched claims or dates)
- R4: charge on bill not on EOB
- R5: billed amount differs between bill and EOB for the same service
- R6: summary bill only, no line items (leads to an "ask for itemized bill" letter)

## UI requirements
- Mobile-first: the family member often photographs the bill on a phone.
- Upload screen: two large drop zones ("Hospital bill", "Insurance summary (EOB)") plus a language picker using native names: Español, 简体中文, 繁體中文, العربية, Tiếng Việt, and Hindi (हिन्दी) labeled "machine translation, not verified".
- Results screen:
  - Big summary card ("Your bill may be $X too high")
  - Flag cards, each with a badge, the dollar amount, and a "this might be fine if…" note
  - Side-by-side tab: English original next to the translation, with mismatched lines highlighted
  - Translated preview of the English dispute letter
- Arabic must render RTL (`dir="rtl" lang="ar"` on translated content).
- Loading states that name each step ("Reading your bill…", "Comparing with insurance…").
- Calm, trustworthy look: one accent color (teal or blue), generous whitespace, shadcn Card/Badge/Tabs, lucide-react icons.

## Hard rules
- Wording must never be a verdict. Flags are "questions to ask the billing office," never "fraud" or "this is wrong."
- No medical advice. Don't interpret diagnosis codes; show only "reason code the hospital listed."
- Never ask for immigration status, SSN, or ID.
- Keep nothing: no localStorage or sessionStorage of bill data; state lives in memory only.
- Fake/synthetic data only.
- Never commit `.env*` files.

## How the user likes to work
Step-by-step guided instructions. Explain the reasoning behind steps. Be direct and accurate.
