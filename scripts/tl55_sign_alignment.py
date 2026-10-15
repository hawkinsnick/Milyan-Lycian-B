"""Exhaustive, qualified TL55 glyph alignment; never a canonical edition or expert review."""
import argparse,collections,hashlib,json,re,unicodedata
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REGISTER='research/tl55-sign-alignment.json'
PIN='2a19ff9daec4b77b24230a1089983d157dbe32b0624d24573b2350955dc44ef8'
def digest(x):return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def strip_marks(text):
 marks=[];base=''
 for c in unicodedata.normalize('NFD',text):
  if c=='\u0323':marks.append('underdot')
  elif c=='\u0332':marks.append('underline')
  else:base+=c
 return unicodedata.normalize('NFC',base),marks
def kind(text):
 if text.isspace():return 'SPACING'
 if text.isalpha() or any(unicodedata.category(c).startswith('L') for c in text):return 'LETTER'
 if text in [':',')']:return 'PUNCTUATION'
 return 'EDITORIAL_NOTATION'
def reference_units(rows,spans):
 units=[]
 for row in rows:
  text=row['text'];pos=0;depth={'square':0,'curly':0,'angle_entity':0}
  while pos<len(text):
   start=pos;match=re.match(r'&(?:lang|rang);|//',text[pos:])
   if match:raw=match[0];pos+=len(raw)
   else:
    pos+=1
    while pos<len(text) and unicodedata.combining(text[pos]):pos+=1
    raw=text[start:pos]
   owning=[s for s in spans if s['row_id']==row['id'] and s['start']<=start and pos<=s['end']]
   if len(owning)!=1:raise ValueError('grapheme crosses accounting boundary')
   base,marks=strip_marks(raw)
   if raw=='[':depth['square']+=1
   if raw=='{':depth['curly']+=1
   if raw=='&lang;':depth['angle_entity']+=1
   u={'id':f"{row['id']}-U{len([x for x in units if x['row_id']==row['id']])+1:03}",'row_id':row['id'],'start':start,'end':pos,'literal':raw,'source_label':owning[0]['source_label'],'kind':'DIGITAL_BREAK_MARKER' if raw=='//' else ('OPAQUE_ENTITY_NOTATION' if raw.startswith('&') else kind(base)),'marks':marks,'editorial_context':{k:bool(v) for k,v in depth.items()},'base':base}
   units.append(u)
   if raw==']':depth['square']-=1
   if raw=='}':depth['curly']-=1
   if raw=='&rang;':depth['angle_entity']-=1
  if any(depth.values()):raise ValueError('unbalanced opaque reference notation')
 return units
def annotate_source(source):
 units=source['glyph_units'];depth=0
 for u in units:
  text=u['text']
  if text=='[':depth+=1
  u['square_bracket_context']=bool(depth)
  if text==']':depth-=1
  u['kind']='ALTERNATIVE' if 'alternatives' in u else kind(text)
  u['base']=unicodedata.normalize('NFC',text)
  if u['role'] in ['PRINT_WRAP_HYPHEN','EDITORIAL_VACAT']:u['kind']='PRINT_LAYOUT'
 if depth:raise ValueError('source bracket imbalance')
 return units
def comparison_key(u,source=False):
 b=u['base']
 # A comparison-only, explicitly declared glyph convention. Original strings are untouched.
 return 'x' if source and b=='χ' else b
def cost(r,s):
 if s['kind']=='ALTERNATIVE' and comparison_key(r) in s['alternatives']:return 0
 if comparison_key(r)==comparison_key(s,True):return 0
 if r['kind']==s['kind']=='SPACING':return 0
 if r['kind']==s['kind']=='LETTER':return 2
 return 4
def gap(u):return 1 if u['kind']=='SPACING' else 2
def align(ref,source):
 n,m=len(ref),len(source);f=[[0]*(m+1) for _ in range(n+1)]
 for i in range(1,n+1):f[i][0]=f[i-1][0]+gap(ref[i-1])
 for j in range(1,m+1):f[0][j]=f[0][j-1]+gap(source[j-1])
 for i in range(1,n+1):
  for j in range(1,m+1):f[i][j]=min(f[i-1][j-1]+cost(ref[i-1],source[j-1]),f[i-1][j]+gap(ref[i-1]),f[i][j-1]+gap(source[j-1]))
 b=[[0]*(m+1) for _ in range(n+1)]
 for i in range(n-1,-1,-1):b[i][m]=b[i+1][m]+gap(ref[i])
 for j in range(m-1,-1,-1):b[n][j]=b[n][j+1]+gap(source[j])
 for i in range(n-1,-1,-1):
  for j in range(m-1,-1,-1):b[i][j]=min(b[i+1][j+1]+cost(ref[i],source[j]),b[i+1][j]+gap(ref[i]),b[i][j+1]+gap(source[j]))
 optimum=f[n][m];rc=[set() for _ in ref];sc=[set() for _ in source]
 for i in range(n+1):
  for j in range(m+1):
   if i<n and j<m and f[i][j]+cost(ref[i],source[j])+b[i+1][j+1]==optimum:rc[i].add(j);sc[j].add(i)
   if i<n and f[i][j]+gap(ref[i])+b[i+1][j]==optimum:rc[i].add(None)
   if j<m and f[i][j]+gap(source[j])+b[i][j+1]==optimum:sc[j].add(None)
 result=[];i,j=n,m
 while i or j:
  if i and j and f[i][j]==f[i-1][j-1]+cost(ref[i-1],source[j-1]):
   i-=1;j-=1;result.append((ref[i],source[j],len(rc[i])>1 or len(sc[j])>1))
  elif i and f[i][j]==f[i-1][j]+gap(ref[i-1]):i-=1;result.append((ref[i],None,len(rc[i])>1))
  else:j-=1;result.append((None,source[j],len(sc[j])>1))
 return list(reversed(result)),optimum

def relation(r,s):
 if r is None:return 'SOURCE_POSITION_WITHOUT_REFERENCE_PARTNER'
 if s is None:return 'REFERENCE_POSITION_WITHOUT_SOURCE_PARTNER'
 if s['kind']=='ALTERNATIVE':return 'ALTERNATIVE_OVERLAP' if comparison_key(r) in s['alternatives'] else 'ALTERNATIVE_DIFFERENCE'
 if r['kind']==s['kind']=='SPACING':return 'EDITORIAL_SPACING_ONLY'
 if comparison_key(r)!=comparison_key(s,True):return 'DIFFERENT_BASE_OR_NOTATION'
 if r['kind']=='LETTER' and s['kind']=='LETTER':
  if r['marks']!=s['marks'] or r['editorial_context']!={'square':s['square_bracket_context'],'curly':False,'angle_entity':False}:return 'BASE_AGREEMENT_QUALIFICATION_DIFFERS'
  if r['base']!=s['base']:return 'DECLARED_TRANSLITERATION_CONVENTION'
  if r['literal']!=s['text']:return 'UNICODE_REPRESENTATION_ONLY'
  return 'BASE_AND_RECORDED_MARKS_AGREE'
 if r['marks']!=s['marks']:return 'NOTATION_MARKS_DIFFER'
 return 'NOTATION_AGREEMENT_ONLY'

def build_from_source(root,source):
 source_digest=digest(source)
 rows=[r for r in json.loads((root/'data/reference/lines.json').read_text()) if r['source_section']=='MIL-TL-055']
 review=json.loads((root/'research/tl55-first-pass-review.json').read_text())
 refs=reference_units(rows,review['reference_span_accounting']);src=annotate_source(source)
 public_source=[]
 for s in src:
  p={k:s[k] for k in ['id','source_label','pdf_ordinal','printed_page','physical_print_row','bbox','role','kind','marks','square_bracket_context']}
  if 'rendered_glyphs' in s:p['alternative_rendered_glyph_boxes']=[g['bbox'] for g in s['rendered_glyphs']]
  public_source.append(p)
 links=[];lines=[]
 for label in range(1,10):
  rr=[r for r in refs if r['source_label']==label];ss=[s for s in src if s['source_label']==label and s['kind']!='PRINT_LAYOUT']
  aligned,c=align(rr,ss);start=len(links)
  for r,s,amb in aligned:links.append({'id':f'TL55-L{label}-A{len(links)-start+1:03}','source_label':label,'reference_unit':r['id'] if r else None,'source_unit':s['id'] if s else None,'relation':relation(r,s),'alignment_ambiguous':amb,'status':'UNRESOLVED_ALIGNMENT' if amb else 'COMPARISON_RECORDED_NOT_ADJUDICATED','canonical_change':False})
  counts=dict(collections.Counter(x['relation'] for x in links[start:]));lines.append({'source_label':label,'alignment_cost':c,'aligned_reference_units':len(rr),'aligned_source_units':len(ss),'relation_counts':counts,'ambiguous_alignment_records':sum(x['alignment_ambiguous'] for x in links[start:]),'expert_adjudication':'PENDING'})
 for r in refs:
  if r['kind']=='DIGITAL_BREAK_MARKER':links.append({'id':'TL55-BREAK-'+r['id'],'source_label':None,'reference_unit':r['id'],'source_unit':None,'relation':'LITERAL_DIGITAL_BREAK_MARKER','alignment_ambiguous':False,'status':'ACCOUNTED_NOT_AN_ANCIENT_SIGN','canonical_change':False})
 for s in src:
  if s['kind']=='PRINT_LAYOUT':links.append({'id':'TL55-PRINT-'+s['id'],'source_label':s['source_label'],'reference_unit':None,'source_unit':s['id'],'relation':'PRINT_LAYOUT_ONLY','alignment_ambiguous':False,'status':'ACCOUNTED_NOT_AN_ANCIENT_SIGN','canonical_change':False})
 return {'format':'tl55-sign-alignment-v1','checked':'2026-10-15','date_basis':'America/Chicago','source_pdf_sha256':source['pdf_sha256'],'private_source_semantic_sha256':source_digest,'source_scope':'Schuerr2005 revised transcription printed121–122/PDF27–28; source PDF, images and full transcription are not bundled.','method':{'font_decode':'Exact-PDF font-specific mapping, visually checked against rendered transcription pages; custom m-tilde/e-tilde and chi glyphs decoded by named fonts only. Underdots retained from dedicated fonts, underlines from individual PDF drawing segments.','reference_offsets':'Python Unicode code points, zero based, end exclusive; grapheme units keep complete original combining sequences and opaque entity markers. No stored reference normalization.','comparison_only':'NFC per-unit comparison; source chi versus digital x is a declared transliteration convention. Neither is exact literal equality. Nasal-mark differences are not silently conflated.','algorithm':'Minimum-cost whole-source-label alignment. Identical comparison keys0, letter substitution2, other substitution4, ordinary gap2, spacing gap1. All optimal-path partner ambiguity is flagged; deterministic traceback is only a candidate alignment.','meaning':'Base/notation comparisons do not establish lexical meaning, physical signs, historical witness independence, accepted corrections or a definitive edition. All mismatch/qualification/ambiguity records remain unadjudicated.','public_replay':'Public validation checks exact inputs, byte coverage and pinned alignment context; optional --pdf performs source-byte/glyph/algorithm replay with a lawfully held exact PDF.'},'inputs':{p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in ['data/reference/lines.json','data/reference/ediana-milyan-source.json','research/tl55-first-pass-review.json','research/schuerr2005-tl55-collation.json']},'reference_units':[{k:v for k,v in r.items() if k!='base'} for r in refs],'source_positions':public_source,'alignments':links,'lines':lines,'summary':{'reference_grapheme_or_notation_units':len(refs),'source_rendered_glyph_or_notation_units':len(src),'alignment_records':len(links),'source_labels':9,'literal_digital_break_markers':4,'print_layout_units':sum(s['kind']=='PRINT_LAYOUT' for s in src),'relation_counts':dict(collections.Counter(x['relation'] for x in links)),'ambiguous_alignment_records':sum(x['alignment_ambiguous'] for x in links),'canonical_readings_added':0,'independent_reviews_added':0},'sign_comparison_coverage_complete':True,'definitive_sign_alignment_established':False,'full_epigraphic_collation_certified':False,'independent_review_status':'PENDING','independent_review_packet':'review/tl55-sign-adjudication.json','rights':{'license':'CC-BY-SA-4.0','scope':'Frozen eDiAna-derived literal units and original project comparison annotations. Source edition, PDF and images retain source rights; access is not bulk redistribution permission.','full_modern_transcription_included':False}}

def adjudication_packet(root,data):
 refs={r['id']:r for r in data['reference_units']};sources={s['id']:s for s in data['source_positions']}
 routine={'BASE_AND_RECORDED_MARKS_AGREE','DECLARED_TRANSLITERATION_CONVENTION','UNICODE_REPRESENTATION_ONLY','EDITORIAL_SPACING_ONLY','NOTATION_AGREEMENT_ONLY','PRINT_LAYOUT_ONLY','LITERAL_DIGITAL_BREAK_MARKER'}
 items=[]
 for a in data['alignments']:
  r=refs.get(a['reference_unit']);s=sources.get(a['source_unit'])
  only_spacing=all(u is None or u['kind']=='SPACING' for u in [r,s])
  if a['alignment_ambiguous'] or (a['relation'] not in routine and not only_spacing):
   items.append({'alignment_id':a['id'],'relation':a['relation'],'alignment_ambiguous':a['alignment_ambiguous'],'disposition':'PENDING','reviewer':None,'rationale':None})
 return {'format':'tl55-sign-adjudication-packet-v1','status':'PREPARED_NOT_REVIEWED','input_alignment_sha256':hashlib.sha256((root/REGISTER).read_bytes()).hexdigest(),'original_review_packet':'review/tl55-independent-review.json','original_review_packet_sha256':hashlib.sha256((root/'review/tl55-independent-review.json').read_bytes()).hexdigest(),'reviewer':None,'assessment':None,'accepted_readings':[],'review_evidence':None,'item_count':len(items),'items':items,'rule':'Each item is a candidate comparison requiring attributable assessment, not an independently verified discrepancy. Review all source positions, not only this triage list; systematic algorithm or font errors can affect apparent agreements. Original source must be checked. No automated result closes expert adjudication.'}

def validate(root=ROOT,pdf=None):
 data=json.loads((root/REGISTER).read_text())
 if digest(data)!=PIN:raise ValueError('sign alignment, qualifications or gate state drift')
 for path,h in data['inputs'].items():
  if hashlib.sha256((root/path).read_bytes()).hexdigest()!=h:raise ValueError('sign comparison input drift')
 rows=[r for r in json.loads((root/'data/reference/lines.json').read_text()) if r['source_section']=='MIL-TL-055'];spans=json.loads((root/'research/tl55-first-pass-review.json').read_text())['reference_span_accounting']
 expected=[{k:v for k,v in r.items() if k!='base'} for r in reference_units(rows,spans)]
 if data['reference_units']!=expected:raise ValueError('literal grapheme/opaque notation loss')
 for key,field in [('reference_units','reference_unit'),('source_positions','source_unit')]:
  expected=collections.Counter(x['id'] for x in data[key]);seen=collections.Counter(x[field] for x in data['alignments'] if x[field] is not None)
  if seen!=expected or any(n!=1 for n in expected.values()):raise ValueError('unit omission, duplicate or unknown partner')
 if any(x['canonical_change'] or (x['alignment_ambiguous'] and x['status']!='UNRESOLVED_ALIGNMENT') for x in data['alignments']):raise ValueError('uncertainty or acceptance promotion')
 if json.loads((root/'review/tl55-sign-adjudication.json').read_text())!=adjudication_packet(root,data):raise ValueError('sign adjudication packet stale or unperformed review claimed')
 if pdf:
  from tl55_source_glyphs import extract
  source=extract(pdf)
  if build_from_source(root,source)!=data:raise ValueError('source glyph decoding or comparison replay differs')
 return {'status':'PASS_TL55_EXHAUSTIVE_SIGN_COMPARISON','source_pdf_replayed':bool(pdf),**data['summary'],'expert_adjudication':'OPEN','full_epigraphic_collation_certified':False}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--pdf',type=Path,help='Optional exact lawfully held source PDF; not copied into the repository');a=p.parse_args();print(json.dumps(validate(pdf=a.pdf),ensure_ascii=False))
