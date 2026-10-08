#!/usr/bin/env python3
"""Standard-library, no-dependency corpus integrity checks."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
records=json.loads((root/'data/inscriptions.json').read_text(encoding='utf-8'))
assert isinstance(records,list)
ids=set()
for record in records:
    assert isinstance(record,dict)
    for field in ('id','language','status','sources','rights'):
        assert field in record, (record.get('id'),field)
    assert record['id'] not in ids, 'duplicate ID'
    ids.add(record['id'])
    assert record['language']=='milyan'
    assert record['status'] in ('provisional','verified')
    assert record['sources'] and isinstance(record['sources'],list)
    for source in record['sources']:
        assert source.get('citation') and source.get('locator')
    if record['status']=='verified':
        assert record.get('diplomatic_transcription'), 'verified record without text'
index=json.loads((root/'ai-skill/generated/research-bundle-index.json').read_text(encoding='utf-8'))
assert len(records)==index['record_count']
assert sum(r['status']=='verified' for r in records)==index['verified_record_count']
assert sum(bool(r.get('diplomatic_transcription')) for r in records)==index['transcribed_record_count']
print(f'PASS: {len(records)} records, {index["verified_record_count"]} verified')
