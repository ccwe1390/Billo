# important - TNHacks26

> Critical facts: getting one wrong is irreversible or expensive, invalidates
> results, or breaks a live external constraint. Numbered, dated, newest last.
> CLAUDE.md wins on conflict. Never remove an entry without telling the user.
> Keep entries short; detail lives in the topic bin. ASCII only.

## 1. No autonomous diagnosis or treatment (2026-10-17)
**What:** The track forbids solutions that make autonomous diagnostic or
treatment decisions. Human oversight must be designed in from the start.
**Constrains:** No feature may output a diagnosis, a treatment choice, or a
triage verdict presented as a decision. AI output informs or routes; a person
decides. Prompts, UI copy, and the demo must show that.
**Why:** It is a stated track rule and part of the "thoughtful, responsible use
of AI" success criterion; breaking it fails the track's premise.
**Source:** pasted Track 2 text ("Responsible innovation"), Evan's message
2026-10-17; detail in compliance.md.

## 2. Synthetic, public, or de-identified data only (2026-10-17)
**What:** Only synthetic, public, or appropriately de-identified data may be
used.
**Constrains:** No real patient records or identifiable health information in
the repo, prompts, logs, screenshots, or the demo. Generate or source safe
data first; label its origin in the repo.
**Why:** Stated track rule; health data is sensitive and a leak cannot be
undone once committed, pushed, or sent to a cloud service.
**Source:** pasted Track 2 text ("Responsible innovation"); detail in
compliance.md and disclosure.md.

## 3. Hacking finishes Sun 2026-10-18 1:00 PM CDT; venue closes Sat 9:00 PM (updated 2026-10-17 ~13:00)
**Update (supersedes the MISSING text below):** per `docs/Hackathon Schedule.txt`, hacking finishes Sun 2026-10-18 1:00 PM, showcase 1:05 PM, final pitches 3:30 PM; Saturday bump-out (venue closes) 9:00 PM, Sunday doors 9:00 AM. Judging criteria in `docs/rubric.txt`. Submission requirements still UNKNOWN. Full agenda in timeline.md.
**Update 2026-10-17 ~13:47:** team plan rev 2 says 12:00 PM / 8 PM; Evan ruled `docs/Hackathon Schedule.txt` is ground truth, so 1:00 PM finish and 9:00 PM venue close stand.
**Original entry (2026-10-17), kept for history:**
**What:** MISSING - the submission deadline, event dates, judging rubric, and
submission format were not provided; only the track text exists.
**Constrains:** Do not plan a schedule or claim a deadline until Evan supplies
them. Treat every date as unknown.
**Why:** A missed or wrongly assumed deadline loses the whole submission.
**Source:** HANDOFF.md "What is known vs missing"; detail in timeline.md.

## 4. OCI is mandatory (2026-10-17)
**What:** The project MUST use Oracle Cloud Infrastructure (Evan, chat
2026-10-17). Not just a judging plus: a requirement.
**Constrains:** The AI parts (extraction, explanation, translation, letter
drafting) run on OCI services, not another provider's API. A non-OCI service
needs Evan's explicit OK. OCI access (account, credits, region with
Generative AI) is BLOCKED-ON-EVAN until he confirms it.
**Why:** Building on another provider would mean a rebuild, or a submission
that misses the requirement.
**Source:** Evan's message 2026-10-17; detail in compliance.md and services.md.
**Update 2026-10-17 16:50 CDT:** OCI access is no longer blocked: the
account, the VM and Generative AI + Language calls all work (services.md).

## 5. OCI credits: $500, hard cap (2026-10-17)
**What:** The team has $500 in OCI credits (Evan, chat 2026-10-17). Evan's
personal spend ceiling beyond that is $0 (EVAN_CONTEXT.md section 3).
**Constrains:** Set an OCI budget alert well below $500 before the first paid
call. No batch or load run without a cost estimate first. Cache model outputs
during development instead of re-calling.
**Why:** If a card is on file, spend past the credits becomes real charges.
**Source:** Evan's message 2026-10-17; detail in budget.md.

## 6. OCI home region must be US Midwest (Chicago) - permanent (2026-10-17)
**What:** The OCI starter kit says to pick US Midwest (Chicago) as the Home
Region at sign-up, and that it cannot be changed later. Sign up with the same
email that the hackathon promotional credits go to; customer type Individual.
**Constrains:** M0.1 account creation. Wrong region or email cannot be undone
and may strand the $500 credits.
**Why:** Irreversible account setting.
**Source:** github.com/ScottStroz/oci-hackathon-starterkit README (read 2026-10-17; third-party kit, not confirmed as TNHacks26-official); detail in services.md.
