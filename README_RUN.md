# Run Bill to Help locally

Python 3 (on this laptop: `py`, 3.14).

```
py -m pip install -r requirements.txt
set FAKE_OCI=1
py -m uvicorn app.main:app --port 8000
```

Open http://127.0.0.1:8000/ . With `FAKE_OCI=1` the whole flow works with no
network and no credentials: the bill photo is "read" as the fields on
`spikes/synthetic-bill/bill-01`, the language model echoes the English facts,
and translations are tagged `[AR draft]` / `[ES draft]` (not real translations).

PowerShell: `$env:FAKE_OCI = "1"`. Bash: `FAKE_OCI=1 py -m uvicorn ...`.

## Real OCI (not FAKE)

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

- Tier 1, translated interface: en, es, ar, zh-CN, zh-TW.
- Tier 2, English interface; only the explanation and the cover letter and
  checklist are translated: vi, fr, ko, ru, de, hi. OCI Language has no Hindi,
  so the Hindi letter is written by Command A; numbers and the hospital name
  are protected and checked the same way as every other language. No
  language is back-translated: the check is placeholders plus the number lock.
- Tagalog is not supported by OCI Language or Command A: known gap.

## Tests

```
py tests/test_numlock.py
py tests/test_engine.py
py tests/test_api.py
py tests/test_policy_page.py
```

Each prints ALL PASS. The tests set FAKE_OCI=1 themselves.

Privacy: nothing is written to disk (uploads stay in memory: the multipart
spool limit is raised above the 8 MB cap) and request bodies are not logged;
only the TYPE of a failed model call is logged (e.g. `ServiceError`).
