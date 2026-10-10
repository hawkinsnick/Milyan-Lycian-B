# Milyan (Lycian B) Corpus

Research-oriented, provenance-first corpus for Milyan, also called Lycian B. Milyan is distinct from Lycian A; 'Lycian B' is an alternative designation, not a second language.

## Status
Initial scaffold (0.1.0). **No inscriptions have yet been verified or transcribed.** Empty datasets must not be interpreted as evidence of absence.

## Scope and standards
- Primary inscription catalog with stable identifiers, object provenance, dating, and bibliography.
- Diplomatic transcription and normalized transliteration kept separate.
- Record damaged, uncertain, restored, and disputed signs explicitly.
- Every linguistic interpretation requires source attribution and confidence/uncertainty metadata.
- Distinguish attested data from scholarly hypotheses and machine-generated suggestions.
- Respect source copyrights and permissions; bibliographic metadata alone does not license reproduction.

## Dataset
`data/inscriptions.json` starts as an empty verified catalog. See `docs/METHODOLOGY.md` and `schemas/inscription.schema.json` before contributing.

## Licensing
Project-original code is covered by PolyForm Noncommercial 1.0.0; copyrightable project-original corpus content and documentation are CC BY-NC 4.0, to the extent contributors own the rights. See `LICENSE`, `LICENSE-CODE`, `LICENSE-CONTENT.md`, `LICENSING.md`, and `NOTICE`. **Third-party source editions, transcriptions, images and datasets are not relicensed**, and each requires source-specific rights verification before redistribution.

## AI skill
See `skills/milyan/SKILL.md`. The master corpus registry lists this repository as a **pending admission candidate**, not a validated scholarly corpus. See `corpus-factory/CORPUS-ADMISSION-CONTRACT.md`.

## Corpus inventory checkpoint
Three provisional segment records (TL 44c, TL 44d, TL 55) cover two monuments. Zero verified text transcriptions. See `docs/COVERAGE.md`, `docs/SOURCES.md`, `ai-skill/SKILL.md` and `research/pre-expert-maximum.json`. This is **not yet** a scholarly text-level 1.0 release.

## Reproducible validation and 1.0 gates

Run `python scripts/validate_corpus.py` and `python ai-skill/scripts/validate_bundle.py`. GitHub Actions runs both on push and pull requests. See `docs/RELEASE-GATES.md`, `docs/RESEARCH-WORKFLOW.md`, `docs/INTEROPERABILITY.md`, and `docs/REVIEW-HANDOFF.md`. Passing structural validation is not the same as verifying epigraphic readings.

## Research API and source reconciliation

The read-only [research API](docs/RESEARCH-API.md) provides inscription search, coverage, KWIC, and exports. The [source reconciliation matrix](research/source-reconciliation.json) tracks edition access, rights and reading verification. The line layer is intentionally empty until verified source readings can be entered; no linguistic inference is warranted from empty results.

Fleet research-contract implementation and replay: [admission guide](docs/FLEET-ADMISSION.md).
