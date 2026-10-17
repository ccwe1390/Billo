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
    Next.js needs Node >= 20.9 (Next.js docs via context7, checked
    2026-10-17; supersedes the "I think 18.18+" guess) - install a
    current Node LTS on the VM in M6.1.
  - Generative AI auth in the kit = API signing key in ~/.oci/config (key
    file chmod 600), separate from the SSH key. Instance principals are not
    covered by the kit.
  - Free Trial model to use: cohere.command-a-03-2025. Grok is NOT supported
    in the Free Trial.
- 2026-10-17 - Starter kit Terraform, read via gh api: the VM image is
  looked up by shape (`oci_core_images` filtered on `var.node_shape`, Oracle
  Linux 9), so an Arm shape gets an Arm image automatically. The installer
  `modules/webserver/scripts/install_shell.sh` runs as cloud-init user_data
  with no `set -e`, so its failures do NOT fail the Terraform apply. Its
  MySQL Shell fallback hardcodes an x86_64 RPM (we don't need MySQL Shell). It
  installs Node via `yum install -y npm` (the OS default, Node 16). It also
  appends `23.1.48.99 dev.mysql.com` to /etc/hosts - a hardcoded DNS pin;
  remove that line after first boot (judgment call, flagged to Evan).
- 2026-10-17 - Stack variables advised to Evan: shape VM.Standard.A1.Flex,
  2 OCPU / 12 GB (Always Free, Arm); fallback E5.Flex 1/4 if capacity fails.
  Databases: "MySQL HeatWave" only (the form has no "none"; Autonomous is
  paid). HeatWave "use credits for a more powerful DBSystem" left OFF.
