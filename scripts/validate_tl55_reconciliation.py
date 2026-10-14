"""Replay attributed source metadata; reject silent promotion to scholarly acceptance."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REGISTER='research/tl55-count-reconciliation-2026-10-14.json'
PIN='903b6deb722c65c4d31e22b058d3c86ea787b2844053b6cd3c5a7c850798484f'
def digest(x):return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def validate(root=ROOT):
 x=json.loads((root/REGISTER).read_text())
 if digest(x)!=PIN:raise ValueError('inspected source identity, categories or acceptance boundary changed')
 if hashlib.sha256((root/x['reference']['path']).read_bytes()).hexdigest()!=x['reference']['sha256']:raise ValueError('frozen reference rows changed')
 rows=json.loads((root/x['reference']['path']).read_text())
 if len(rows)!=114 or len([r for r in rows if r['source_section']=='MIL-TL-055'])!=9:raise ValueError('source row denominator drift')
 return {'status':'PASS_TL55_COUNT_VOICE_ACCOUNTING','quoted_historical_count':8,'edition_entry_groups':9,'digital_rows':9,'exact_reading_equivalence':False,'physical_line_count_certified':False}
if __name__=='__main__':print(json.dumps(validate()))
