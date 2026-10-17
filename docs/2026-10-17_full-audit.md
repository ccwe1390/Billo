# Full audit - code + docs + cross-domain (2026-10-17 16:35 CDT)

Scope: C:\ClaudeCode\TNHacks27, whole project, HEAD 4a89076, tree clean.
Method: the `audit` skill. 4 cold Sonnet workers (A code-core M1-M3/M10/M13,
B code-surface M6-M9/M12/M15/G1-G4, C live docs D1-D8, D history docs),
session model (Opus) re-ran every high and ran the X-series. Findings pass
changed nothing. Fix status is recorded in the project record, not here.

## 1. Executive summary

The code is healthier than the story told about it. Most highs are claims that
outlived the code: back-translation was never built, MySQL HeatWave was never
used and is deleted, VUMC was never encoded, yet the pitch text, HANDOFF and
PRD F2 still describe them, and the tests assert a `back_checked: true` flag
that measures nothing. Two code highs would show on stage: one photo read
freezes the whole site, and any not-eligible result in a non-English language
always falls back to English. Engine, number-lock presence check, escaping,
client-result rejection and secrets are clean.

## 2. Architecture and policy decisions (outrank the fix list)

- A1. No corrected pitch exists. The only pitch / demo script / judge answers
  (docs/2026-10-17_HackTN26_Health_Access_Plan_rev2.txt) still say "The
  hospital prints a code" (345, 358, 420), "VUMC already selected" / "VUMC's
  policy opens" (357, 381), "Download PDF" (192), Dad's bills / reminders /
  dashboard (194-197, not built), "Each rule is a database row" (414), "four
  Oracle services" (406), and has no B.A.R.S. answer (0 hits). F9 wording fix
  1 would claim an opt-in save that does not exist (DH6).
- A2. One synthetic policy for every hospital (CC6). hospital_name
  "Vanderbilt University Medical Center" -> free_care, Cumberland's email and
  phone, letter "To the Financial Assistance Office, Vanderbilt University
  Medical Center:".
- A3. Paid endpoints are public with no rate limit and no field length cap; an
  8,000,000-char hospital_name reached the model prompt (CS4). Budget alert
  unconfirmed.

## 3. Findings

Src: A, B, C, D = workers; S = session model. Tier CONFIRMED = re-run by S
unless marked "(A)" / "(B)" (worker reproduced it).

| # | Sev | Tier | Src | Finding | Evidence | Fix | Eff |
|---|---|---|---|---|---|---|---|
| 1 | high | CONFIRMED | A,B,S | /extract is `async def` and calls the blocking OCI SDK: one bill read freezes the server | stub 1 s: extracts done 1.06/2.06/3.06 s; an unrelated 0.05 s task done at 3.06 s; main.py:151,159 | `await asyncio.to_thread(...)` | XS |
| 2 | high | CONFIRMED | A,B,S | Not-eligible + any non-English language always fails the number lock -> English fallback | locked [...,'0','240'] -> numbers_match False for es, ar; engine.py:150 locks "0" | required = numbers in the facts; locked = allowed | XS |
| 3 | high | CONFIRMED | C,A,B,S | "translate + back-translate check" is false; `back_checked` flag (main.py:318) asserted by tests | 0 back-translation code (grep + Grep tool) | rename flag; fix HANDOFF:51, PRD F2, contracts | S |
| 4 | high | CONFIRMED | C,D,S | HANDOFF, PRD F2 (:302), rev2 say MySQL HeatWave holds the rules; rules are JSON, DB deleted 16:01 | git grep + grep mysql/heatwave in app/tests: exit 1 | dated strike; corrected pitch | XS |
| 5 | high | CONFIRMED | D,S | rev2 pitch/demo/judge text contradicts F9 and the build (A1) | grep lines above | corrected pitch sheet | S |
| 6 | med | CONFIRMED | A,S | Any hospital name gets Cumberland's policy (A2) | S run: free_care, Cumberland contacts, Vanderbilt letter | match flag + warning | S |
| 7 | med | CONFIRMED (laptop) | A,B,S | Uploads > 1 MiB are spooled to a temp file on disk; "nothing written to disk" false | Starlette 1.8.0 spool_max_size = 1 MiB; 3 MB upload rolled to disk | raise spool size above 8 MB | XS |
| 8 | med | CONFIRMED (A) | A,B | Double-upload race: last reply wins | browser: HOSP A fields beside image B | sequence token in onFile | XS |
| 9 | med | CONFIRMED (A) | A | Re-pick leaves the old Continue enabled with S.bill null | app.js:281 no re-render | renderBill() after S.bill = null | XS |
| 10 | med | CONFIRMED (B) | B | No field length cap, no rate limit (A3) | 8,000,000 chars -> 200 | max length + per-IP limit | S |
| 11 | med | REPORTED (needs live OCI) | A | `_chat` ignores finish_reason; max_tokens 600; truncated Hindi passes the lock | oci_client.py:67-74 | fail unless COMPLETE | XS |
| 12 | med | CONFIRMED (A) | A | Tests weaker than green: 16/47 mutants survive; oci_client 48% covered; app.js 0 behaviour tests | A's mutation + settrace run | add targeted tests | M |
| 13 | med | CONFIRMED (C) | C,A | Language list drift: contracts.md:9 en/es/ar; decisions.md:117-125; HANDOFF Goal; PRD F1 | main.py:49 has 11 | doc edits | S |
| 14 | med | CONFIRMED (C) | C,D | HANDOFF:44 "deployed from c689291"; live is 116d631 | last-modified 16:08 CDT | one line | XS |
| 15 | med | CONFIRMED (C) | C | Handoff prompt "Next" lists the done axe audit | 5e80c6d | rewrite | XS |
| 16 | med | CONFIRMED (C) | C | Bins frozen in the morning (stub bins, INDEX:47, no PIVOT in decisions.md, dependencies.md Next.js) | 103 tracked files | pointers + PIVOT entry | S |
| 17 | med | CONFIRMED (C,D) | C,D | PRD F4 0/8 ticked; F3 "10 bills" (2 exist); F9 Home/Reminders/QR not marked; :278 Tennessee card | ls, grep | dated notes | S |
| 18 | med | CONFIRMED (D) | D | 14 unfilled [x] brackets in the pitch region | grep count | fill from V1 or cut | S-M |
| 19 | med | REPORTED (no network) | D | Unverified slide numbers beyond T7 ($7B, 175%, 24%, 9.3%, 282,294, HHS 2026 values) | no verification record | extend T7; verify HHS | S |
| 20 | low-med | CONFIRMED (B) | B | requirements.txt unpinned; server versions unrecorded | 4 bare names | pin | S |
| 21 | low-med | CONFIRMED (A) | A | Client discards 413/415 reasons: big phone photo shows "not available" | app.js:287 | show size/type message | XS |
| 22 | low | CONFIRMED (A,B) | A,B | "1e999999" -> decimal.Overflow 500; "1E+400000" ~15 s spin | function + endpoint runs | length guard + ArithmeticError | XS |
| 23 | low | CONFIRMED (A,B) | A,B | Decimal comma read 100x ("4812,40" -> 48124000) | _norm_cents runs | null when ambiguous | XS |
| 24 | low | CONFIRMED (A,B) | A,B | Non-string or 9999-12-31 statement date -> 500; "20261001" accepted | engine.py:63,102 | YYYY-MM-DD only, catch errors | XS |
| 25 | low | CONFIRMED (A) | A | Broad excepts log nothing | 0 logging calls | log exception type only | XS |
| 26 | low | CONFIRMED (A,B) | A,B | Past deadline printed with no warning | 2020-01-01 -> "Apply by 2020-08-28" | UI note | S |
| 27 | low | CONFIRMED (A,B) | A,B | Number lock is set membership; fullwidth digits fail closed | check() runs | add fullwidth digits; honest wording | XS |
| 28 | low | CONFIRMED (B) | B | Literal "{1}" in an account number collides with placeholders | became 2026-10-01, lock passed | protect literal {n} first | S |
| 29 | low | CONFIRMED (B) | B | HTTP only, no security headers, /openapi.json public | curl -D; ASGI GET 200 | openapi_url=None, headers; TLS is M | XS/M |
| 30 | low | mixed | A,B,C,D | submitAnswers races (CC19/20); focus/ARIA (CS13); non-ASCII digits (CS14); no LICENSE (CS12); README_RUN stale (DL6/14/15); a11y audit stale (DL16); gotchas stale (DL10); pre-mortem dead refs (DL11); PRD:219 TAB path (DL19); "bump out" inference (DH9); brief errata (DH10/11); record time slips (DH13/14); 61.0% denominator (DH16) | per worker | mostly one-line | XS |

## 4. Edge cases (P1/P2 in full)

| # | Pri | Gen | Trigger | Where | Failure |
|---|---|---|---|---|---|
| E1 | P2 | G2 | pick photo A then B before A returns (CONSTRUCTED; A reproduced in browser) | app.js:276 | A's fields beside image B |
| E2 | P2 | G4 | account number "{1}" with a hospital name (OBSERVED) | oci_client.py:146 | wrong value, lock passes |
| E3 | P2 | G1 | model returns "4812,40" (OBSERVED, function level) | main.py:103 | $481,240.00 shown |
| E4 | P2 | G1 | 8,000,000-char hospital_name to /explain (OBSERVED) | main.py:34 | paid call with a huge prompt |

P3: over-limit in non-English (#2); "38.000" or Arabic-Indic income disables
the button with no message; 9999-12-31 -> 500; past deadline; 1 cent over 200%
shows "200%" on the 75% row (CC12, documented floor); "1 people"; income
10^15 -> percent 62656641604; "1E+400000" spin; any contract_version
accepted; text bytes sent as IMAGE/PNG accepted (no magic-byte check).

## 5. Verified true (load-bearing negatives)

- No secrets: pm-secretscan --history and --worktree 0 (S); grep for
  private-key, tenancy/user OCIDs, key fingerprints 0 (S); B second grep 0.
- Live serves HEAD: live app.js sha256 equals `git archive HEAD` (S); md5 vs
  `git show` plus last-modified 16:08 CDT (C); only LF vs CRLF differs (B).
- 4/4 test files exit 0 (S real exit codes; C and D re-ran).
- Packet injection-safe: escaped payloads in en/es/ar/hi, html.escape on every
  value, iframe without allow-scripts (B, two methods).
- No innerHTML/outerHTML/insertAdjacentHTML/document.write/eval in app.js
  (B, grep + Grep tool).
- Client result ignored: mutants A2/A3 killed; extra="forbid" rejects ssn with
  422 (B, C).
- Money exact: 3192000 cents -> free care, 3192001 -> discount (B, tests).
- No browser storage, no third-party runtime requests (B, C).
- Record at rest: A-Y contiguous, 26/26 TOC anchors, 0 fences, 0 CRLF, 0
  non-ASCII; only deletion ever is the documented 0f8e552 line (D).
- 0 Co-Authored-By trailers in history (C).

## 6. Corrections to the project's own records

| Claim as written | Re-measured | Verdict |
|---|---|---|
| HANDOFF:44 "deployed from c689291" | 116d631 | false |
| "OCI Language (translate + back-translate check)" | no back-translation code | false |
| "11.8 s ... blurred bill photo" | 9.7 s gate run, 11.8 s 14:55 re-run; rendered PNG | mixes runs |
| pre-mortem P1 "4 services ran live, no errors" | 3 services, 2 bugs found that day | false |
| a11y audit "`<main>` fix not applied yet" | applied in 116d631 | stale |
| gotchas "six callers of fill()" | 7 | stale |
| pre-mortem "5 launch-blocking" | E1, E4 later reclassified launch-blocking | ambiguous |

## 7. Fix order

A1-A3 decisions first. Then 1, 2, 8, 9, 21 (XS demo fixes; 8 must ship with 1
because 1 un-serializes uploads). Then 3, 4, 5, 14, 15, 18 (what teammates
say). Then 7, 10, 11, 22, 24, 6. Then 12, 13, 16, 17, 19, 20. Then E2, E3 and
23-30.

## 8. Coverage

Swept: M1, M2, M3, M13, M10 (A); M6, M7, M8, M9, M12, M15, G1-G4 (B); D1-D8
(C); D1, D2, D5-D8 (D). Partial: M4 (no linters installed; stdlib AST pass and
node --check only), M5 (all files born 2026-10-17, relative churn
uninformative; statement coverage by a settrace script, no branch coverage).
Not swept: M11 fuzzing, M14 graph (4 modules), every real-OCI path, the VM
side (Apache, systemd, /tmp, logs). X1-X5 run by the session model, NOT cold.
Trails: C counted 34 files (the brief's 35 was an orchestrator arithmetic
slip, 6+26+2); D's shard was 10 (3 docs went to C); no file dropped, 103/103
tracked covered; independent re-count vendored 37 = 37, bins 26 = 26. B cited
non-existent lines (engine.py:271/310/358, numlock.py:402); its findings
reproduced at engine.py:63/102/150.

## 9. Cost

4 Sonnet workers, 0 delegates, 261 worker tool calls, ~1.03M subagent
tokens, ~20 min wall clock (16:14-16:35 CDT).

## 10. Addendum

Worker A ran `taskkill /F /FI "IMAGENAME eq py.exe"` to stop its own server,
which force-kills every py.exe on the laptop. No Python process was running at
16:35. Any Python job of Evan's that failed around 16:25-16:30 may be this.
