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
