# Research brief - How BillScan sustains itself financially

**Date:** 2026-10-17 (written 23:23-23:40 CDT; saved 23:45 CDT)
**Status: PARTIAL.** The comparables-funding and hospital-economics /
regulation collection did not complete in the first run; a second agent is
collecting it and its findings will be merged below (section "Merge").
Until then the model ranking is an assumption-driven hypothesis table, not
an evidence-tested verdict. Do not quote it to judges as settled.
**Question:** Which revenue or funding model can pay BillScan's operating
costs (cloud AI calls, hosting, translation review, support, compliance)
without charging low-income patients or creating a conflict with the
patient's interest?
**For:** Evan and the TNHacks26 team - the judge answer "how does this
sustain itself" (2026-10-18) and the post-hackathon owner/funding decision
(PRD F11 open item O-1).

## TL;DR (first run)

- No model won yet: the evidence that decides between them (comparables'
  990s, hospital vendor spend, Oct-2026 regulation status) was not collected
  in the first run.
- One verified finding changes the question: cloud cost per patient is
  cents. Roughly $0.04-$0.15 per non-English packet journey and ~$30/month
  for the VM. Large Cohere is $0.0156 per 10,000 characters and OCI Language
  translation is $10.00 per 1,000 transactions after the first 1,000
  (both VERIFIED-VERBATIM on Oracle's price list, list updated 2026-10-08).
- So cloud is not the cost to fund. The unpriced costs are people and
  compliance: a maintainer, native-speaker translation review, support,
  privacy/legal review, and policy-rule upkeep per hospital.
- Working hypothesis (untested): a grant-funded nonprofit pilot first
  (lowest conflict, fits "nothing stored"), then a flat-fee subscription for
  NONPROFIT hospitals behind conflict firewalls. Contingency fees on patient
  savings are ruled out.
- Source-interest: every verified number is Oracle's own list price
  (VENDOR-SELF-REPORTED) - the right source for a list-price claim; no
  independent cost data was collected.

## Hypotheses (written before collection)

- H1 (expected best): B2B SaaS to nonprofit hospitals - IRS 501(r) FAP,
  publicity and translation duties plus Schedule H charity reporting make a
  multilingual front door that raises completed applications worth paying
  for. Refuted if incumbents already sell presumptive screening cheaply, or
  if more FAP enrollment costs hospitals revenue they would rather keep.
- H2: grants/philanthropy as a nonprofit or fiscally sponsored project.
  Refuted if funders do not back software-only tools without outcome data.
- H3: licensing to EHR/patient-portal or patient-financial-engagement
  vendors (Epic, Cedar, Flywire). Refuted if they already ship multilingual
  FAP screening.
- H4: Dollar For-style nonprofit with human advocates, software as a force
  multiplier.
- H5: payers / Medicaid MCOs / employers / government contracts.
- H0: no model sustains it without conflict; it stays a portfolio project.
- Ruled out: a contingency fee on patient savings - it charges the
  low-income patient, rewards overstated "savings" (the app bans that word),
  and may fall under Tennessee debt-adjusting regulation (lead only: the TN
  Commerce PDF returned 404 - UNREACHABLE; needs legal review).

## Method (first run)

Primary sources for unit economics: Oracle's price list page (browser text)
and its price-list API JSON (lastUpdated 2026-10-08T14:38:16Z), Oracle docs
(pay-on-demand, Command A Vision), an archived copy of the OCI Language
pricing page (web.archive.org snapshot 2025-12-06; the live page redirects to
an estimator). Code read: app/main.py, app/oci_client.py,
app/data/policy_cumberland_synthetic.json to count calls and characters per
journey. Limitations: no interviews (willingness to pay needs 5-10 discovery
calls with patient-financial-services directors and foundation program
officers); no measured OCI bill (the tenancy Usage API was not queried, so
image billing is an estimate); stage 8.5 ran on the unit-economics claims
only.

Phase effects (2026-10-17):
  8.5 verify - added a limitation (Command A Vision image billing is
               undocumented: docs give tokens per image, pricing is per
               character) and caught a conflict (current price list: first
               1,000 translation transactions free; archived page: first
               5,000). No verdict flipped - there was no verdict yet.
  10.5 assess - run by the orchestrator over all briefs (see the end).

## F1. Unit economics (verified prices, estimated quantities)

Prices (VERIFIED-VERBATIM unless marked):
- "Oracle Cloud Infrastructure Generative AI - Large Cohere $0.0156 10,000
  transactions"; "A transaction is a character" (price list; same in the
  API JSON, part B108077).
- Chat is billed on "prompt length (in characters) + response length (in
  characters)" (docs, pay-on-demand).
- Command A Vision bills as Large Cohere; "A 512 x 512 image is converted to
  about 1,610 tokens" - the docs do not say how image tokens become billed
  characters, so per-image cost is UNKNOWN.
- OCI Language text translation: first 1,000 transactions $0.00, then
  $10.00 per 1,000 transactions (price list; API part B95920). A transaction
  is up to 1,000 characters per API call, rounded up (archived page).
- VM.Standard.E5.Flex: $0.03 per OCPU-hour, $0.002 per GB-hour (price list).

Per-journey estimate (ASSUMPTION-DRIVEN; characters estimated from the
prompts and templates in the code, not measured):

| Step | Service | Estimated quantity | Estimated cost |
|---|---|---|---|
| /extract text | Large Cohere | ~260-char prompt + ~300-char reply | ~$0.0009 |
| /extract image | Large Cohere | unknown; 1,610 tokens x ~4 chars ~ 6,440 chars, up to ~9 tiles for a phone photo | $0.01-$0.09 (bound, unverified) |
| /explain (Command A languages) | Large Cohere | ~2,300 chars in+out | ~$0.004 |
| /explain (OCI Language languages) | Translation | ~800 chars, 1 transaction | $0.01 |
| /packet | Translation | letter 1-2 transactions + 2-3 checklist items | $0.03-$0.05 |
| Non-English journey | | | ~$0.04-$0.15 |

Hosting: 1 OCPU / 4 GB = $0.038/hour x 744 h = $28.27/month, plus ~$2/month
boot volume, so ~$30/month (~$360/year). Break-even arithmetic (assumption:
10,000 non-English journeys a year at the top of the range): $1,500 AI +
$360 hosting = ~$1,900/year in cloud. The binding costs are unpriced:
maintainer time, 32-language review, support, legal/privacy review, policy
upkeep. No market rate for any of them was collected - MISSING, not
estimated.

## F2. Regulatory hooks (prior verification only; Oct-2026 status pending)

IRS 501(r) duties (written FAP, web publication, bill notice, translation
threshold "the lesser of 1,000 individuals or 5 percent of the community
served") apply to tax-exempt hospitals only - VERIFIED-VERBATIM in
docs/research/2026-10-17_bill-decoder-crowding.md. So VUMC and Ascension
Saint Thomas (nonprofit) are 501(r) entities; HCA (for-profit) is not.
Nashville General's 501(c)(3) status: not checked. CFPB medical-debt rule,
CMS price transparency, state screening mandates, Tennessee statutes:
pending (merge).

## F3. Comparables and hospital economics

Pending (merge). Only prior figure: Mediloop at $129 per bill (crowding
brief; vendor self-reported; patient-paid, excluded by this brief's premise).

## Models ranked (HYPOTHESIS TABLE until the merge)

| Rank | Model | Who pays | Evidence in hand | Conflict risk | Fit with "nothing stored" |
|---|---|---|---|---|---|
| 1 | Grant-funded pilot (nonprofit or fiscal sponsor) | Foundations | Cloud cost ~$1.9k/yr | Low | High |
| 2 | Flat subscription for NONPROFIT hospitals | VUMC / Ascension class | 501(r) duties verified; prices missing | HIGH - the payer is the creditor | Medium (counts-only dashboard fits; hospitals will want patient-level data) |
| 3 | Licensing to portal / PFS vendors | Cedar, Flywire, EHR vendors | none | High (paid on collections) | Low-medium |
| 4 | Dollar For-style nonprofit | Donors | 990 pending | Low | High |
| 5 | Government contract (Metro Nashville / state) | Public budget | none | Low-medium | High |
| 6 | Payers / MCOs / employers | Insurers | weak fit (users often uninsured) | Medium | Medium |
| X | Contingency fee on patient savings | Patient | excluded | Unacceptable | n/a |

Conflict mitigations for any hospital-paid model: the rules engine and every
policy citation stay public; the hospital supplies only its published FAP;
the result shows before any hospital-branded step; "not eligible" always
shows the payment-plan contact and outside help; contracts forbid
patient-level data (counts only, under-10 suppression - already built);
annual aggregate audit; flat price per hospital, never per approval or per
dollar collected; prefer nonprofit hospitals.

## Recommended path (conditional on the merge)

1. Months 0-2: finish the evidence; measure real per-journey OCI cost with
   the Usage API over 20 synthetic journeys; settle the owner and a fiscal
   sponsor.
2. Months 1-4: one small Tennessee or national health-equity grant sized to
   cloud + a part-time maintainer + translation review.
3. Months 3-9: one no-fee pilot with a nonprofit Nashville hospital (VUMC or
   Ascension Saint Thomas; Nashville General as a safety-net partner if its
   status fits; HCA last). Metric: completed FAP applications per 100 QR
   scans, by language, counts only.
4. Months 9-12: a paid flat subscription only if the pilot shows more
   completed applications and the conflict terms are signed.

## Verification table

| Load-bearing claim | Source | Verdict |
|---|---|---|
| Large Cohere $0.0156 per 10,000 characters | price list (browser text) + API JSON B108077 | VERIFIED-VERBATIM (2 calls, 1 vendor) |
| 1 transaction = 1 character; prompt + response | price list + docs | VERIFIED-VERBATIM |
| Command A Vision bills as Large Cohere | docs | VERIFIED-VERBATIM |
| Image billing in characters | docs | NOT-FOUND (confirmed by a text read) - cost UNKNOWN |
| Translation $10.00 per 1,000 transactions after 1,000 | price list + API JSON B95920 | VERIFIED-VERBATIM |
| 1 translation transaction = up to 1,000 chars per call | archived page 2025-12-06 | VERIFIED-VERBATIM (archived, may be stale) |
| E5 $0.03 OCPU-h, $0.002 GB-h | price list + API JSON | VERIFIED-VERBATIM |
| 501(r) applies to tax-exempt hospitals only | irs.gov via prior brief | VERIFIED-VERBATIM there; not re-fetched |
| Tennessee regulates debt adjusting | TN Commerce PDF | UNREACHABLE (404) - lead only |

## Numbers register (first run)

| Number | Claim | Source | Date | Interest class | Verdict |
|---|---|---|---|---|---|
| $0.0156 / 10k chars | Large Cohere price | Oracle price list | 2026-10-08 | VENDOR-SELF-REPORTED | VERIFIED-VERBATIM |
| ~1,610 tokens | 512x512 image | Oracle docs | read 2026-10-17 | VENDOR-SELF-REPORTED | VERIFIED-VERBATIM |
| $10.00 / 1,000 tx; first 1,000 free | translation | Oracle price list | 2026-10-08 | VENDOR-SELF-REPORTED | VERIFIED-VERBATIM |
| first 5,000 free | archived page | web.archive.org | 2025-12-06 | VENDOR-SELF-REPORTED | conflicts with 1,000; treat 1,000 as binding |
| $0.03 / $0.002 per hour | E5 OCPU / GB | Oracle price list | 2026-10-08 | VENDOR-SELF-REPORTED | VERIFIED-VERBATIM |
| ~$30/month | VM + boot volume | arithmetic | 2026-10-17 | DERIVED | assumptions stated |
| $0.04-$0.15 | non-English journey | arithmetic, chars estimated | 2026-10-17 | DERIVED / UNVERIFIABLE image term | estimate |
| ~$1,900/year | cloud at 10k journeys | arithmetic | 2026-10-17 | DERIVED | assumption-driven |

Structural checks: 100% of verified numbers are Oracle list prices
(disclosed in the TL;DR); the API JSON and the HTML page are two calls to one
vendor, not two independent sources.

## Thin / missing (first run)

- Comparables' 990s and vendor pricing; presumptive-screening prices (the
  number that most decides H1); AHA and Nashville-system charity care and
  bad debt; Oct-2026 regulation status - pending merge.
- OCI image billing (absent from the docs) - measure with the Usage API.
- Whether OCI Language bills each batch document separately - the estimate
  assumes per document (conservative).
- Price of human review for 32 languages - not searched.
- Willingness to pay of any Nashville hospital or funder - needs interviews.

## What would change this conclusion

- Cheap, multilingual incumbent presumptive screening -> H1 weakens.
- Evidence that higher FAP enrollment lowers bad debt and collection cost
  more than it costs -> H1 strengthens.
- An active Tennessee medical-debt / health-access funder -> H2 concrete.
- Measured image cost far above $0.09 -> cost per user moves toward dimes.
- Building F11.7 push reminders (server storage) -> compliance cost rises.

## Sources (read 2026-10-17)

- https://www.oracle.com/cloud/price-list/ (browser text)
- https://apexapps.oracle.com/pls/apex/cetools/api/v1/products/?currencyCode=USD (JSON, lastUpdated 2026-10-08T14:38:16Z)
- https://docs.oracle.com/en-us/iaas/Content/generative-ai/pay-on-demand.htm
- https://docs.oracle.com/en-us/iaas/Content/generative-ai/cohere-command-a-vision-07-2025.htm
- https://web.archive.org/web/20251206133447id_/https://www.oracle.com/artificial-intelligence/language/pricing/
- https://docs.cohere.com/docs/image-inputs (WebFetch; CLOSE-PARAPHRASE; not load-bearing)
- tn.gov Commerce debt-adjusting PDF (404, UNREACHABLE)
- Project files: PRD_ROADMAP.md, docs/research/2026-10-17_bill-decoder-crowding.md, .claude/project-memory/budget.md and operations.md, app/main.py, app/oci_client.py, app/data/policy_cumberland_synthetic.json

## Merge

(pending - comparables, hospital economics, regulation status, funders)
