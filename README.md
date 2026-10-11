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

## Populated eDiAna reference layer
Read `docs/EDIANA-REFERENCE.md`, `research/reference-manifest.json` and `research/ediana-reference-crosswalk.json` before using `data/reference/records.json` or `data/reference/lines.json`. Two frozen digital catalogue entries provide 114 text rows (TL 55: 9; TL 44c: 34; TL 44d: 71). Preserve source strings and source authorship. These are source-attributed digital readings, not independently verified diplomatic readings or additional physical objects. Default API canonical queries remain separate; request `--layer reference` explicitly. The source and derived component retain CC-BY-SA-4.0 with original eDiAna hyperlinks and primary-edition attribution, irrespective of project-original NC terms. Readings, lemmas and source annotations are attributed claims.

The EpiDoc reference export round-trips every derived line field and exact source text. All 57 pinned upstream patterns execute; no invented graphical apparatus, physical certification or expert acceptance follows. The frozen-cache acquisition and failed live retrieval are explicit; future source changes require a reviewed new snapshot. Replay `python scripts/build_reference.py`, the pinned upstream validator, and `python ai-skill/scripts/validate_bundle.py` before use. Remaining primary-edition collation and variant acquisition are work items, not proof of exhaustion.

### Primary edition locator controls
`research/primary-edition-locator-control.json` records visual inspection of the Getty/Internet Archive Kalinka 1901 scan. TL 44c/d facsimiles are on printed p.41; the relevant transliterations are on p.43 (c32–65 and d1–53) and p.44 (d54–71). TL 55 is introduced on p.53 and illustrated/transliterated on p.54. Printed page and PDF ordinal are separate fields. The historical eight-line description of TL 55 differs from nine frozen eDiAna rows; preserve the discrepancy without forcing row-to-physical-line equality. Keep broad bibliography verbatim while using precise observed locators. This scan belongs to the same source genealogy; no new independent witness, exact reading equivalence or expert acceptance follows.
