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
