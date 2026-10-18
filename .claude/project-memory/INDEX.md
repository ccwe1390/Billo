# project-memory index - TNHacks26

Read first: important.md - 6 critical entries (updated 2026-10-17)

Knowledge:
- decisions.md - module, users, metric, languages, scope (updated 2026-10-17)
- gotchas.md - Synthea threading nondeterminism, moving jar tag, no adjustments, Java path (updated 2026-10-17)
- people.md - roles, deciders, collaborators, orgs (updated 2026-10-17)
- timeline.md - event agenda; hacking ends Sun 1:00 PM; venue closes Sat 9 PM (updated 2026-10-17)
- glossary.md - easily confused terms (updated 2026-10-17)
- compliance.md - track rules; full event rules not yet seen (updated 2026-10-17)
- budget.md - $500 OCI credits, $0 personal ceiling; expiry and account unknown (updated 2026-10-17)
- disclosure.md - what may leave the project (updated 2026-10-17)

Running systems:
- operations.md - one OCI VM (FastAPI behind Apache), deploy log; no jobs/backups by design (updated 2026-10-18)
- services.md - OCI services in use (Generative AI, Language, one VM) + starter-kit facts (updated 2026-10-17)

Output:
- experiments.md - live model runs (gate 1, blur test, translations); the precision/recall plan is superseded (updated 2026-10-17)
- writing.md - venues, style/voice, citations, submission status (updated 2026-10-17)

Physical:
- hardware.md - parts/BOM, wiring, CAD, purchase gating (updated 2026-10-17)

Code:
- architecture.md - pointer to HANDOFF + contracts.md (updated 2026-10-17)
- conventions.md - cents, ISO dates, el()/fill(), string markers (updated 2026-10-17)
- dependencies.md - pinned Python requirements; JDK 17 + Synthea jar with hashes (updated 2026-10-17)
- testing.md - framework, layout, coverage/frozen rules (updated 2026-10-18)
- tooling.md - build/lint/format/CI + required commands (updated 2026-10-17)
- data.md - Synthea snapshot command, row counts, determinism, adjustment gap (updated 2026-10-17)
- security.md - pointer: limits, headers, auth model (updated 2026-10-17)
- features.md - built vs not built (updated 2026-10-18)
- performance.md - journey timing (updated 2026-10-17)
- ui.md - accessibility, RTL, design/asset/a11y evidence rules (updated 2026-10-17)

Project-specific bins:
- languages.md - language ranking evidence + OCI Language support per language (updated 2026-10-17)

Stubs (first line STATUS): writing, hardware (empty/N/A); architecture, conventions, features, performance, security, testing, tooling (one-line pointers)

Map (not a bin - see SKILL section 5.1):
- DIRECTORY.md - not built (103 tracked files; the app is 4 Python modules + one JS file)

Cross-bin invariants:
- Synthetic/public/de-identified data only; no autonomous diagnosis or treatment (important.md 1-2).
- Dates are known (important.md 3: hacking ends Sun 2026-10-18 1:00 PM CDT); OCI works; the team roster is still unconfirmed.
