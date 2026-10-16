"""Verify TL44 bibliographic/label routing without treating it as sign collation."""
import argparse
import hashlib
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
REGISTER = 'research/tl44-source-checkpoint.json'

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def audit(register, reference, metadata):
    expected = {r['id']: r for r in reference if r['source_section'] in ('MIL-TL-044-C', 'MIL-TL-044-D')}
    rows = register['rows']
    if len(rows) != 105 or len({r['reference_row_id'] for r in rows}) != 105 or {r['reference_row_id'] for r in rows} != set(expected):
        raise ValueError('TL44 row inventory omitted, duplicated or invented')
    for row in rows:
        original = expected[row['reference_row_id']]
        face = original['source_section'][-1].lower()
        label = int(original['line_label'].replace('·', '').strip())
        page = 43 if face == 'c' or label <= 53 else 44
        wanted = {'source_section': original['source_section'], 'literal_reference_line_label': original['line_label'],
                  'reference_text_sha256': sha(original['text'].encode()), 'proposed_kalinka_label': f'{face}{label}',
                  'kalinka_printed_page': page, 'kalinka_pdf_ordinal': page + 10,
                  'facsimile_printed_page': 41, 'facsimile_pdf_ordinal': 51,
                  'full_row_sign_collation_complete': False, 'physical_line_identity_verified': False, 'accepted_reading': False}
        if any(row[k] != v for k, v in wanted.items()):
            raise ValueError('literal input, page/label route or unperformed collation drift')
    if len(register['editions']) != 2:
        raise ValueError('modern edition identity count')
    for edition, year in zip(register['editions'], (2016, 2018)):
        m = metadata[year]['message']
        for key, value in [('doi', m['DOI']), ('title', m['title'][0]), ('volume', m['volume']), ('issue', m['issue']),
                           ('crossref_page_range', m['page']), ('published_print', m['published-print']['date-parts'][0]),
                           ('published_online', m.get('published-online', {}).get('date-parts', [None])[0])]:
            if edition[key] != value:
                raise ValueError('publisher metadata role drift: ' + key)
        if any(edition[k] is not False for k in ['article_pdf_acquired', 'article_pdf_visually_inspected', 'critical_apparatus_collated', 'reuse_permission_established']):
            raise ValueError('metadata promoted to acquisition, collation or reuse permission')
        if edition['page_range_confirmed_from_article_pdf'] is not None:
            raise ValueError('uninspected article pagination certified')
    conflict = register['editions'][1]['pagination_conflict']
    if conflict['publisher_and_crossref'] != '55–106' or conflict['previously_seen_author_platform_extracted_header'] != '55–105' or conflict['status'] != 'UNRESOLVED_UNTIL_ARTICLE_PDF_FIRST_AND_LAST_PAGE_INSPECTION':
        raise ValueError('pagination conflict erased')
    limits = register['limits']
    for key in ['verified_canonical_readings_added', 'independent_reviews_added', 'new_physical_objects_added', 'modern_article_pdfs_acquired', 'full_sign_collations_of_tl44_rows_completed']:
        if limits[key] != 0:
            raise ValueError('unperformed scholarly work claimed')
    if limits['frozen_reference_rows_changed'] or limits['source_independence_established']:
        raise ValueError('frozen reference or independence boundary drift')
    if {i['id'] for i in register['issues']} != {'TL44C-BOUNDARY-64-65', 'TL44D-PAGE-53-54', 'TL44-UNPLACED-FRAGMENTS'}:
        raise ValueError('selected observation inventory drift')
    for issue in register['issues']:
        if issue['canonical_change_applied'] or not set(issue['reference_row_ids']) <= set(expected):
            raise ValueError('observation promoted or linked outside scope')
    return {'tl44c_label_routes': 34, 'tl44d_label_routes': 71, 'modern_edition_identities': 2,
            'selected_boundary_observations': 3, 'full_row_sign_collations': 0, 'accepted_readings': 0}

def validate(root=ROOT, pdf=None):
    root = Path(root)
    register = json.loads((root / REGISTER).read_text())
    for pin in register['input_pins']:
        if sha((root / pin['path']).read_bytes()) != pin['sha256']:
            raise ValueError('frozen input hash mismatch: ' + pin['path'])
    if register['input_pins'][0]['sha256'] != 'c9e91db653d9fed2e0ac9d0428127623ad7175f4bbef7e08bc2f8a85cc399ead':
        raise ValueError('frozen reference baseline replaced')
    metadata = {}
    for edition, year in zip(register['editions'], (2016, 2018)):
        raw = (root / edition['metadata_snapshot']).read_bytes()
        if sha(raw) != edition['metadata_sha256']:
            raise ValueError('metadata hash mismatch')
        metadata[year] = json.loads(raw)
    if pdf:
        raw = Path(pdf).read_bytes()
        if len(raw) != register['kalinka_source']['bytes'] or sha(raw) != register['kalinka_source']['sha256']:
            raise ValueError('wrong Kalinka source PDF')
    return audit(register, json.loads((root / 'data/reference/lines.json').read_text()), metadata)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pdf', help='Optionally verify the exact lawfully held Kalinka scan; does not automate visual review')
    args = parser.parse_args()
    print(json.dumps(validate(pdf=args.pdf), indent=2))
