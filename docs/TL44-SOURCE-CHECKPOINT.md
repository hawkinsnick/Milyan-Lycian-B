# TL44c/d: edition identity and source-label checkpoint

This checkpoint resolves two modern bibliographic identities and routes all105 existing digital row labels to Kalinka1901 pages. It does not complete105 sign collations. Read `research/tl44-source-checkpoint.json`; every proposed route retains the original row ID, literal label and text hash. All114 frozen reference strings remain unchanged; no canonical reading, independent review or new physical object is added.

| Target | Publisher-deposited identity | Date roles | Pagination |
|---|---|---|---|
| TL44c32–65 | Diether Schürr, *Zum Agora-Pfeiler in Xanthos V: das Nordgedicht auf Cheriga (TL44c,32ff.)*, Kadmos55(1–2), DOI10.1515/kadmos-2016-0008 | Print2016-05-24; no online date field in this Crossref response |147–196 in publisher/Crossref metadata; not verified from article PDF |
| TL44d | Diether Schürr, *Zum Agora-Pfeiler in Xanthos VI: das Westgedicht auf Cheriga und Muni (TL44d)*, Kadmos57(1–2), DOI10.1515/kadmos-2018-0006 | Print2018-06-01; online2018-10-08 | Publisher/Crossref55–106; previously seen author-platform extracted header55–105. Unresolved pending actual first/last PDF page inspection. |

The exact titles, spaces, date arrays and metadata response hashes are in the register and committed Crossref snapshots. Platform catalogue/upload years and publisher copyright footers are different date roles; they do not replace the print year. A missing Crossref license field supplies no reuse grant. Bibliographic identity, acquisition, visual consultation, critical collation and republication rights are separate statuses.

The modern article PDFs remain **unacquired**. Author-platform browser access was denied; no alternate-route retry was made. Publisher full text requires access. Obtain authorized publisher/library copies or a lawfully supplied user copy, verify pagination and the revised text/apparatus locators, then begin source-attributed sign comparison. No purchase, author contact, institutional authorization or download permission is presumed.

## Kalinka source inspection

The Getty/Internet Archive Kalinka1901 scan was independently reacquired. SHA-256 `0a25872a235602955772da2d73bc3f8fd6d342bae050ab6abf70216e4368f9da` matches the earlier locator receipt:154 PDF pages,13,372,650 bytes. This pass visually inspected printed41/PDF51 (facsimiles),43/PDF53 and44/PDF54 (transliterations), including an enlarged north-end crop. Provider NOT_IN_COPYRIGHT metadata is inherited from the earlier register; no new legal determination is asserted. Kalinka and its digital descendants are not newly independent witnesses.

| Existing digital segment | Proposed printed-label route | Printed page | PDF ordinal |
|---|---|---|---|
| TL44c,34 digital rows | c32–65 |43 |53 |
| TL44d, first53 digital rows | d1–53 |43 |53 |
| TL44d, remaining18 digital rows | d54–71 |44 |54 |

These are label-sequence/page routes, not proof that each digital row equals one ancient physical line or that every sign agrees. The modern editions remain essential for updated readings, apparatus and interpretation.

Three bounded observations are recorded:

- **c64–65 carryover:** digital c64 ends `serijekabu//rã :` and c65 begins `sebe masa`. Kalinka printed43 has `cabu-` at the end of64 and `rã sebe masa` at65. Preserve the digital strings and expose the allocation separately; do not silently relocate a fragment or globally normalize historical transliteration conventions.
- **d53–54 page transition:** West transcription continues from printed43 to44. Page boundaries do not create extra objects or independent readings.
- **Unplaced fragments:** Kalinka’s separate heading e) records two fragments of uncertain north/west placement. They are not automatically additional admitted c/d rows or missing objects to fill by inference.

Only the first observation compares a small literal boundary fragment; the others are layout/inventory controls. This is not an exhaustive discrepancy inventory, apparatus review or complete sign comparison.

## Query and replay

Run `python scripts/tl44_source_checkpoint.py`; optional `--pdf PATH` verifies the exact scan bytes without pretending to repeat visual inspection. Query `python scripts/evidence_query.py --help` for the `tl44-label-routes`, `tl44-source-issues` and `tl44-modern-editions` collections. Evidence-query outputs retain native record, JSON pointer and source hash. Keep row routes, source observations and bibliographic targets in their separate units; never sum them into objects or witnesses.

Original comparison notes and metadata do not relicense the modern articles. No modern PDF, image, full transcription or full apparatus is committed. Existing eDiAna reference components retain CC-BY-SA-4.0 and attribution; project licensing does not override upstream terms. Historical attribution and reconciliation registers stay historical snapshots; this checkpoint supplies the new consultation state.
