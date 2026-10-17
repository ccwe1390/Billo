# languages - TNHacks26

Which languages the Bill Decoder explains bills in, and the evidence. Searched
2026-10-17. Explanations are in the user's language; appeal letters stay in
English (for the provider).

## US ranking evidence (sourced only - nothing filled by guess)
- 2019 ACS (Census story, 2022-12): top 5 non-English home languages are
  Spanish, Chinese, Tagalog, Vietnamese, Arabic. Share speaking English less
  than "very well": Vietnamese 57%, Chinese 52%, Spanish 39%, Arabic 35%,
  Tagalog 30%.
  https://census.gov/library/stories/2022/12/languages-we-speak-in-united-states.html
- LEP (limited English proficient) ranking, MPI tabulations of ACS: 2010 and
  2018 both give Spanish, Chinese, Vietnamese, Korean, Tagalog, Arabic as the
  top 6 (2010: Spanish ~16.5M, Chinese ~1.5M, Vietnamese ~836k, Korean ~635k,
  Tagalog ~489k, Arabic ~321k).
  https://www.nationalcapacd.org/wp-content/uploads/2020/06/COVID-19-LEP-by-Language-UPDATED-with-012221-data.docx.pdf
- MPI 2022: 26.5M LEP (8.4% of population); top 5 = Spanish + four Asian
  languages, >75% of LEP. Which four not extracted.
  https://www.migrationpolicy.org/sites/default/files/publications/USCCR-Hofstetter-Testimony-March2025-FINAL.pdf
- Ranks 7-10: MISSING. Source to use: ACS table C16001 (needs a free Census API
  key) or the MPI US language profile page (403 to automated fetch).
- Hindi: not in the top 5 home languages (2019) nor the top 6 LEP (2010, 2018).

## OCI Language translation support (OCI CLI reference, target codes, 2026-10-17)
- Listed: ar, zh-CN, zh-TW, es, vi, ko, ru, fr, fr-CA, pt, pt-BR (+ 20 others).
- NOT listed: Hindi (hi), Tagalog (tl), Haitian Creole (ht). These would rely on
  an OCI Generative AI model alone, with no OCI Language back-translation check.
  https://docs.oracle.com/en-us/iaas/tools/oci-cli/latest/oci_cli_docs/cmdref/ai/language/batch-language-translation.html

## Build notes
- Arabic is right-to-left: UI and generated text need RTL layout.
- Chinese: OCI lists both Simplified (zh-CN) and Traditional (zh-TW).

## 2026-10-17 - OCI Language list confirmed (31 languages)
- Oracle docs "Supported Languages" (one table for Oracle Translate as a whole)
  lists 31, identical to the CLI list above, including Vietnamese (vi) and
  Slovenian (sl). https://docs.oracle.com/en-us/iaas/language/using/translate.htm
- A 29-entry list Evan pasted (source not named) omits vi and sl; the two
  Oracle sources both include them, so vi is treated as supported (verify with
  a live call once OCI access exists).
- Hindi, Tagalog, Haitian Creole: absent from all three lists.

## 2026-10-17 - Wave 1 decided (Evan)
- Wave 1: Spanish (es), Chinese (zh-CN + zh-TW), Arabic (ar, RTL), Vietnamese (vi).
- Hindi: additional option, OCI Generative AI only; mark its output as not
  back-translation-checked.
