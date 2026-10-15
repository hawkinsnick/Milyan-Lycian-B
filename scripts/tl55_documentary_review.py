"""Replay complete documentary review of TL55 candidates without granting epigraphic acceptance."""
import argparse,collections,hashlib,json,unicodedata
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REGISTER='research/tl55-documentary-sign-review.json'
PIN='1542ed9b7acfc457824024a22231d54501b2ae2700dde8d127c5839792833b20'
def digest(x):return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def audit_cases(review,alignment,packet):
 links={a['id']:a for a in alignment['alignments']};refs={u['id']:u for u in alignment['reference_units']};src={u['id']:u for u in alignment['source_positions']};cases=review['cases']
 if len(cases)!=58 or len({c['id'] for c in cases})!=58:raise ValueError('review case identity drift')
 expected=collections.Counter(i['alignment_id'] for i in packet['items']);seen=collections.Counter(i for c in cases for i in c['alignment_ids'])
 if expected!=seen or any(n!=1 for n in seen.values()):raise ValueError('flagged candidate omitted, duplicated or invented')
 ambiguous={a['id'] for a in alignment['alignments'] if a['alignment_ambiguous']};ambseen=[i for c in cases for i in c['algorithm_ambiguous_records']]
 if set(ambseen)!=ambiguous or len(ambseen)!=len(ambiguous):raise ValueError('ambiguity coverage lost')
 for c in cases:
  if not c['documentary_assessment'].strip() or c['status']!='DOCUMENTARY_REVIEW_COMPLETE_NOT_EPIGRAPHIC_ACCEPTANCE':raise ValueError('missing substantive documentary disposition')
  if c['unique_point_mapping_claimed'] or c['canonical_change_applied'] or c['independent_review_added']:raise ValueError('documentary result promoted to scientific acceptance')
  if any(links[i]['source_label']!=c['source_label'] for i in c['context_alignment_ids']):raise ValueError('wrong source-label context')
  if not set(c['alignment_ids'])<=set(c['context_alignment_ids']) or not set(c['context_alignment_ids'])<=set(c['anchor_alignment_ids']):raise ValueError('missing comparison context')
  for p in c['preferred_documentary_correspondences']:
   if p['accepts_reading']:raise ValueError('restoration accepted by correspondence')
   if p['reference_unit'] and refs[p['reference_unit']]['source_label']!=c['source_label']:raise ValueError('wrong reference position')
   if p['source_unit'] and src[p['source_unit']]['source_label']!=c['source_label']:raise ValueError('wrong printed position')
  if c['ambiguity_disposition']=='REPEATED_RUN_NO_UNIQUE_POINT_MAPPING':
   run=c['repeated_run']
   if run['identity_of_extra_ancient_sign_established'] or len(run['reference_units'])!=1 or len(run['source_units'])!=2:raise ValueError('repeated-run ambiguity falsely resolved')
 if review['scope']['full_epigraphic_certification_granted'] or review['scope']['independent_reviews_added'] or review['scope']['accepted_readings_added']:raise ValueError('unperformed expert adjudication claimed')
 counts=collections.Counter()
 for c in cases:counts[c['ambiguity_disposition']]+=len(c['algorithm_ambiguous_records'])
 if [counts[k] for k in ['POSITIONAL_CORRESPONDENCE_DOCUMENTED','REPEATED_RUN_NO_UNIQUE_POINT_MAPPING','RANGE_ONLY_NO_UNIQUE_POINT_MAPPING']]!=[19,2,15]:raise ValueError('documentary ambiguity accounting drift')
def audit_source_pairs(review,refs,source):
 for c in review['cases']:
  for p in c['preferred_documentary_correspondences']:
   r=refs.get(p['reference_unit']);s=source.get(p['source_unit']);rel=p['relation']
   if rel in ['RESTORED_TO_UNKNOWN_POSITION','DOUBTFUL_READING_TO_UNKNOWN_POSITION','REFERENCE_LETTER_TO_UNKNOWN_POSITION']:
    if r['kind']!='LETTER' or s['text']!='.':raise ValueError('preferred lacuna correspondence has wrong source glyph')
   elif rel=='REFERENCE_UNKNOWN_TO_DOUBTFUL_PRINTED_LETTER':
    if r['literal']!='.' or not s['text'].isalpha() or 'underdot' not in s['marks']:raise ValueError('unknown/doubtful correspondence drift')
   elif rel=='DIFFERING_LETTER_AT_ANCHORED_POSITION':
    if r['kind']!='LETTER' or not s['text'].isalpha() or 'underdot' not in s['marks']:raise ValueError('anchored differing letter drift')
   elif rel=='REFERENCE_LETTER_WITHOUT_PRINTED_LETTER_PARTNER':
    if r['kind']!='LETTER' or s is not None:raise ValueError('letter incorrectly paired with delimiter')
   elif rel=='PRINTED_PUNCTUATION_WITHOUT_REFERENCE_PARTNER':
    if r is not None or s['text']!=':':raise ValueError('delimiter incorrectly paired with letter')
   else:raise ValueError('unreviewed correspondence relation')
  if 'repeated_run' in c:
   run=c['repeated_run'];rv=refs[run['reference_units'][0]]['literal'];values=[source[s]['text'] for s in run['source_units']]
   if len(values)!=2 or any(unicodedata.normalize('NFC',v)!=unicodedata.normalize('NFC',rv) for v in values):raise ValueError('repeated-run source values differ')
def validate(root=ROOT,pdf=None):
 root=Path(root);review=json.loads((root/REGISTER).read_text())
 if digest(review)!=PIN:raise ValueError('review note, source locator, uncertainty or gate state changed')
 for path,h in review['inputs'].items():
  if hashlib.sha256((root/path).read_bytes()).hexdigest()!=h:raise ValueError('documentary review input drift')
 from tl55_sign_alignment import validate as validate_alignment
 validate_alignment(root,pdf=pdf)
 alignment=json.loads((root/'research/tl55-sign-alignment.json').read_text());packet=json.loads((root/'review/tl55-sign-adjudication.json').read_text());audit_cases(review,alignment,packet)
 first=json.loads((root/'research/tl55-first-pass-review.json').read_text());apparatus={e['id']:e for e in first['apparatus_entries']};links={a['id']:a for a in alignment['alignments']}
 for case in review['cases']:
  for key,field in [('reference_position_ids','reference_unit'),('source_position_ids','source_unit')]:
   expected=list(dict.fromkeys(links[i][field] for i in case['context_alignment_ids'] if links[i][field]))
   if expected!=case[key]:raise ValueError('documentary source context omitted or changed')
  if any(apparatus[i]['source_line']!=case['source_label'] for i in case['specific_apparatus_entry_ids']):raise ValueError('wrong apparatus context')
  if sorted({p for i in case['specific_apparatus_entry_ids'] for p in apparatus[i]['printed_pages']})!=case['specific_apparatus_printed_pages']:raise ValueError('apparatus page drift')
 if pdf:
  from tl55_source_glyphs import extract
  audit_source_pairs(review,{r['id']:r for r in alignment['reference_units']},{s['id']:s for s in extract(pdf)['glyph_units']})
 return {'status':'PASS_TL55_DOCUMENTARY_SIGN_COMPARISON_COMPLETE','source_pdf_replayed':bool(pdf),**review['summary'],'expert_adjudication':'OPEN','full_epigraphic_certification':False}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--pdf',type=Path);a=p.parse_args();print(json.dumps(validate(pdf=a.pdf)))
