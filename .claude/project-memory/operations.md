# operations - TNHacks26

- 2026-10-17 - The website is hosted on OCI (Evan): ONE Compute VM running the
  Next.js server behind a reverse proxy (decisions.md). (Supersedes the
  earlier same-day entry: hosting service not chosen.)
- No scheduled jobs and no backups: the product stores nothing after a
  session, so there is nothing to back up (by design, HANDOFF Goal).
- Website-profile rows (project-memory profiles/website.md, read 2026-10-17):
  redirect map N/A (no earlier site); maintenance evidence N/A (no scheduled
  jobs).
- 2026-10-17 - To verify before relying on: Always Free covers the VM shape we
  pick; instance principals work for Generative AI, Document Understanding,
  and Language calls from that VM.
- 2026-10-17 - Starter-kit apply job ormjob20261017165954 FAILED at 17:27:34
  UTC (12:27 CDT) on the VM: "500-InternalError, Out of host capacity" for
  VM.Standard.A1.Flex (2 OCPU/12 GB) in US-CHICAGO-1-AD-1. Already created
  and kept in the stack's Terraform state: VCN, 2 subnets, security lists,
  internet gateway, route table, MySQL DB system "Hackathon MySQL HeatWave"
  (shape MySQL.8, 50 GB, about 14 min to create), and a HeatWave cluster
  (HeatWave.32GB, 1 node, about 13 min). Whether these are Always Free is
  UNVERIFIED - check the console. Fix: edit the stack's shape to
  VM.Standard.E5.Flex 1 OCPU / 4 GB (paid, uses credits) and re-apply; only
  the instance should be created.
- 2026-10-17 - Starter-kit re-apply SUCCEEDED (Evan pasted job page at
  ~14:09 CDT): APPLY job, compartment daruwallae23 (root), 18:13:32 ->
  18:15:02 UTC (13:13 -> 13:15 CDT). Shape used UNVERIFIED (expected
  E5.Flex 1/4 after the A1 capacity failure). Kit outputs (stack/output.tf,
  read via gh api): webserver_public_ip, ssh_private_key (generated PEM when
  no key path was given), heatwave_private_ip. Public ingress opens ONLY
  22, 80, 443 (so the app must serve on 80/443; Oracle Linux firewalld may
  also need the port opened). VM user on Oracle Linux 9: opc (I think,
  verify on first SSH). As of 14:09 CDT neither C:\Users\daruw\.ssh\ nor
  C:\Users\daruw\.oci\ exists on the laptop.
- 2026-10-17 14:42 CDT - DEPLOYED (fake mode) at http://207.211.181.174/ .
  SSH key: no visible output (sensitive, shown as a lock) -> extracted from
  the downloaded Terraform state (tls_private_key.public_private_key_pair)
  to C:\Users\daruw\.ssh\HackTN26.pem, locked with icacls; fingerprint
  SHA256:QA3BKoVf7B7Ub+BRjZ2U5/P9fi44/2Bc6uSMPcEfhp4 (RSA 2048). Evan to
  delete the state JSON from Downloads (it holds the key).
  VM facts: user opc, Oracle Linux 9.8, x86_64 (so E5.Flex, paid), 2 vCPU,
  3.4 GB RAM, Python 3.9.25 stock -> installed python3.12 (3.12.15) via dnf.
  Layout: /opt/bill-to-help (app from `git archive HEAD`, .venv,
  env file chmod 600 with FAKE_OCI=1), systemd unit bill-to-help.service
  (uvicorn 127.0.0.1:8000, --no-access-log, User=opc), Apache httpd on :80
  reverse-proxies to it (/etc/httpd/conf.d/bill-to-help.conf,
  LimitRequestBody 10 MB), SELinux httpd_can_network_connect=1. Checked from
  the laptop: / 200, /policy-cumberland.html 200, POST /extract bill-01 200.
  Redeploy = re-run the same git-archive + setup script (scratch, not in repo).
  Not live yet: VM has no OCI credentials (decision pending: instance
  principal vs copying the API key).
- 2026-10-17 14:55 CDT - VM LIVE with real OCI. /opt/bill-to-help/env
  (chmod 600): OCI_AUTH=instance_principal, OCI_COMPARTMENT_ID=<tenancy>,
  OCI_VISION_MODEL_ID=cohere.command-a-vision,
  OCI_TEXT_MODEL_ID=cohere.command-a-03-2025 (no FAKE_OCI). Redeploy used:
  `tar --exclude=__pycache__ -cf - app | ssh ... ` into ~/bill-to-help,
  copy app/ to /opt/bill-to-help/, `sudo systemctl restart bill-to-help`.
  Note: this shipped the working tree, not a commit - commit before the
  next deploy so the server matches git.
- 2026-10-17 15:06 CDT - Redeployed from commit 145c8af (`git archive HEAD
  app | ssh ...`), so the server matches git. Live app.js has 0 matches for
  the removed placeholder card; / returns 200.
- 2026-10-17 15:40 CDT - Redeployed from c689291 (Paper Trail) via
  `git archive HEAD app | ssh ...`. Live checks: /, /style.css,
  /fonts/fonts.css, an Arabic woff2, a Web Awesome variant CSS and an icon
  all 200; live app.js contains the new markers; real-AI journey 11.4 s,
  Spanish packet numbers_match=True.
- 2026-10-17 15:52-16:01 CDT - Deleted the starter kit's unused MySQL DB
  system "TNHacks26 Bill Decoder" (MySQL.8) and its HeatWave.32GB cluster
  via the OCI SDK, with Evan's approval. Automatic-backup retention was set
  to DELETE first; final backup skipped. HeatWave DELETED 15:58:15, DB
  system DELETED 16:01:35; list_db_systems shows 0 ACTIVE. Live journey
  passed afterwards (16:01, 11.3 s). NEVER re-apply the HackTN26-starterkit
  stack: Terraform would recreate both, and `destroy` would delete the VM.
- 2026-10-17 16:08 CDT - Redeployed from 116d631 (six bug fixes). Live
  checks: journey 11.7 s; ar and zh-TW packets keep the hospital name and
  pass the number check; packet HTML has <main> and the 640px stack rule.
- 2026-10-17 16:50 CDT - Corrections: the VM runs FastAPI/uvicorn behind
  Apache (the first entry's "Next.js" is superseded); instance principals
  for Generative AI and Language are verified live (decisions.md 14:50). The
  "To verify" entry on Always Free is moot: E5.Flex is a paid shape.
- 2026-10-17 16:58 CDT - Redeployed from c4a28f0 (audit fixes) with the
  git-archive command; Evan allowed SSH. VM venv versions read first and
  equal requirements.txt pins: fastapi 0.143.3, starlette 1.8.0, pydantic
  2.14.1, uvicorn 0.54.0, python-multipart 0.0.32, oci 2.188.0, Python
  3.12.15. Apache conf: ProxyPreserveHost On, ProxyPass / to 127.0.0.1:8000,
  LimitRequestBody 10485760 (mod_proxy adds X-Forwarded-For by default).
  Live checks: app.js equals git archive HEAD; nosniff / no-referrer /
  SAMEORIGIN headers; /openapi.json 404; text sent as image/png -> 415;
  journey bill-02-blur3 -> extract 3.5 s (date of service null, amount
  $1,858.50 correct) -> free_care 115% -> es explanation and es packet pass
  the number check, 10.7 s total; es not-eligible explanation passes; hi
  packet passes (translator command_a) in 15.7 s. journalctl: no warnings.
  Rollback target: 116d631.
- 2026-10-17 19:26-19:30 CDT - Evan said "go"; Claude's deploy of cc3c333
  was refused by the auto-mode classifier ("Production Deploy") even though
  SSH reads are allowed. Nothing changed on the VM (live app.js = c4a28f0).
  Evan runs deploys from Windows PowerShell 5.1 with deploy.ps1 (record
  AG): git archive -o file + scp (never a PS 5.1 pipe: it corrupts binary),
  then deploy-remote.sh on the VM (backup ~/backup-before-<c>.tar, stage,
  import check, swap, restart). The unit runs one uvicorn process (no
  --workers flag; counters are per process).
- 2026-10-17 23:44 CDT - The deploy scripts live in the repo at deploy/
  (moved from the session scratchpad, record AN); .gitattributes keeps
  deploy/*.sh LF because core.autocrlf=true. Run from the repo root:
  powershell -ExecutionPolicy Bypass -File deploy\deploy.ps1 -Commit <c>.
- 2026-10-17 19:30-19:42 CDT - Deployed by Evan (deploy.ps1/https.ps1),
  checked by Claude (record AH): D1 cc3c333 (19:30) -> HTTPS (mod_ssl,
  certbot 5.8.0 in /opt/certbot, cert lineage billscan-ip for IP
  207.211.181.174, expires 2026-10-24 15:39 GMT, no renewal timer; conf.d
  bill-to-help-acme.conf + bill-to-help-ssl.conf; :80 unchanged) -> D2
  c30be63 (19:41). Backups on the VM: ~/backup-before-cc3c333.tar (=
  c4a28f0 app), ~/backup-before-c30be63.tar (= cc3c333 app). main =
  c30be63. Live journeys pass on http and https; journal clean.
- 2026-10-18 00:07 CDT - Evan deployed 5af2f1f with deploy.ps1 (32 languages +
  audit-2 fixes). Backup ~/backup-before-5af2f1f.tar (= c30be63 app); rollback
  target c30be63. Live checks 00:09 (record AR) pass on http and https. Local
  main = 5af2f1f (not pushed). 07:4x: deploy-remote.sh / rollback-remote.sh now
  fail unless the engine loads (m._rules()) and /stats answers after restart
  (984a537, record AT; first used on the next deploy).
- 2026-10-18 ~07:48 CDT - Evan deployed 984a537 (audit 3 fixes). The health
  check ran for the first time and passed after one refused curl during
  start-up. Backup ~/backup-before-984a537.tar (= 5af2f1f app); rollback target
  5af2f1f. Live checks 07:50 pass (record AU). Local main = 984a537.
- 2026-10-18 08:48 CDT - Claude ran deploy.ps1 at Evan's request: rehearsal (984a537 again with
  the new scripts: "backup: keeping existing", DEPLOYED, -Watch OK), then bdc76df (real VUMC +
  Ascension policies). Backup ~/backup-before-bdc76df.tar = the 984a537 app. ROLLBACK from bdc76df:
  `deploy.ps1 -Commit bdc76df -Rollback` (restores 984a537). Do NOT roll back with -Commit 984a537:
  that restores the 5af2f1f app (Cumberland only). Live checks 08:49 pass (record AV). main = bdc76df.
- 2026-10-18 09:59 CDT - Claude deployed f6b6f05 (audit-4 fixes; first run of the split rm/mkdir/tar
  lines). Backup ~/backup-before-f6b6f05.tar = the bdc76df app. Rollback: `deploy.ps1 -Commit f6b6f05
  -Rollback` (restores bdc76df). Live checks 10:00 pass (record AX). main = f6b6f05.
- 2026-10-18 10:20 CDT - Claude deployed e53d1ce (landing-check fixes + VUMC underinsured condition).
  Backup ~/backup-before-e53d1ce.tar = the f6b6f05 app. Rollback: `deploy.ps1 -Commit e53d1ce -Rollback`
  (restores f6b6f05). Live checks 10:21 pass (record AZ). main = e53d1ce, not pushed.
- 2026-10-18 ~10:38 CDT - Claude deployed 08265fa (Evan: "Do 1-4"). Backup ~/backup-before-08265fa.tar = the e53d1ce app.
  Rollback: `deploy.ps1 -Commit 08265fa -Rollback` (restores e53d1ce). Live checks pass (record BB).
- 2026-10-18 ~10:35 CDT - Apache (VM only, not in the repo): /etc/httpd/conf.d/bill-to-help-perf.conf (DEFLATE for
  html/css/js/json/svg/text, DeflateAlterETag NoChange) and `Protocols h2 http/1.1` in bill-to-help-ssl.conf (backup
  ~/bill-to-help-ssl.conf.before-perf). Undo: delete the perf conf, copy the backup back, `sudo systemctl reload httpd`.
- 11:11 CDT - Phase 2 build on worktree C:/ClaudeCode/TNHacks27-f12 (branch f12); preview config f12-fake (port 8770) in
  .claude/launch.json. NOT deployed; merge + deploy only on Evan's word, 12:40 CDT hard cut (record BB).
- 2026-10-18 11:16 CDT - Claude deployed 99d4851 (merge of f12: Phase 2 + Billow). Backup ~/backup-before-99d4851.tar = the 08265fa
  app. Rollback: deploy.ps1 -Commit 99d4851 -Rollback (restores 08265fa). Live checks pass (record BC).
