# Billo

Turn a photo of a hospital bill into that hospital's financial assistance application.

Many Nashville hospitals will reduce or forgive bills for families under certain
incomes, but the rules are buried in long English-only PDFs, so most families
never apply. Billo reads the bill, checks the hospital's real published policy,
and builds the application packet, in 32 languages.

## What it does
1. **Read the bill**: upload a photo; AI reads the hospital, account number,
   amount due and dates. You check and confirm every field.
2. **Answer a few questions**: household size, yearly income, tax filing.
3. **See your estimate**: a rules engine compares your answers to the hospital's
   financial assistance policy (Vanderbilt and Ascension Saint Thomas). Every
   rule links to the page of the policy it comes from.
4. **Get your packet**: pre-filled application fields, document checklist,
   deadline, and a cover letter, translated into your language.

## Safety by design
- The AI only reads and translates. A tested rules engine makes the eligibility estimate.
- Every dollar amount is checked after translation; if one changes, Billo shows the English.
- Nothing is saved: no accounts, no stored photos, no ID numbers asked.
- It's an estimate. The hospital makes the final decision.

## Built with
Python, FastAPI, plain HTML/CSS/JavaScript, and the Claude API (Anthropic).

## Run it
See [README_RUN.md](README_RUN.md). Short version:

    py -m pip install -r requirements.txt
    set ANTHROPIC_API_KEY=your-key
    py -m uvicorn app.main:app --port 8000

Then open http://127.0.0.1:8000. Test bills (all fake) are in `app/static/test-bills/`.
Demo mode with no key: `set FAKE_AI=1`.

## Tests
Run each file in `tests/`; each prints ALL PASS.

## Origin
Started at TNHacks26 (October 2026) and continued for the Congressional App Challenge (TN-7).
