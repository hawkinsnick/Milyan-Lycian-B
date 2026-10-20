## AI skill validation — 2026-10-20 (contract remains 0.3.1)

- Add executable skill checks, exact native lookup examples and a GitHub check receipt.
- Fingerprint operational skill files and retain source-specific evidence limits.
- Return a structured rejection for invalid/missing evidence requests.

# Changelog

## 0.1.0 — initial scaffold
- Added research methodology, machine-readable empty catalog, inscription schema, and corpus AI skill.
- No primary inscription content has been imported or verified.
- Master AI skill integration remains pending.

## 0.2.0 — evidence inventory and AI integration checkpoint
- Registered TL 44c, TL 44d and TL 55 as provisional, source-attributed targets (two monuments).
- Added corpus research skill, authority profile, generated index, coverage, source bibliography and validation script.
- Added master AI registry entry with admission PENDING; no verified text yet.

## Evidence-tooling checkpoint
- Added machine-readable source-reconciliation matrix and line-level schema.
- Added read-only research API, coverage, KWIC, JSON/CSV exports and API smoke tests.
- Updated AI skill and research bundle index; scholarly text verification remains blocked.

## 2026-10-11 — current-summary reconciliation
Generate the current README summary from native authorities and reject drift in CI. Update individual skill authority routing; retain historical research gates and release scope.

## Unreleased — AI integrity checkpoint

Require checked native dependency projections, preserve corpus-native bundle schemas, and publish synchronized bundles only on their validated source parent. Add Git race and hostile dependency tests; no new readings or expert acceptance.

## TL55 count reconciliation — 14 October 2026

Read `research/tl55-count-reconciliation-2026-10-14.json` and `docs/TL55-COUNT-RECONCILIATION.md`. Attribute eight to Texier quoted by Kalinka p.53; p.54 has nine transliteration entry groups, including the short final group, matching the nine frozen reference rows in count. Preserve differing boundary allocation, unchanged source strings and the historical quotation. This accounts for source count voices; it does not certify nine physical lines, exact full-reading equivalence, independent witness or accepted readings.

Validation now rebuilds the native AI bundle before checking its authority hashes, so newly declared source authorities are checked in the source commit CI. Publication still uses the exact checked source parent.

## 2026-10-15 — Native evidence and alternative-reading queries

Added pinned native evidence profiles, exact-ID/JSON-pointer queries, coverage replay, loss/corruption/identity/path tests and CI. Updated researcher documentation, AI instructions and evidence bundle indexing. Existing source data and scientific acceptance states are unchanged.

## Schürr2005 TL55 comparison

Read `research/schuerr2005-tl55-collation.json`, `research/tl55-qualified-collation.json` and `docs/SCHUERR2005-TL55-COLLATION.md`. The author-posted PDF is acquired and hash-pinned. Revised labels1–9 and their apparatus pages are located; six selected source differences are qualified. Keep documentation, revised transcription/apparatus and poetic reconstruction distinct. Preserve doubtful forms, alternatives, emendations, literal reference strings and row-boundary allocation. `research_api.py collation` exposes the qualified view; a row without an issue is not fully collated. Source access does not license bulk republication, unattributed PDF overlays are excluded, and raw extracted glyphs are not authoritative. All114 reference rows remain unchanged; verified canonical readings and independent reviews remain zero.


## TL55 complete first documentary pass

Read `research/tl55-first-pass-review.json` and `review/tl55-independent-review.json` together with the original checkpoint. All9 revised source lines and74 apparatus entries now have a completed first comparison pass; counts are7,10,11,10,13,10,5,6,2 by source line. Four digital `//` markers occur in rows2,4,7,8: carryover goes to the following source label and is exposed separately by span. All reference characters and markers are accounted for without normalization; this is allocation accounting, not proof of equivalent readings. Query `research_api.py collation` for row context, original attributed apparatus review notes and span metadata. Six selected issue dossiers remain a bounded subset, not a count of every discrepancy.

The packet is PREPARED_NOT_REVIEWED with null reviewer/assessment and zero accepted readings. A source-coverage inventory is not complete sign-by-sign epigraphic collation, an independent review or expert acceptance. Never close these gates using automated checks, AI-generated review or Schürr’s publication as a new review of this project. No full article interpretation, source independence, physical-line certification, new reading or bulk reuse permission is claimed. Frozen114 reference rows and canonical zero remain unchanged. The original six-issue checkpoint remains immutable historical evidence; use the first-pass register for current review coverage.


## TL55 exhaustive encoded-sign comparison

Read `docs/TL55-SIGN-COMPARISON.md`, `research/tl55-sign-alignment.json` and `review/tl55-sign-adjudication.json`. All nine revised printed lines are compared at glyph/grapheme/notation-unit level:1348 reference units and1233 source print-unit positions, in1441 candidate alignment records. These are mixed editorial/print units, not counts of ancient signs or independent witnesses. All36 records ambiguous across optimal alignment paths stay UNRESOLVED_ALIGNMENT. The152 triage items include qualification and notation differences; they are not152 certified errors or alternative scholarly reading pairs.

Use `python scripts/research_api.py signs --text TL55-L2-A087` or a row/unit ID. Each hit retains literal eDiAna offsets and marks, source page/PDF ordinal/bounding box, comparison method and rights. `--format csv` keeps nested context as JSON. `python scripts/tl55_sign_alignment.py` replays public integrity/coverage; optional `--pdf PATH` checks the exact lawfully held PDF and reruns glyph decoding and all candidate alignments. The PDF hash is mandatory; source glyph mapping is font-specific. PDF underlines must be read as individual drawing segments, not a combined drawing bounding box.

Comparison-only NFC and chi/x conventions do not rewrite source strings or certify literal equality. The p/l alternative, underdots, underlined punctuation, bracket/entity context, nasal-mark differences, layout hyphens and vacat labels remain distinct. Automated matching cannot resolve uncertain repeated signs, establish lexical meaning, accept a reading or count a new independent witness. Full source transcription and images remain outside the repository. Full epigraphic certification and independent external adjudication stay open; original review packets are historical checkpoints, not evidence of completed expert review. All114 frozen reference rows and canonical zero are unchanged.


## TL55 documentary sign comparison completed

Read `docs/TL55-DOCUMENTARY-COMPLETION.md` and `research/tl55-documentary-sign-review.json`. All1441 encoded records remain accounted for; all152 flagged records have58 source-located documentary assessments. All36 algorithmic ambiguity records are reviewed:19 receive positional/notation explanations,2 describe a repeated run without unique point identity and15 retain range-only correspondence. These are overlapping candidate-record categories, not accepted readings, scholarly alternative pairs or ancient-sign totals. No flagged record remains without a documentary disposition.

Use `research_api.py sign-review --text TL55-REVIEW-55`; `signs` now attaches documentary context while preserving the original ambiguity flags. `tl55_documentary_review.py` verifies exact coverage and qualifiers; optional `--pdf PATH` replays the exact source and preferred positional/placeholder correspondences. A restored letter paired to a lacuna slot does not validate that letter. Brackets and colons are not competing letters. A one-to-two repeated-run comparison does not identify a newly recovered ancient sign. Do not erase the original36 algorithmic flags or claim a unique point mapping for the remaining ranges.

This closes the bounded documentary-comparison task for TL55’s revised transcription and apparatus. It does not close independent expert adjudication, monument autopsy, physical-line certification, a full70-page poetic/lexical study, TL44 source acquisition or broader source rights. Original152-item expert triage remains PREPARED_NOT_REVIEWED; no reviewer, accepted correction or independent assessment is invented. All114 frozen rows and canonical zero remain unchanged.


## 2026-10-16 — TL44 source checkpoint

Two modern TL44 edition identities are confirmed from pinned publisher-deposited metadata. All105 existing TL44 digital row labels have Kalinka page routes, with three selected boundary/inventory observations. Modern article PDFs and full sign/apparatus comparison remain pending; West pagination stays unresolved. All114 frozen rows and canonical zero are unchanged. [Source evidence and next actions](docs/TL44-SOURCE-CHECKPOINT.md).

## 2026-10-16 scoped human-validation preparation

Added exact evidence-bound decision routing and preserved acquisition/maintainer prerequisites. [TL44 boundary review](docs/TL44-BOUNDARY-REVIEW.md) accounts for105 rows and47 documentary marker contexts without accepting readings.

## 2026-10-17 — Research delivery controls

Add checksum-bound native search/evidence responses, deterministic local research
packaging and offline replay, revision-bound review submission forms and rejection
tests. Update individual AI instructions and documentation. No source record,
reading, expert acceptance or redistribution permission is added by this change.
