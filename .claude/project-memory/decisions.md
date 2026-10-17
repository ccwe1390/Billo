# decisions - TNHacks26

Standing decisions (what is decided NOW). History lives in the record.

- 2026-10-17 - Track 2, "Health Access, Equity & Experience", is the chosen track.
  Reason: not given. Decided by: the team, as relayed by Evan in chat; team
  membership unknown.
- 2026-10-17 - No problem, user group, or measurable outcome is chosen yet. This is
  the next decision (HANDOFF.md, Next actions).
- 2026-10-17 - Build ONE module: the Bill Decoder (photo or file of a hospital
  bill + EOB -> line-by-line plain explanation, flagged likely errors, drafted
  appeal or itemized-bill request). Discharge Companion and Med nudges are
  dropped for this event. Reason: only module with exact ground truth (we write
  the synthetic bills and inject the errors) and no clinical-risk surface; the
  track says go deep on one problem. Decided by: Evan, chat 2026-10-17.
  Still open: user group/equity hook, metric, scope, rules source.
- 2026-10-17 - Language scope: target the top 10 US immigrant languages; first
  wave Spanish, Chinese, Arabic (Evan). Hindi was in Evan's first wave; open
  question raised: Hindi is not top-ranked for LEP and is not in OCI Language's
  translation list (see languages.md). Ranks 7-10 not yet sourced.
  Decided by: Evan, chat 2026-10-17.
- 2026-10-17 - Mission and scope set (Evan, answers to 6 questions):
  (1) mission is the internal north star first; pitch copy derived later.
  (2) users = limited-English/low-income patients AND the family member who
  reads the bill. (3) wave-1 languages = Spanish, Chinese, Arabic, Vietnamese;
  Hindi is an additional option (Generative AI only, no OCI Language check).
  Supersedes the Hindi-open part of the language entry above. (4) headline
  metric = precision/recall on planted errors in synthetic bills; demo number
  = dollars flagged on the same set; no real-world savings claim.
  (5) financial-assistance check = add-on if time allows. (6) product name =
  placeholder. Mission text lives in HANDOFF.md Goal.
