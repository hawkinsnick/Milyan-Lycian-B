# TL55 documentary sign comparison: completion and limits

The bounded documentary comparison of the frozen digital TL55 text against Schürr2005’s revised transcription and apparatus is complete. All1441 encoded comparison records remain accounted for. Every one of the152 flagged records now has an explicit source-located assessment, grouped into58 documentary cases. No flag is silently dismissed as agreement.

The printed transcription (pp.121–122/PDF27–28) and apparatus (pp.123–129/PDF29–35) were visually consulted for this follow-up. Exact reference-unit IDs, source-position IDs, printed-page/PDF locators and specific apparatus paragraphs where securely identified are retained in `research/tl55-documentary-sign-review.json`. Cases without a specific apparatus entry rely on the printed transcription; an apparatus discussion is not invented for an unmentioned digital intervention. All assignments retain the earlier provisional source-label/carryover allocation.

## What happened to the 36 algorithmic ambiguities

| Documentary disposition | Candidate records | What remains qualified |
|---|---:|---|
| Positional or notation explanation |19|Restored/doubtful letters compare to unknown slots; delimiters remain delimiters. No restored reading is validated.|
| Repeated-run correspondence |2|One digital letter compares with a two-letter printed run; no unique individual partner or extra ancient-sign identity is established.|
| Range-only correspondence |15|Damaged ranges, boundary allocation or competing sign/separator patterns do not establish unique point pairings.|

The counts sum to36 original algorithmic records. Their flags remain immutable in the encoded alignment register. The review provides an interpretive overlay, not a rewritten alignment or claim that36 ancient signs have been resolved. The19 positional explanations also remain documentary proposals, not independently adjudicated epigraphic correspondences.

The range-only cases are `TL55-REVIEW-23`, `-32`, `-52` and `-58`; the repeated-run case is `-55`. They are fully compared as ranges without pretending that available evidence supplies unique individual pairings. The earlier source’s uncertain letters, alternatives and editorial interventions remain attributed. Apparent agreements in the unflagged records still rely on the encoded comparison, not a new independent reading of the monument.

## Research use

- `python scripts/research_api.py sign-review --text TL55-REVIEW-55` retrieves the repeated-run case and its unresolved point-identity boundary.
- `python scripts/research_api.py signs --text TL55-L8-A062` returns the original ambiguous candidate with the documentary assessment attached. Its expert state remains pending.
- Both commands support `--format csv`; nested context stays JSON rather than being flattened into unsupported certainty.
- `python scripts/tl55_documentary_review.py` replays immutable inputs, exact152-record coverage, all36 ambiguity dispositions and the absence of accepted readings or independent review.
- Optional `--pdf /absolute/path/source.pdf` additionally reruns the exact-PDF alignment and checks the preferred unknown-slot, delimiter and repeated-run correspondences. Replaying the same method is not independent scholarly review.

The review notes and qualified reference context use the existing CC-BY-SA-4.0 component terms. The PDF, images, complete modern transcription and apparatus remain outside GitHub and retain source rights.

## Remaining scholarly boundary

This completes the documentary task, including review of all flagged candidate comparisons. It does not certify a definitive critical edition, physical-line correspondence or the identity of damaged ancient signs. Independent expert adjudication and epigraphic certification remain open; the original152-item external-review packet remains `PREPARED_NOT_REVIEWED`, with no reviewer or accepted readings. A complete70-page poetic/lexical interpretation is outside this bounded comparison.

All114 frozen reference rows and existing EpiDoc strings are unchanged. Canonical verified readings and independent reviews remain zero. The TL44c/TL44d primary-edition tasks remain separate acquisition/collation work.
