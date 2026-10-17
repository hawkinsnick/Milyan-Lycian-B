"""Replay exact TL44 marker/span accounting and its bounded human request."""
import argparse,hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PACKET='research/tl44-boundary-documentary-review.json'
LIMITS={'reference_rows_changed':False,'canonical_readings_added':0,'physical_objects_added':0,'independent_reviews_added':0,'modern_articles_acquired':0,'full_row_sign_collations_completed':0}
def sha(b):return hashlib.sha256(b).hexdigest()
def audit(d,reference,request):
    expected={x['id']:x for x in reference if x['source_section'] in {'MIL-TL-044-C','MIL-TL-044-D'}}
    if len(expected)!=105 or len(d['rows'])!=105 or {x['reference_row_id'] for x in d['rows']}!=expected.keys():raise ValueError('missing duplicate or invented TL44 row')
    if d['limits']!=LIMITS or any(type(d['limits'][k]) is not type(v) for k,v in LIMITS.items()):raise ValueError('unsupported research promotion')
    wanted={};spans=0
    for row in d['rows']:
        original=expected[row['reference_row_id']];s=original['text'];face=original['source_section'][-1];label=int(original['line_label'].replace('·','').strip());cursor=0;markers=[]
        if row['text_sha256']!=sha(s.encode()) or row['codepoints']!=len(s) or row['literal_line_label']!=original['line_label'] or row['full_row_sign_collation_complete'] is not False:raise ValueError('literal row or scope drift')
        for span in row['spans']:
            a,b=span['start'],span['end']
            if type(a) is not int or type(b) is not int or a!=cursor or not a<b<=len(s) or sha(s[a:b].encode())!=span['sha256']:raise ValueError('nonexact span coverage')
            if span['role']=='literal_boundary_marker':
                if s[a:b]!='//':raise ValueError('invented or normalized marker')
                markers.append(a)
            elif span['role']!='reference_fragment':raise ValueError('unknown span unit')
            cursor=b;spans+=1
        positions=[m.start() for m in re.finditer('//',s)]
        if cursor!=len(s) or markers!=positions or row['boundary_marker_count']!=len(positions):raise ValueError('marker lost from complete partition')
        for ordinal,start in enumerate(positions,1):wanted[f'TL44-{face}{label}-MARKER-{ordinal}']=(original,start,face,label)
    if len(wanted)!=47 or len(d['markers'])!=47 or {x['id'] for x in d['markers']}!=wanted.keys():raise ValueError('missing duplicate or invented marker context')
    renders={x['id']:x for x in d['source']['renders']}
    for m in d['markers']:
        original,start,face,label=wanted[m['id']];text=original['text'];before=label-1 if (face,label)==('C',40) else label
        if (m['marker_start'],m['marker_end'],m['literal_prefix'],m['literal_suffix'],m['reference_row_id'])!=(start,start+2,text[:start],text[start+2:],original['id']):raise ValueError('marker payload or target drift')
        if m['proposed_printed_context']!=[face.lower()+str(before),face.lower()+str(before+1)]:raise ValueError('source label boundary drift')
        pages=[43] if face=='C' or label<53 else ([43,44] if label==53 else [44])
        if m['printed_pages']!=pages or m['pdf_ordinals']!=[p+10 for p in pages]:raise ValueError('page context drift')
        if not m['consultation_crops'] or not set(m['consultation_crops'])<=renders.keys() or not m['observation']:raise ValueError('source consultation absent')
        if m['source_layout_context_visually_compared'] is not True or any(m[k] is not False for k in ['exact_transcription_equivalence_established','physical_line_identity_verified','canonical_reading_admitted','independent_review']):raise ValueError('layout comparison promoted to epigraphic acceptance')
    if request['status']!='PREPARED_NOT_REVIEWED' or set(request['required_target_ids'])!=wanted.keys() or len(request['required_target_ids'])!=47:raise ValueError('human scope drift')
    if request['decisions'] or request['automatic_admission'] is not False or request['scientific_approval_granted'] is not False:raise ValueError('unperformed human acceptance claimed')
    for k in ['reviewer','affiliation','review_date','conflicts_and_source_dependence','signed_or_attributed_review_evidence']:
        if request[k] is not None:raise ValueError('prepared request falsely populated as review')
    return {'status':'PASS_TL44_BOUNDARY_DOCUMENTARY_ACCOUNTING','reference_rows':105,'literal_boundary_markers':47,'exact_codepoint_spans':spans,'full_row_sign_collations':0,'independent_reviews':0}
def validate(root=ROOT,pdf=None):
    root=Path(root);raw=(root/PACKET).read_bytes();d=json.loads(raw);request=json.loads((root/'review/tl44-boundary-human-request.json').read_text())
    for pin in d['inputs']:
        if sha((root/pin['path']).read_bytes())!=pin['sha256']:raise ValueError('stale native authority')
    if request['inputs']!=[{'path':PACKET,'sha256':sha(raw)}]:raise ValueError('human request input drift')
    if pdf:
        b=Path(pdf).read_bytes()
        if sha(b)!=d['source']['sha256'] or len(b)!=d['source']['bytes']:raise ValueError('wrong source PDF')
    return audit(d,json.loads((root/'data/reference/lines.json').read_text()),request)
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--pdf',type=Path);a=p.parse_args();print(json.dumps(validate(pdf=a.pdf)))
