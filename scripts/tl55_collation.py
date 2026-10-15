"""Qualified TL55 source comparisons; never rewrite frozen readings or conflate edition layers."""
import argparse,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REGISTER='research/schuerr2005-tl55-collation.json'
OUTPUT='research/tl55-qualified-collation.json'
PIN='c0f4145b059c257ef03e9e6fd949a8f7fb5d5ce91c128aea4b629676187b276f'
def load(root,p):return json.loads((root/p).read_text())
def digest(x):return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def build(root=ROOT):
 c=load(root,REGISTER)
 if digest(c)!=PIN:raise ValueError('inspected source claims, layers, uncertainty or rights drift')
 for path,key in [(c['reference']['path'],'sha256'),(c['reference']['raw_path'],'raw_sha256')]:
  if hashlib.sha256((root/path).read_bytes()).hexdigest()!=c['reference'][key]:raise ValueError('frozen reference changed')
 rows=[r for r in load(root,c['reference']['path']) if r['source_section']=='MIL-TL-055']
 if len(rows)!=9 or len({r['id'] for r in rows})!=9:raise ValueError('reference row identity drift')
 index={r['id']:r for r in rows}
 for issue in c['issues']:
  for ref in issue['reference_rows']:
   row=index.get(ref['row_id']);offset=ref['offset'];fragment=ref['literal_fragment']
   if row is None or row['text'][offset:offset+len(fragment)]!=fragment:raise ValueError('wrong reference locus or opaque source text loss')
 if len(c['issues'])!=6 or len({i['id'] for i in c['issues']})!=6:raise ValueError('bounded issue set drift')
 result=[]
 for n,row in enumerate(rows,1):
  result.append({'reference_row_id':row['id'],'source_reference_row':row,'comparison_source':c['source']['citation'],'comparison_source_id':'schuerr2005','source_label':n,'source_transcription_printed_pages':c['source_line_structure']['transcription_pages'][str(n)],'source_apparatus_printed_pages':c['source_line_structure']['apparatus_pages'][str(n)],'label_alignment_status':'SOURCE_LABEL_CORRESPONDENCE_ONLY','full_row_text_equivalence_established':False,'issues':[i for i in c['issues'] if any(r['row_id']==row['id'] for r in i['reference_rows'])],'canonical_reading_admitted':False,'independent_review':False,'boundary':'A row without a selected issue has not passed complete critical collation. Source labels, text strings, physical lines, emendations and reconstructions remain different layers.'})
 return {'format':'milyan-qualified-tl55-collation-v1','source_checkpoint':REGISTER,'source_checkpoint_sha256':hashlib.sha256((root/REGISTER).read_bytes()).hexdigest(),'row_count':9,'selected_issue_count':6,'license':'CC-BY-SA-4.0','license_scope':'Qualified reference view and project comparison annotations; underlying Schürr article, images and editorial edition retain their source rights and are not relicensed.','attribution':'eDiAna editors and individual/source authors as specified by research/reference-manifest.json; Schürr2005 and Kalinka1901; project-added source comparisons and wrappers.','full_critical_collation_complete':False,'canonical_readings_added':0,'independent_reviews_added':0,'rows':result}
def validate(root=ROOT):
 data=build(root)
 if load(root,OUTPUT)!=data:raise ValueError('qualified comparison stale or altered')
 return {'status':'PASS_BOUNDED_TL55_PRIMARY_COMPARISON','source_labels_located':9,'selected_issues':6,'frozen_source_rows_unchanged':114,'canonical_readings_added':0,'independent_reviews_added':0,'complete_critical_collation':False}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');a=p.parse_args()
 if a.write:(ROOT/OUTPUT).write_text(json.dumps(build(),ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(validate()))
