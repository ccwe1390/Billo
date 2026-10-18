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

## 2026-10-17 ~14:00 CDT - Tiers revised (Evan) and support re-verified
- Evan: Chinese (zh-CN, zh-TW) moves to tier 1 (translated interface) with
  en, es, ar. Tier 2 = "the rest of the US top 10" per a list Evan pasted
  (source not named): Spanish ~42M, Chinese ~3.5M, Tagalog ~1.7M,
  Vietnamese ~1.5M, Arabic ~1.3-1.4M, French (incl. French Creole and
  Cajun) ~1.2M, Korean ~1.1M, Russian ~1M, German. Its top 5 match the
  Census 2019 story above; ranks 6-9 are from Evan's paste only.
- Tier 2 built: vi, fr, ko, ru, de (+ hi from the earlier decision).
- Support, read 2026-10-17 from vendor pages:
  - OCI Language (31 languages,
    https://docs.oracle.com/en-us/iaas/language/using/translate.htm): has
    ar, zh-CN, zh-TW, es, vi, fr, ko, ru, de; NOT Tagalog, Hindi, Haitian
    Creole, Farsi, Kurdish, Somali, Swahili, Burmese, Amharic, Nepali.
  - Cohere Command A (23 languages, https://docs.cohere.com/docs/command-a):
    English, French, Spanish, Italian, German, Portuguese, Polish, Czech,
    Dutch, Romanian, Greek, Ukrainian, Russian, Japanese, Korean, Chinese,
    Vietnamese, Indonesian, Hindi, Arabic, Hebrew, Persian, Turkish. NOT
    Tagalog. (Oracle's own Command A page names no languages.)
- Gap stated, not built: Tagalog (#3 in the US list) - neither service.
  The "French" census group includes Haitian Creole, which is unsupported;
  our French is French only.
- Risk to test live: machine translation into fr/de/ru/es may reformat
  numbers ("4.812,40", "4 812,40"); the number lock then rejects the text
  and falls back to English. If that happens often, protect numbers with
  placeholders before translating.
- 2026-10-17 20:13 CDT - SUPERSEDES the tier lists above (record AI, Evan):
  32 languages = the 31 Oracle Translate codes (29 languages; fr/fr-CA,
  pt/pt-BR) + hi, all with a translated interface; list in
  app/data/languages.json. 27 interface files machine-translated by OCI (hi
  by Command A), unreviewed; 118 keys each after more_langs was removed, minus
  12 dropped meaning-flipped strings (3,174 strings shipped). Back-translation
  check (OCI Language, 3 safety keys x 26 languages): r_decides went past
  tense in cs/he/ja/th/tr/vi, Thai notice lost its negation, home_estimate
  became "reduce TO" in he/hr/it/ru/sk. Guard: tSafe shows English under 10
  safety keys; the flipped strings are English only. Explanation route:
  OCI Language for da, hr, hu, no, sk, sl, fi, sv, th (outside Command A's
  documented languages), Command A for the rest.
