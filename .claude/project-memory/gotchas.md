# gotchas - TNHacks26

- 2026-10-17 - Synthea is NOT deterministic with default threading, even
  with -s/-cs/-r fixed. Pass `--generate.thread_pool_size=1` (verified
  byte-identical across 2 runs). Source: data.md.
- 2026-10-17 - Synthea's `master-branch-latest` jar is a moving tag; pin by
  our recorded sha256 (dependencies.md), not by re-downloading.
- 2026-10-17 - Synthea output has no contractual adjustments (0 nonzero
  ADJUSTMENTS rows); error type 3 needs adjustments we generate.
- 2026-10-17 - Java is portable, not on PATH: call it by full path.
- 2026-10-17 - Evan's local shell is PowerShell 5.1: no `&&`, no `chmod`.
  VM commands (dnf, Node upgrade) run INSIDE the SSH session (bash on Oracle
  Linux), not locally. Windows OpenSSH refuses a private key that other users
  can read; restrict it with `icacls .\key.pem /inheritance:r` then
  `icacls .\key.pem /grant:r "$($env:USERNAME):(R)"` (the README's
  `chmod 600` is the macOS/Linux equivalent).
- 2026-10-17 - SSH key file name/location (Evan): save the starter kit's
  generated key as `C:\Users\daruw\.ssh\HackTN26.pem` - outside the repo so it
  can never be committed. Use that path in the icacls/ssh commands above.
- 2026-10-17 - Python on Evan's laptop: use `py` (Python 3.14.7, pip 26.2.1).
  `python`/`python3` hit the Microsoft Store alias and fail. This corrects
  earlier "no Python" claims (record Appendix O). The `oci` package was NOT
  installed then (installed later: 2.188.0).
- 2026-10-17 - `Element.replaceChildren(a, null, b)` renders the null as the
  text "null" (unlike our `el()` helper, which skips nulls). It showed on the
  result screen as two stray "null" lines. Fixed at the chokepoint: every
  caller in app/static/app.js goes through `fill()`, which filters nulls;
  tests/test_api.py asserts `.replaceChildren(` appears only inside fill().
- 2026-10-17 - OCI config on Windows: Notepad saved `config` as
  `config.txt`, and the downloaded key was saved without `.pem` while
  `key_file=` pointed at `oci_api_key.pem` -> ConfigFileNotFound. Fixed by
  renaming both (Claude, 14:21 CDT). Check with
  `py -c "import oci; oci.config.validate_config(oci.config.from_file())"`.
- 2026-10-17 - Model IDs: on-demand serving accepts the model NAME (e.g.
  `cohere.command-a-vision`, `cohere.command-a-03-2025`); list them with
  oci.generative_ai.GenerativeAiClient.list_models (endpoint
  https://generativeai.us-chicago-1.oci.oraclecloud.com) - the console's
  "View code" showed `---`.
- 2026-10-17 - Record entry bodies: NO line may start with three backticks.
  Appendix U line 682 did ("```json fence ..."), opening a code block that
  never closed; append-record-entry.js skips fenced lines, so it refused
  every later append (TOC/heading count mismatch). The record-guard hook
  blocks Claude from editing the record; the repair needs Evan (edit by
  hand, or relaunch with PM_RECORD_UNLOCK=1). Check before appending:
  grep -n '^\s\{0,3\}```' <body file> must print nothing.
- 2026-10-17 - Machine translation mangles proper nouns, and the number
  lock only guards digits. Protect names (hospital name) with the same {n}
  placeholders as numbers and check they survive (oci_client.protect_numbers
  keep=). Hindi uses Command A without placeholders, so it is unprotected.
- 2026-10-17 - Windows console is cp1252: printing Arabic/Chinese from
  Python raises UnicodeEncodeError. Use PYTHONIOENCODING=utf-8 and write to
  a file.
- 2026-10-17 - A page served from the public VM cannot fetch from
  127.0.0.1 (Chromium blocks public-to-private requests). For browser tests
  that need local files, run the app locally instead.
- 2026-10-17 - The browser pane's screenshots can lag a fresh DOM change;
  confirm the visible screen with JS before trusting a shot.
- 2026-10-17 16:50 CDT - The Appendix U fence gotcha above was repaired in
  0f8e552; the rule (no record line may start with three backticks) stands.
- 2026-10-17 - Starlette spools any multipart upload over 1 MiB to a temp
  FILE on disk before the handler runs (MultiPartParser.spool_max_size).
  Phone photos are larger, so "nothing written to disk" was false until
  main.py raised the limit above the 8 MB cap (audit, record AA).
- 2026-10-17 - An `async def` FastAPI endpoint that calls a blocking SDK
  freezes the whole event loop: static files and every other user wait.
  Call blocking work with `await asyncio.to_thread(...)`, or make it a plain
  `def` (FastAPI runs those in a thread pool).
- 2026-10-17 - numlock.check(text, locked) treats every locked number as
  REQUIRED. Passing "allowed" numbers there (the engine's discount "0" for a
  not-eligible tier) made every non-English not-eligible explanation fall
  back. Required = numbers in the English facts; locked = allowed only.
- 2026-10-17 20:52 CDT - SUPERSEDES the Hindi line above: since c4a28f0 the Hindi
  path masks numbers and the hospital name like every language
  (oci_client.translate_genai_many -> protect_numbers/restore_numbers).
- 2026-10-17 23:30 CDT - SUPERSEDES the spool note above: spool_max_size is now
  MAX_IMAGE_BYTES and a middleware refuses /extract bodies whose
  Content-Length exceeds 8 MiB + 64 KiB before FastAPI parses them; the old
  "raise the spool above the cap" let 9-10 MiB bodies reach a temp file
  (audit 2 #15). A chunked upload with no Content-Length still parses first.
