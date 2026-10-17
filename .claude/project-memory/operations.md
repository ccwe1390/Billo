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
