# TL55: exhaustive encoded-sign comparison

The revised transcription on Schürr2005 printed pp.121–122 (PDF27–28) now has an exhaustive position-level comparison with the frozen eDiAna TL55 strings. All1348 reference grapheme/notation units and1233 source print-unit positions are accounted for in1441 candidate alignment records. This closes the missing encoded-sign comparison layer. It does not close independent epigraphic adjudication or certify a definitive edition.

The source is the exact author-posted PDF identified by SHA-256 in the [alignment register](../research/tl55-sign-alignment.json). Printed pages were rendered and visually read. Dedicated font glyphs were decoded only for this exact source: the linguistic font’s m-tilde/e-tilde and the Greek chi fonts are explicitly mapped. Underdots come from the dedicated dotted fonts. Four underlined punctuation positions are recovered from individual PDF drawing segments, including the three segments combined in one drawing object. Unknown source bytes, fonts or custom glyphs stop optional replay.

Each source position has a stable ID, PDF ordinal, printed-page number, source line label, print-row index, bounding box and mark/context fields. Coordinates are PDF points, origin at the upper left; they locate the printed edition, not a photographed or independently inspected ancient sign. The explicit p/l alternative is one comparison unit retaining three rendered-glyph boxes. The33 print-layout units include wrap hyphens and editorial vacat labels; they are accounted for separately from text comparison. These mixed unit totals must never be reported as counts of ancient signs.

Each reference unit retains its exact original literal, row ID and zero-based, end-exclusive Python Unicode code-point offsets. Combining marks stay attached; opaque `&lang;`/`&rang;` entities and other editorial notation stay literal. All four `//` markers are separately accounted for, using the earlier provisional source-allocation spans. That allocation itself remains reviewable. No whitespace is treated as a proven ancient word boundary.

## What the comparison records

| Relation | Records | Interpretation |
|---|---:|---|
| Base and recorded marks agree |746|Printed/digital comparison only; no new accepted reading|
| Declared chi/x convention |16|Transliteration correspondence, not literal equality|
| Unicode representation only |54|Comparison-only NFC correspondence; raw strings unchanged|
| Base agrees, qualification differs |20|Underdots or editorial context require review|
| Different base or notation |26|Candidate substitutions, including ambiguous cross-type pairs|
| Notation marks differ |5|Includes underlined punctuation and marked separator|
| Explicit alternative overlaps |1|Single digital form does not erase p/l|
| Reference position without partner |204|Includes notation/spacing; not204 missing ancient signs|
| Source position without partner |60|Includes notation/spacing; not60 newly recovered signs|
| Notation agreement only |167|Editorial/punctuation comparison, not linguistic agreement|
| Editorial spacing only |105|No lexical-boundary inference|
| Digital break markers |4|Literal source-row markers|
| Print layout only |33|Editorial/printing features|

The complete table sums to1441 records. Separately,36 of those records have more than one possible partner across minimum-cost alignment paths; the ambiguity count overlaps relation categories. No unique total of scholarly disagreements or ancient lost signs follows from this table.

Alignment is performed within each of the nine provisional source-label allocations. Match keys use NFC locally and the declared source chi/digital x convention; letter substitutions cost2, other substitutions4, ordinary gaps2 and spacing gaps1. Forward/backward dynamic programming finds all partner ambiguity on optimal paths. A deterministic traceback supplies one candidate sequence; it does not adjudicate competing epigraphic alignments. Nasal mark variations outside the declared NFC correspondence are retained as differences. Apparently agreeing positions can still contain a systematic encoding or alignment error and must remain within expert review scope.

## Query and replay

`python scripts/research_api.py signs --text TL55-L2-A087` returns a candidate comparison with reference literal/context, source coordinates, method, source PDF hash and rights. The text filter is a literal substring over returned context; row IDs or unit IDs also work. `--format csv` preserves nested objects as JSON fields.

`python scripts/tl55_sign_alignment.py` verifies immutable public inputs, exact reference-unit reconstruction, complete single-use source/reference accounting and the unperformed-expert-review state. This public replay tests integrity, not fresh visual verification of source glyph identities.

With the exact lawfully held PDF, `python scripts/tl55_sign_alignment.py --pdf /absolute/path/source.pdf` also decodes source positions and reruns the alignment for exact equality with the public register. This optional route requires PyMuPDF; ordinary query/CI validation does not. The source hash is checked before decoding. The decoded full source stays in the local audit process; no source transcription or images are printed or imported into GitHub. A private full glyph audit is retained separately and bound by the register's semantic hash. Reproducing the same algorithm is not an independent scholarly assessment.

## Expert handoff and limits

The [sign-adjudication supplement](../review/tl55-sign-adjudication.json) pins the comparison and original review packet, with152 pending triage items. It includes every ambiguous record and non-routine non-spacing comparison. It is neither152 proven errors nor152 attributed alternative reading pairs. Reviewer, rationale, assessment and accepted readings remain empty. Review must include the original source and apparent agreements as well as flagged positions; sign ambiguity is not settled by algorithm cost.

The earlier nine-line/74-entry documentary inventory and six selected issue dossiers remain immutable checkpoints. Their counts do not become independent witnesses. All114 reference rows, all existing EpiDoc strings and the zero verified canonical readings remain unchanged. Full epigraphic certification, independent expert adjudication, TL44 edition acquisition and broader modern-source reuse permission remain open.

The qualified reference units and project annotations use CC-BY-SA-4.0 with existing eDiAna and edition attribution. The source edition, PDF and images retain their rights. Exact-source local replay grants no redistribution licence.

The collection handoff byte-pins the complete register and triage packet but does not reinterpret per-glyph source labels as new bibliographic acquisition leads. Those comparison records remain queryable through their native collections, and the152 pending triage items remain in the linked review packet. This avoids duplicating glyph metadata as null acquisition tasks; it does not remove review obligations or close a scientific gate.


## Documentary follow-up completed

All152 triage records now have58 source-located assessments in the [documentary completion register](../research/tl55-documentary-sign-review.json). All36 algorithmically ambiguous records are explained positionally or retained as range/repeated-run comparisons. Original algorithm flags and the external expert packet remain unchanged. Use `research_api.py sign-review` for the completed documentary layer; [scope and remaining limits](TL55-DOCUMENTARY-COMPLETION.md).
