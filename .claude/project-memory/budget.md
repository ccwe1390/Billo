# budget - TNHacks26

- 2026-10-17 - Spend ceiling is $0 beyond the existing Claude Max plan; any
  other spend needs a conversation with Evan first. Owner of this fact:
  C:\ClaudeCode\standards\EVAN_CONTEXT.md section 3 (do not restate a
  different number here; point there).
- 2026-10-17 - Consequence: OCI usage (Generative AI, Document Understanding,
  Language) must run on hackathon-provided credits or a free trial/tier, or
  get Evan's explicit OK. Which of these exists: MISSING (BLOCKED-ON-EVAN).
- 2026-10-17 - The team has $500 in Oracle OCI credits (Evan, chat
  2026-10-17). Supersedes the "MISSING" in the entry above for the cost
  source. Still unknown: expiry date, whose account/tenancy holds them, whether
  a payment card is on file (overrun risk), and whether they cover Generative
  AI, Document Understanding, and Language.
- 2026-10-17 - Starter kit FAQ (github.com/ScottStroz/oci-hackathon-starterkit README (read 2026-10-17; third-party kit, not confirmed as TNHacks26-official)): the card is for identity
  verification; paid usage is billed only after you explicitly upgrade the
  account. So keep the account un-upgraded; spend past the credits then
  stops rather than charging the card (per the README - unverified with
  Oracle).
- 2026-10-17 15:49 CDT - Usage API (read-only), cost on 2026-10-17 UTC so
  far: $0.3175, all MySQL: DB ECPU $0.2928, HeatWave capacity $0.0220,
  storage $0.0027. The kit's MySQL.8 DB system + HeatWave.32GB cluster are
  NOT Always Free (~$0.10/hr), and the app never used them. Evan approved
  deletion; Claude deleted both via the OCI SDK (automatic backups set to
  DELETE first, final backup skipped). VM (E5.Flex) cost had not appeared
  in the usage data yet (lag). Budget alert still UNCONFIRMED.
