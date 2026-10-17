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
- 2026-10-17 - Decided (Evan): OCI Language is the translator; the website is
  hosted on OCI. See decisions.md.
- 2026-10-17 - From the OCI starter kit README (github.com/ScottStroz/oci-hackathon-starterkit README (read 2026-10-17; third-party kit, not confirmed as TNHacks26-official)):
  - Account: Chicago home region (permanent), same email as the promo
    credits, Individual, MFA via Oracle Mobile Authenticator.
  - Kit deploys via Resource Manager: VCN + subnets + gateways, one compute
    instance (default VM.Standard.E5.Flex, 1 OCPU, 4 GB - a PAID shape; other
    shapes allowed; E5 capacity not guaranteed), plus MySQL HeatWave (Always
    Free default) and/or Autonomous DB (paid). We store nothing, so no DB is
    needed by our design.
  - The kit's VM ships Node.js 16, Python 3.9 (3.12 installable), Java.
    Next.js needs a newer Node than 16 (I think 18.18+; verify) - install a
    current Node LTS on the VM in M6.1.
  - Generative AI auth in the kit = API signing key in ~/.oci/config (key
    file chmod 600), separate from the SSH key. Instance principals are not
    covered by the kit.
  - Free Trial model to use: cohere.command-a-03-2025. Grok is NOT supported
    in the Free Trial.
