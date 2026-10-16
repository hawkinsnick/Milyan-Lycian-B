# Milyan (Lycian B) Corpus

<!-- CURRENT-STATUS:START -->
## Current evidence status

Populated, frozen eDiAna reference layer; structural fleet admission is distinct from scholarly acceptance. 2 digital catalogue records provide 114 source text rows across 3 provisional segments on 2 reported monuments. Canonical verified readings: 0; independent reviews: 0. TL 55 count voices are accounted: a quoted historical eight-line description and nine printed edition entry groups. Schürr2005 first documentary comparison pass covers all nine revised lines and74 apparatus entries, with all four literal digital break markers accounted for. Six selected issues retain focused dossiers. The encoded-sign comparison now exhaustively accounts for1348 reference units and1233 source print positions in1441 candidate alignment records, including36 ambiguous records. Documentary review of all152 flagged records is complete in58 source-located cases, retaining range-only correspondences without invented unique pairings. The expert packet is prepared; full epigraphic certification and external adjudication remain open.

Authorities: [reference manifest](research/reference-manifest.json) and [remaining gates](research/pre-expert-maximum.json). Reference rows are not independently certified physical lines.
<!-- CURRENT-STATUS:END -->

Research-oriented, provenance-first corpus for Milyan, also called Lycian B. Milyan is distinct from Lycian A; 'Lycian B' is an alternative designation, not a second language.

## Evidence layers
Canonical verified transcriptions remain absent; the separately attributed digital reference layer is populated. Empty canonical results must not be interpreted as evidence of absence.

## Scope and standards
- Primary inscription catalog with stable identifiers, object provenance, dating, and bibliography.
- Diplomatic transcription and normalized transliteration kept separate.
- Record damaged, uncertain, restored, and disputed signs explicitly.
- Every linguistic interpretation requires source attribution and confidence/uncertainty metadata.
- Distinguish attested data from scholarly hypotheses and machine-generated suggestions.
- Respect source copyrights and permissions; bibliographic metadata alone does not license reproduction.

## Dataset
`data/inscriptions.json` contains the provisional bibliographic segment inventory. See `docs/METHODOLOGY.md` and `schemas/inscription.schema.json` before contributing.

## Licensing
Project-original code is covered by PolyForm Noncommercial 1.0.0; copyrightable project-original corpus content and documentation are CC BY-NC 4.0, to the extent contributors own the rights. See `LICENSE`, `LICENSE-CODE`, `LICENSE-CONTENT.md`, `LICENSING.md`, and `NOTICE`. **Third-party source editions, transcriptions, images and datasets are not relicensed**, and each requires source-specific rights verification before redistribution.

## AI skill
Use `ai-skill/SKILL.md`; `skills/milyan/SKILL.md` is the legacy instruction path. The master corpus registry structurally admits this repository through its native contract adapter; this does not certify readings or scholarly completeness. See `corpus-factory/CORPUS-ADMISSION-CONTRACT.md`.

## Corpus inventory checkpoint
Three provisional segment records (TL 44c, TL 44d, TL 55) cover two monuments. Zero verified text transcriptions. See `docs/COVERAGE.md`, `docs/SOURCES.md`, `ai-skill/SKILL.md` and `research/pre-expert-maximum.json`. This is **not yet** a scholarly text-level 1.0 release.

## Reproducible validation and 1.0 gates

Run `python scripts/validate_corpus.py` and `python ai-skill/scripts/validate_bundle.py`. GitHub Actions runs both on push and pull requests. See `docs/RELEASE-GATES.md`, `docs/RESEARCH-WORKFLOW.md`, `docs/INTEROPERABILITY.md`, and `docs/REVIEW-HANDOFF.md`. Passing structural validation is not the same as verifying epigraphic readings.

## Research API and source reconciliation

The read-only [research API](docs/RESEARCH-API.md) provides inscription search, coverage, KWIC, and exports. The [source reconciliation matrix](research/source-reconciliation.json) tracks edition access, rights and reading verification. The canonical verified line layer is intentionally empty; request `--layer reference` for populated source-attributed rows. No linguistic inference is warranted from an empty canonical result.

Fleet research-contract implementation and replay: [admission guide](docs/FLEET-ADMISSION.md).

## Populated eDiAna reference layer
Read `docs/EDIANA-REFERENCE.md`, `research/reference-manifest.json` and `research/ediana-reference-crosswalk.json` before using `data/reference/records.json` or `data/reference/lines.json`. Two frozen digital catalogue entries provide 114 text rows (TL 55: 9; TL 44c: 34; TL 44d: 71). Preserve source strings and source authorship. These are source-attributed digital readings, not independently verified diplomatic readings or additional physical objects. Default API canonical queries remain separate; request `--layer reference` explicitly. The source and derived component retain CC-BY-SA-4.0 with original eDiAna hyperlinks and primary-edition attribution, irrespective of project-original NC terms. Readings, lemmas and source annotations are attributed claims.

The EpiDoc reference export round-trips every derived line field and exact source text. All 57 pinned upstream patterns execute; no invented graphical apparatus, physical certification or expert acceptance follows. The frozen-cache acquisition and failed live retrieval are explicit; future source changes require a reviewed new snapshot. Replay `python scripts/build_reference.py`, the pinned upstream validator, and `python ai-skill/scripts/validate_bundle.py` before use. Remaining primary-edition collation and variant acquisition are work items, not proof of exhaustion.

### Primary edition locator controls
`research/primary-edition-locator-control.json` records visual inspection of the Getty/Internet Archive Kalinka 1901 scan. TL 44c/d facsimiles are on printed p.41; the relevant transliterations are on p.43 (c32–65 and d1–53) and p.44 (d54–71). TL 55 is introduced on p.53 and illustrated/transliterated on p.54. Printed page and PDF ordinal are separate fields. The historical eight-line description of TL 55 differs from nine frozen eDiAna rows; preserve the discrepancy without forcing row-to-physical-line equality. Keep broad bibliography verbatim while using precise observed locators. This scan belongs to the same source genealogy; no new independent witness, exact reading equivalence or expert acceptance follows.

## AI integrity checkpoint — 2026-10-11

[AI integrity controls](docs/AI-INTEGRITY.md) document source-bound bundle publication and checked cross-corpus dependency safeguards. Reading coverage and scholarly acceptance are unchanged.

[TL 55 count reconciliation and remaining reading limits](docs/TL55-COUNT-RECONCILIATION.md).

## Evidence and alternative-reading queries

[Query source evidence and unresolved alternatives](docs/EVIDENCE-AND-ALTERNATIVES.md) using exact native IDs, full source records, pinned artifact locators and explicit corpus-specific scope. [Coverage by native view](analysis/evidence-query-coverage.json) keeps catalogue entries, reading versions, assertions and research issues distinct. This interface adds no source collation, canonical reading or expert acceptance.

## Schürr2005 TL55 comparison

Read `research/schuerr2005-tl55-collation.json`, `research/tl55-qualified-collation.json` and `docs/SCHUERR2005-TL55-COLLATION.md`. The author-posted PDF is acquired and hash-pinned. Revised labels1–9 and their apparatus pages are located; six selected source differences are qualified. Keep documentation, revised transcription/apparatus and poetic reconstruction distinct. Preserve doubtful forms, alternatives, emendations, literal reference strings and row-boundary allocation. `research_api.py collation` exposes the qualified view; a row without an issue is not fully collated. Source access does not license bulk republication, unattributed PDF overlays are excluded, and raw extracted glyphs are not authoritative. All114 reference rows remain unchanged; verified canonical readings and independent reviews remain zero.


TL55 review coverage now extends to all9 revised lines and74 apparatus entries; all4 digital break markers are accounted for. The [review packet](review/tl55-independent-review.json) is prepared, with expert adjudication and full sign-level collation still open. [Current comparison guide](docs/SCHUERR2005-TL55-COLLATION.md).

Bounded attribution and comparison review: [source qualifications and remaining gaps](docs/ATTRIBUTION-REVIEW.md).


[TL55 exhaustive encoded-sign comparison](docs/TL55-SIGN-COMPARISON.md): all reference and source print positions accounted for;36 ambiguous candidate alignment records retained. Query `research_api.py signs`; expert adjudication and epigraphic certification remain open.


[TL55 documentary comparison completed](docs/TL55-DOCUMENTARY-COMPLETION.md): all152 flagged comparisons now have source-located assessments, with every algorithmic ambiguity explained or retained as a non-unique range. Independent expert adjudication remains open.


## 2026-10-16 — TL44 source checkpoint

Two modern TL44 edition identities are confirmed from pinned publisher-deposited metadata. All105 existing TL44 digital row labels have Kalinka page routes, with three selected boundary/inventory observations. Modern article PDFs and full sign/apparatus comparison remain pending; West pagination stays unresolved. All114 frozen rows and canonical zero are unchanged. [Source evidence and next actions](docs/TL44-SOURCE-CHECKPOINT.md).
