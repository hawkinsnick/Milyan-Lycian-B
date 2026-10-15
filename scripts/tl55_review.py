"""Replay first-pass coverage and guard the unperformed independent review."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REVIEW='research/tl55-first-pass-review.json'
PACKET='review/tl55-independent-review.json'
PINS={'research/tl55-first-pass-review.json': '569ce81ab36a50a09f108c758255bec00bcd460a64cdf548a0cf0b0f1b7ac0e0', 'review/tl55-independent-review.json': 'ce9ef32ba783f9dfa6fdc71ad06b972dabd0b51258643a466e72c5ba71ec3bc5'}
def sha(data):return hashlib.sha256(data).hexdigest()
def audit_spans(rows,spans):
 index={r['id']:r for r in rows}
 if set(s['row_id'] for s in spans)!=set(index):raise ValueError('row coverage gap')
 for rid,r in index.items():
  cursor=0
  for s in [s for s in spans if s['row_id']==rid]:
   if s['start']!=cursor or not cursor<s['end']<=len(r['text']):raise ValueError('span omission, overlap or invalid extent')
   fragment=r['text'][cursor:s['end']]
   if sha(fragment.encode())!=s['literal_sha256']:raise ValueError('literal span changed')
   n=int(rid.rsplit('-',1)[1]);k=r['text'].find('//')
   if s['kind']=='LITERAL_DIGITAL_BREAK_MARKER':
    if fragment!='//' or s['source_label'] is not None:raise ValueError('marker relabeled')
   elif s['kind']=='REFERENCE_CARRYOVER_TEXT':
    if k<0 or cursor!=k+2 or s['source_label']!=n+1:raise ValueError('carryover alignment drift')
   elif s['kind']!='REFERENCE_TEXT' or s['source_label']!=n:raise ValueError('source-label allocation drift')
   cursor=s['end']
  if cursor!=len(r['text']):raise ValueError('unreviewed tail')
 if sum(s['kind']=='LITERAL_DIGITAL_BREAK_MARKER' for s in spans)!=4:raise ValueError('not all four markers accounted for')
def validate(root=ROOT):
 for p,pin in PINS.items():
  if sha((root/p).read_bytes())!=pin:raise ValueError('first-pass or external-review state changed without source review')
 review=json.loads((root/REVIEW).read_text());packet=json.loads((root/PACKET).read_text())
 for p,pin in packet['inputs'].items():
  if sha((root/p).read_bytes())!=pin:raise ValueError('review packet input drift')
 rows=[r for r in json.loads((root/'data/reference/lines.json').read_text()) if r['source_section']=='MIL-TL-055']
 audit_spans(rows,review['reference_span_accounting'])
 counts=[7,10,11,10,13,10,5,6,2]
 entries=review['apparatus_entries']
 if len(entries)!=74 or len({e['id'] for e in entries})!=74:raise ValueError('apparatus coverage drift')
 for n,count in enumerate(counts,1):
  group=[e for e in entries if e['source_line']==n]
  if [e['entry_ordinal_within_line'] for e in group]!=list(range(1,count+1)):raise ValueError('entry omission or duplicate')
  if any(e['disposition']!='REVIEWED_NOT_ADJUDICATED' or e['new_reading_admitted'] for e in group):raise ValueError('review promoted to adjudication')
 if packet['status']!='PREPARED_NOT_REVIEWED' or packet['reviewer'] is not None or packet['assessment'] is not None or packet['accepted_readings'] or packet['automatically_closes_expert_gate']:raise ValueError('unperformed expert review claimed')
 if review['scope']['full_critical_collation_complete'] or review['scope']['complete_character_level_equivalence_certified']:raise ValueError('coverage promoted to full critical equivalence')
 return {'status':'PASS_TL55_FIRST_PASS_COVERAGE','source_lines_reviewed':9,'apparatus_entries_reviewed':74,'digital_break_markers_accounted_for':4,'independent_reviews':0,'expert_gate':'OPEN','full_critical_collation_complete':False}
if __name__=='__main__':print(json.dumps(validate()))
