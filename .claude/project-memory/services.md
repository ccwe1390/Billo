# services - TNHacks26

OCI is mandatory (important.md 4). Candidate OCI services for the Bill Decoder,
from Oracle docs/marketing pages searched 2026-10-17. Not yet tested, not yet
chosen; no account exists yet (BLOCKED-ON-EVAN). Credential NAMES only here,
never values.

- OCI Document Understanding - OCR + table extraction (rows/cols/cells) from
  PDF/JPEG/PNG/TIFF. Table extraction may be English-only (docs inconsistent);
  fine for US bills, which are English.
  https://www.oracle.com/artificial-intelligence/document-understanding/features/
- OCI Generative AI - chat models (lineup varies by region; check the live
  "Models by Region" page). 11 commercial regions incl. Ashburn, Chicago,
  Phoenix. https://docs.oracle.com/en-us/iaas/Content/generative-ai/regions.htm
- OCI Language - text/document translation, ~30 languages (sources say 21-31;
  check current docs). https://www.oracle.com/artificial-intelligence/text-translation/
- Not checked yet: free-tier/credit coverage of these services, hosting choice
  (Compute vs Functions), OCI Vault for secrets.
