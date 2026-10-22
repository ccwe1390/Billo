# Run Billo (formerly Billo) locally

Python 3 (on this laptop: `py`, 3.14).

```
py -m pip install -r requirements.txt
set FAKE_AI=1
py -m uvicorn app.main:app --port 8000
```

Open http://127.0.0.1:8000/ . With `FAKE_AI=1` the whole flow works with no
network and no credentials: the bill photo is "read" as the fields on
`spikes/synthetic-bill/bill-01`, the language model echoes the English facts,
and translations are tagged `[AR draft]` / `[ES draft]` (not real translations).

PowerShell: `$env:FAKE_AI = "1"`. Bash: `FAKE_AI=1 py -m uvicorn ...`.

## Real AI with Claude (the default)

Billo uses the Anthropic API (Claude) unless `AI_PROVIDER=oci`. One model reads the
bill photo, rewrites the explanation and translates the letter, in every language.

| Env var | Meaning |
|---|---|
| `ANTHROPIC_API_KEY` | your key from console.anthropic.com (never commit it) |
| `BILLO_CLAUDE_MODEL` | optional; default `claude-opus-5-5` |
| `BILLO_CLAUDE_EFFORT` | optional; default `low` |

```
set ANTHROPIC_API_KEY=sk-ant-...
py -m uvicorn app.main:app --port 8000
```

Numbers and the hospital name are still swapped for `{n}` placeholders before
translating and checked by the number lock after, exactly as with OCI.

## Real OCI (`AI_PROVIDER=oci`, the TNHacks26 setup)

Needs `~/.oci/config` (profile DEFAULT, or set `OCI_PROFILE`) and:

| Env var | Meaning |
|---|---|
| `OCI_COMPARTMENT_ID` | compartment OCID |
| `OCI_VISION_MODEL_ID` | Command A Vision model ID (confirm in the console) |
| `OCI_TEXT_MODEL_ID` | Command A model ID |
| `OCI_LANGUAGE_ENDPOINT` | optional OCI Language endpoint override |
| `OCI_AUTH` | `instance_principal` on the OCI VM (no key on the server); unset on a laptop (uses `~/.oci/config`) |

Generative AI calls go to the Chicago endpoint. OCI Language translation was
verified live on 2026-10-17 for es, fr, de, ru, ar, zh-CN, zh-TW, ko and vi
(n=1 each, experiments.md).

## Languages

- 32 languages, listed once in `app/data/languages.json`: the 31 codes Oracle
  Translate supports (29 languages; fr/fr-CA and pt/pt-BR) plus Hindi. Every
  language has a translated interface, picked from a dropdown.
- Interface text: en, es, ar, zh-CN, zh-TW are hand-written inside
  `app/static/app.js`; the other 27 are `app/static/i18n/<code>.json`,
  machine-translated once by OCI (Hindi by Command A) and not human-reviewed.
  Rebuild: `node scripts/dump_ui_strings.js app/static/app.js t_en.json`, then
  `py scripts/build_i18n.py t_en.json [codes]` (real OCI, laptop key).
- Safety lines (estimate, the hospital decides, nothing saved, no ID asked)
  show the English under a machine translation; strings whose meaning flipped
  on back-translation are English only (`DROP` in scripts/build_i18n.py).
- Explanation: Command A or OCI Language per `languages.json`; the cover
  letter: OCI Language, Hindi by Command A. Numbers and the hospital name are
  protected and checked in every language (placeholders plus the number lock).
- Tagalog is not supported by OCI Language or Command A: known gap.

## Tests

```
py tests/test_numlock.py
py tests/test_engine.py
py tests/test_api.py
py tests/test_claude_backend.py
py tests/test_policy_page.py
py tests/test_answer_key.py
py tests/test_checks.py
py tests/test_eob_checks.py
py tests/test_dispute.py
node tests/test_app_js.js
```

Each prints ALL PASS. The tests set FAKE_AI=1 themselves (FAKE_OCI=1 still works).

Privacy: nothing is written to disk (an upload over 8 MB is refused by its
Content-Length before it is read; allowed uploads stay in memory) and request bodies are not logged;
only the TYPE of a failed model call is logged (e.g. `ServiceError`).
