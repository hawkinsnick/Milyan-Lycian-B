# TL55: source comparison and independent-review handoff

The author-posted article has been acquired and pinned by SHA-256. This closes the article-delivery dependency for this source. Printed pages and PDF ordinals are separate: printed p.121 is PDF27. The article runs pp.95–164, 70 PDF pages. The register lists exactly which pages were visually inspected; acquisition of the whole file is not a claim of complete reading collation.

The article distinguishes photographic/facsimile documentation, a revised transcription with apparatus, and a later poetic reconstruction. The revised transcription explicitly labels lines1–9 on pp.121–122; apparatus routes for all nine are on pp.123–129. Its p.99 description also discusses the partly executed ninth line. These are attributed edition observations, not a project autopsy or independently certified physical-line count. The earlier Texier quotation and Kalinka count checkpoint remain intact.

Six selected issues qualify the frozen eDiAna reference: an opening sign the editor excludes, a qualified alternative letter in line2, the alternative forms in line4, a graphic-reading/emendation distinction in that line, and two differences in character allocation at row boundaries. The register retains exact reference fragments and offsets, source page locators, qualifications and editorial layers. No competing form is adopted as a canonical correction. These six dossiers are selected examples; the expanded first-pass inventory below covers every apparatus paragraph.

The edition’s uncertainty conventions and source-specific transliteration changes are recorded without applying global normalization. Raw extracted PDF text is unsafe as a transcription authority because some dedicated glyphs extract incorrectly. The downloaded PDF also includes highlights/comment overlays on reconstruction pages; their unattributed contents are excluded from the evidence. Article authorship follows the printed article, not PDF producer metadata.

## Research use

`python scripts/research_api.py collation` returns nine qualified reference rows. `--text MIL-TL055-S2005-LINE4-PL` selects its relevant row; `--format csv` retains structured source context as JSON fields. The literal eDiAna strings and their uncertainty/entity notation are unchanged. Canonical queries still contain zero verified lines. The 114 reference rows remain a separate source-attributed layer.

`python scripts/tl55_collation.py` replays the register and qualified view. `--write` regenerates the view. Checks reject changes to frozen strings, erasure of alternatives, promotion of qualified readings, conflation of reconstruction with graphic transcription, unsupported rights claims and lost comparison context.

## Rights and remaining scope

The PDF, page images, full modern transcription, full apparatus and reconstructed poem are excluded from the repository. Limited attributed findings and tiny source comparisons support the project’s original analysis. Author-posted access supplies no general redistribution licence. The qualified reference view, including project comparison annotations, is distributed under CC-BY-SA-4.0 consistently with the eDiAna-derived component; this does not license Schürr’s underlying article or images.

Complete sign-by-sign epigraphic collation, additional edition targets, applicable permissions for broader modern-edition reuse and independent epigraphic assessment remain open. There are no new verified readings, accepted interpretations, physical objects or independent reviews.


## Completed first documentary pass

The [current inventory](../research/tl55-first-pass-review.json) records the completed first visual reading/comparison pass for revised transcription pp.121–122 and all apparatus paragraphs pp.123–129. It has74 entries, numbered within source line:7,10,11,10,13,10,5,6,2. Notes are project-original paraphrases of attributed editorial assessments, not replacement readings or a republished apparatus. The source's qualifier remains operative even where an individual note reports its editor's certainty. The record distinguishes first-pass coverage from a full sign-by-sign critical collation or certification of text equality.

All nine literal reference strings are covered by17 nonoverlapping spans, including four two-character `//` markers in digital rows2,4,7,8. Material following each marker is provisionally associated with the next source label while its original digital row stays intact. This adds the2/3 and4/5 boundary cases to the two previously selected7/8 and8/9 cases. Unicode offsets count Python string code points, without normalization; span hashes cover exact UTF-8 bytes. These are source-allocation observations, not lexical segmentation or physical-line certification.

`python scripts/tl55_review.py` verifies exhaustive span accounting, entry identities, immutable review input hashes and the unperformed-expert-review state. The collation query includes line review, source-ordinal apparatus review notes and reference spans. CSV keeps these as JSON fields. No missing selected issue is interpreted as full agreement.

The [independent-review packet](../review/tl55-independent-review.json) fixes input hashes, source access information, expertise requirements and eleven review questions, including the six selected issue IDs. Reviewer, affiliation, date, assessment and review evidence remain null; dispositions and accepted readings remain empty. A qualified independent reviewer must assess every line, sign uncertainty and competing editorial layer, supply attributable per-issue decisions and identify unresolved objections. The packet is ready for review, not already reviewed. No external outreach has been made.
