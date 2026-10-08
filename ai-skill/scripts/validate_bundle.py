#!/usr/bin/env python3
import json
from pathlib import Path
root=Path(__file__).resolve().parents[2]
records=json.loads((root/'data/inscriptions.json').read_text())
index=json.loads((root/'ai-skill/generated/research-bundle-index.json').read_text())
assert len(records)==index['record_count']
assert len({r['id'] for r in records})==len(records)
assert sum(r['status']=='verified' for r in records)==index['verified_record_count']
assert sum(bool(r['diplomatic_transcription']) for r in records)==index['transcribed_record_count']
for r in records:
    assert r['language']=='milyan' and r['sources'] and r['rights']
    for s in r['sources']: assert s['citation'] and s['locator']
print('PASS: record identity, evidence provenance, bundle counts')
