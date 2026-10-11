# Source-attributed Milyan reference layer

The repository now offers a populated digital reference alongside its three provisional bibliographic targets. Two eDiAna catalogue records contain 114 source text rows: TL 55 has nine, TL 44c has 34 (labels 32–65), and TL 44d has 71 (labels 1–71). These are source row counts, not unique physical-object or independent-witness counts. The three empty source heading rows are retained separately. Section correspondence follows eDiAna headings and does not certify monument identity.

## Provenance and attribution

Source: Miller, Jared; Rieken, Elisabeth; Hackstein, Olav; Yakubovich, Ilya (eds.), 2017–, [eDiAna](https://www.ediana.gwi.uni-muenchen.de). [Official citation guidelines](https://www.ediana.gwi.uni-muenchen.de/assets/pdfs/citation.pdf), p.1, require source hyperlinks; p.2 states CC BY-SA 4.0. Interpretations should cite the relevant individually authored lemmata and the primary editions listed in the source headings. The source project's [methodology](https://www.ediana.gwi.uni-muenchen.de/project.php) warns that readings and analyses can change.

Frozen source: `data/reference/ediana-milyan-source.json`, SHA-256 `e53dca3df71f06af95c0091646ee0d1b20fe6c78c1a24ac0f9b9e49cadd425a0`, copied byte-for-byte from `hawkinsnick/Lycian-and-Carian` commit `8ae31f14326b5162271ed699a53343d2c0b657b7`, path `data/raw/ediana/milyan-1-0.json`. Direct live retrieval returned HTTP 403 on 2026-10-11; this release is a frozen-cache replay, not a fresh live-content validation. Source locators point to exact group and row index.

Source text strings, brackets, punctuation and combining marks are unchanged. Raw annotations are preserved in the source JSON; source interpretations are not promoted to established lexical facts. Changes consist of project IDs, provenance wrappers, a source-label crosswalk and JSON/EpiDoc serialization. This source-derived component and its adaptations remain **CC BY-SA 4.0**; project-original noncommercial terms do not override it. No photos or other separately licensed components are imported.

## Use and replay

```bash
python scripts/research_api.py coverage --layer reference
python scripts/research_api.py lines --layer reference
python scripts/research_api.py kwic --layer reference --text mlutene
python scripts/research_api.py lines --layer reference --format csv
python scripts/research_api.py export --layer reference
python scripts/build_reference.py
python -m unittest discover -s tests -p test_reference.py
```

The API defaults to the canonical/provisional layer, whose verified reading count is zero. Choose `--layer reference` to query the attributed digital readings. Literal KWIC uses casefolded source strings, not restoration or linguistic adjudication. Lack of a hit is not evidence of lexical absence. JSON and CSV retain provenance; CSV encodes nested values as JSON.

`interchange/epidoc/milyan-reference.xml` preserves every derived line field in a native-record JSON note and exact source text in an `ab`. Digital source rows are marked as textparts; no graphical or critical apparatus is invented from opaque notation. `scripts/validate_upstream_epidoc.py` requires exact schema/compiler hashes in `interchange/epidoc/upstream-pins.json`. Run with `--schema` and `--compiler` pointing to those pinned upstream dependencies. The dedicated CI job acquires these exact commits and runs RNG plus all 57 embedded Schematron patterns; 348 fired rules, zero findings. Any report or failed assertion rejects this strict profile. Four adversarial integration tests verify execution and reject dependency tampering and contradictory dates.

## Remaining scholarly work

Critical-edition collation, graphical evidence, variant apparatus, alternative readings and source independence remain open. This completes reference population and serialization for the declared frozen source, not the entire world corpus or scholarly acceptance. Three provisional targets, zero verified canonical readings and no independent reviews remain the canonical acceptance state. Collection review packets now declare all two reference records and 114 reference rows in separate views, never summed as physical objects.
