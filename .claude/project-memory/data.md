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
- 2026-10-17 - SUPERSEDES the "Java is NOT installed" line above: Temurin
  JDK 17.0.20.1+1 is now installed portably at
  `C:\Users\daruw\tools\jdk-17.0.20.1+1\` (not on PATH; call
  `...\bin\java.exe` by full path).
- 2026-10-17 - Canonical Synthea snapshot: `data/synthea/s42-p10-r20261017-t1/`
  (gitignored), made with:
  `java -jar C:\Users\daruw\tools\synthea-with-dependencies.jar -s 42 -cs 42
  -p 10 -r 20261017 --exporter.baseDirectory=./ --exporter.csv.export=true
  --exporter.fhir.export=false --generate.thread_pool_size=1`
  Rows (excluding header): claims_transactions 7400 (CHARGE 2242, PAYMENT
  2906, TRANSFERIN 1126, TRANSFEROUT 1126), claims 686, encounters 515,
  patients 11 (10 alive + 1 dead), payers 10, procedures 1386. Per-file
  sha256 in `data/synthea/s42-p10-r20261017-t1.sha256`.
- 2026-10-17 - DETERMINISM: with default threading, two runs with the same
  seed gave different files (row order everywhere; claims_transactions IDs
  and payers.csv totals actually differ). With
  `--generate.thread_pool_size=1`, two runs were byte-identical on every CSV.
  Always pass it.
- 2026-10-17 - GAP for error type 3: the snapshot has ZERO rows with a nonzero
  ADJUSTMENTS amount, so Synthea gives us no contractual adjustments. M1.3 must
  generate them (design not decided).
