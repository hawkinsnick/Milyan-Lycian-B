#!/usr/bin/env python3
"""Replay the frozen eDiAna digital reference; no critical-reading promotion."""
import argparse, hashlib, json, xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RAW='data/reference/ediana-milyan-source.json'
RAW_SHA='e53dca3df71f06af95c0091646ee0d1b20fe6c78c1a24ac0f9b9e49cadd425a0'
NS='http://www.tei-c.org/ns/1.0';ET.register_namespace('',NS)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def node(parent,name,text=None,**attrs):
 e=ET.SubElement(parent,'{'+NS+'}'+name,attrs)
 if text is not None:e.text=text
 return e
def build(root=ROOT):
 raw=root/RAW
 if sha(raw)!=RAW_SHA:raise ValueError('frozen source digest drift')
 source=json.loads(raw.read_text());records=[];lines=[];crosswalk=[]
 expected={'TL 55 (Antiphellos)':('0',9),'TL 44 (Xanthos)':('1',105)}
 if set(source)!=set(expected):raise ValueError('source group drift')
 for group,rows in source.items():
  docid,n=expected[group];rid='EDIANA-MILYAN-'+docid;current=None;entries=[];headers=[]
  for index,row in enumerate(rows):
   if row['docid']!=docid or row['graph']!='line':raise ValueError('source row type or identity drift')
   if not row['sentence']:
    if row['word'] not in ['· TL 55 (Antiphellos)','· TL 44c (Xanthos)','· TL 44d (Xanthos)']:raise ValueError('unknown source section')
    current={'· TL 55 (Antiphellos)':'MIL-TL-055','· TL 44c (Xanthos)':'MIL-TL-044-C','· TL 44d (Xanthos)':'MIL-TL-044-D'}[row['word']]
    headers.append({'source_row':index,'label':row['word'],'bibliography':row['ref'],'candidate_project_segment':current});continue
   if current is None:raise ValueError('text without source header')
   line={'id':rid+'-ROW-'+str(index),'source_record_id':rid,'source_group':group,'source_row':index,'line_label':row['word'],'text':row['sentence'],'source_section':current,'source_locator':'/'+group+'/'+str(index),'source_url':'https://www.ediana.gwi.uni-muenchen.de/corpus.php?corpus=milyan&docid='+docid,'source_sha256':RAW_SHA,'raw_path':RAW,'language':'milyan','unit':'digital_source_text_row','status':'source_attributed_reference','license':'CC-BY-SA-4.0','canonical_reading_admitted':False,'independent_review':False,'physical_object_identity_verified':False,'annotation_policy':'Raw source annotations preserved in frozen JSON; interpretations are attributed, not adjudicated.'}
   entries.append(line);lines.append(line)
  if len(entries)!=n:raise ValueError('source text-row coverage drift')
  records.append({'id':rid,'source_id':docid,'label':group,'unit':'digital_catalogue_entry','source_headers':headers,'text_row_ids':[x['id'] for x in entries],'source_sha256':RAW_SHA,'source_url':entries[0]['source_url'],'license':'CC-BY-SA-4.0','canonical_reading_admitted':False,'independent_review':False})
  for h in headers:crosswalk.append({'source_record_id':rid,'source_header':h['label'],'source_row':h['source_row'],'project_segment':h['candidate_project_segment'],'relation':'source_label_correspondence','status':'source_attributed_not_physical_certification','bibliography':h['bibliography']})
 if len(lines)!=114 or len({x['id'] for x in lines})!=114:raise ValueError('reference coverage mismatch')
 counts={s:sum(x['source_section']==s for x in lines) for s in ['MIL-TL-055','MIL-TL-044-C','MIL-TL-044-D']}
 if list(counts.values())!=[9,34,71]:raise ValueError('section count drift')
 tei=ET.Element('{'+NS+'}TEI');header=node(tei,'teiHeader');desc=node(header,'fileDesc');title=node(desc,'titleStmt');node(title,'title','Frozen eDiAna Milyan digital reference; not a critically collated edition')
 pub=node(desc,'publicationStmt');node(pub,'publisher','hawkinsnick/Milyan-Lycian-B');av=node(pub,'availability',status='free');node(av,'licence','CC-BY-SA-4.0; source-derived component, no additional NC restriction.',target='https://creativecommons.org/licenses/by-sa/4.0/')
 src=node(desc,'sourceDesc');p=node(src,'p','Miller, Rieken, Hackstein and Yakubovich (eds.), eDiAna. Frozen source cached in Lycian-and-Carian commit 8ae31f14326b5162271ed699a53343d2c0b657b7. Individual lemma authors and primary editions remain controlling citations. ');node(p,'ref','eDiAna',target='https://www.ediana.gwi.uni-muenchen.de');node(p,'ref','Citation guidelines',target='https://www.ediana.gwi.uni-muenchen.de/assets/pdfs/citation.pdf')
 body=node(node(tei,'text'),'body');edition=node(body,'div',type='edition',subtype='source-attributed-digital-reference')
 for line in lines:
  part=node(edition,'div',type='textpart',subtype='digital-source-row',n=line['id']);node(part,'ab',line['text']);node(part,'note',json.dumps(line,ensure_ascii=False,sort_keys=True),type='native-record-json')
 xml=ET.tostring(tei,encoding='utf-8',xml_declaration=True)+b'\n';parsed=ET.fromstring(xml);back=[json.loads(x.text) for x in parsed.findall('.//{'+NS+'}note')];texts=[x.text for x in parsed.findall('.//{'+NS+'}ab')]
 if back!=lines or texts!=[x['text'] for x in lines]:raise ValueError('EpiDoc roundtrip loss')
 manifest={'schema_version':'1.0','source':{'authority':'eDiAna','cache_repository':'hawkinsnick/Lycian-and-Carian','cache_commit':'8ae31f14326b5162271ed699a53343d2c0b657b7','cache_path':'data/raw/ediana/milyan-1-0.json','raw_path':RAW,'sha256':RAW_SHA,'observation_date':'2026-10-11','acquisition':'Previously acquired frozen cache; direct live retrieval returned HTTP 403 on observation date. No fresh live-content replay claimed.'},'rights':{'license':'CC-BY-SA-4.0','evidence':'https://www.ediana.gwi.uni-muenchen.de/assets/pdfs/citation.pdf','locator':'p.1 citation and hyperlink policy; p.2 imprint','attribution':'Miller, Jared; Rieken, Elisabeth; Hackstein, Olav; Yakubovich, Ilya (eds.), 2017–, eDiAna. Cite individual lemma authors for interpretations and the printed editions listed in source headers.','change_notice':'Project-derived row IDs, provenance wrappers, section crosswalk and JSON/EpiDoc serialization; original source text strings preserved exactly.'},'coverage':{'digital_catalogue_records':2,'source_text_rows':114,'source_header_rows':3,'project_bibliographic_targets':3,'section_rows':counts,'canonical_verified_readings':0,'new_certified_physical_joins':0,'independent_reviews':0},'xml_sha256':hashlib.sha256(xml).hexdigest(),'roundtrip':'Every derived line field and exact source text preserved; raw annotations retained in source JSON, not converted into critical apparatus.','limits':['Source rows are not unique physical objects or independent witnesses.','Digital source segmentation and readings are not independently authenticated.','Brackets and combining marks remain opaque source transcription conventions; no graphical certainty is inferred.','Live source updates and critical-edition variant collation remain open.'],'scientific_approval_granted':False}
 return {'data/reference/records.json':records,'data/reference/lines.json':lines,'research/ediana-reference-crosswalk.json':crosswalk,'research/reference-manifest.json':manifest,'interchange/epidoc/milyan-reference.xml':xml}
def main():
 a=argparse.ArgumentParser();a.add_argument('--write',action='store_true');args=a.parse_args()
 for rel,obj in build().items():
  p=ROOT/rel;b=obj if isinstance(obj,bytes) else (json.dumps(obj,indent=2,ensure_ascii=False)+'\n').encode()
  if args.write:p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
  elif not p.exists() or p.read_bytes()!=b:raise SystemExit('stale reference output: '+rel)
 print('PASS: 2 source records, 114 rows, exact source text and EpiDoc roundtrip; no critical-edition certification')
if __name__=='__main__':main()
