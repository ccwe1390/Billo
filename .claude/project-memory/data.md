# data - TNHacks26

- 2026-10-17 - Bill source = Synthea CSV export (decisions.md). Files we use:
  `claims_transactions.csv` (Type CHARGE/PAYMENT/ADJUSTMENT/TRANSFERIN/
  TRANSFEROUT, Amount, Unit Amount, Payments, Adjustments, Outstanding,
  Procedure Code, Patient Insurance ID), `claims.csv` (Outstanding1/2/P,
  Status1/2/P, Diagnosis1-8), `encounters.csv` (Total_Claim_Cost,
  Payer_Coverage), `payers.csv`.
  Source: https://github.com/synthetichealth/synthea/wiki/CSV-File-Data-Dictionary
- Procedure codes in Synthea are SNOMED-CT. US bills show CPT/HCPCS: we keep
  our own small SNOMED -> CPT/HCPCS mapping table (descriptions in our own
  words; CPT descriptor licensing unverified).
- Synthea needs Java to run. Java is NOT installed on Evan's machine
  (checked 2026-10-17). Alternative: a prebuilt Synthea sample dataset
  (download needs Evan's OK).
