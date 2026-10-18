STATUS: pointer (2026-10-17 16:50 CDT) - No auth by design; AnswersIn extra="forbid" (no SSN/ID/name); instance principal (no keys on the VM); field values text/number only, <= 200 chars; 60 paid requests/60 s per IP + 600/hour total (record AL); nosniff/no-referrer/SAMEORIGIN headers; no /openapi.json. HTTP and HTTPS live since 2026-10-17 19:39 (Let's Encrypt IP certificate, expires 2026-10-24, no auto-renewal; record AH). Audit 2 #1, #2, #19 fixed on f10 (record AL); open: #12 number-lock design, #16 threadpool, #33 unused vendor dir. Audit: docs/2026-10-17_full-audit.md.
- 2026-10-18 (08265fa, deployed ~10:38 CDT, live): JSON POST bodies over 64 KiB get 413 "Request is too large." before parsing
  (declared length or bytes read, so chunked too; _JsonBodyCap is the innermost ASGI middleware - behind a BaseHTTPMiddleware
  the HTTPException arrives wrapped and becomes a 400). OCI GenAI read timeout 40 s. Security audit 2026-10-18 open items:
  opc runs the app with NOPASSWD sudo (harden after the event), instance-principal scope unverified (Evan checks the
  console), no daily cost cap, http :80 without CSP/HSTS, pending OS updates, swapfile vs "nothing is stored" (record BB).
- 2026-10-18 12:14 CDT - EOB text reads cut to 200 chars (af1d5f6). Human check is now one "This is correct" box per screen
  (189163e): still a person confirming every value before use (important.md 1), but weaker than per-field ticks (record BH).
