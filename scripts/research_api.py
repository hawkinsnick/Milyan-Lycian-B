#!/usr/bin/env python3
"""Read-only evidence-first corpus query interface; no fabricated text."""
import argparse
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(name): return json.loads((ROOT/'data'/name).read_text(encoding='utf-8'))
def main():
    p=argparse.ArgumentParser(description="Milyan corpus read-only researcher interface")
    p.add_argument('command',choices=['inscriptions','lines','kwic','coverage','export'])
    p.add_argument('--text',default='',help='Case-insensitive query; KWIC searches only attested line readings')
    p.add_argument('--format',choices=['json','csv'],default='json')
    p.add_argument('--layer',choices=['canonical','reference'],default='canonical',help='Source-attributed digital reference is separate from canonical verified readings')
    a=p.parse_args()
    inscriptions=load('inscriptions.json');lines=load('lines.json')
    reference_records=load('reference/records.json');reference_lines=load('reference/lines.json')
    if a.layer=='reference':
        if a.command=='coverage': result={'layer':'source_attributed_reference','records':len(reference_records),'text_rows':len(reference_lines),'verified_readings':0,'independent_review':False,'warning':'Digital source rows are not unique physical objects or an independently collated edition.'}
        elif a.command=='inscriptions': result=[r for r in reference_records if a.text.casefold() in json.dumps(r,ensure_ascii=False).casefold()]
        elif a.command=='lines': result=reference_lines
        elif a.command=='kwic':
            if not a.text:p.error('kwic requires --text')
            result=[dict(r,match_basis='literal casefolded source string; no restoration or lexical adjudication') for r in reference_lines if a.text.casefold() in r['text'].casefold()]
        else:result={'records':reference_records,'lines':reference_lines,'manifest':json.loads((ROOT/'research/reference-manifest.json').read_text()),'warning':'Source-attributed reference only; cite original eDiAna and primary editions.'}
        emit(result,a,p);return
    if a.command=='inscriptions': result=[r for r in inscriptions if a.text.casefold() in json.dumps(r,ensure_ascii=False).casefold()]
    elif a.command=='lines': result=lines
    elif a.command=='kwic':
        if not a.text: p.error('kwic requires --text')
        result=[{'id':line['id'],'line':line['line_label'],'reading':reading['text'],'source':reading['source']} for line in lines for reading in line['readings'] if a.text.casefold() in reading['text'].casefold()]
    elif a.command=='coverage':
        result={'inscription_segments':len(inscriptions),'verified_segments':sum(x['status']=='verified' for x in inscriptions),'line_records':len(lines),'verified_lines':sum(x['status']=='verified' for x in lines),'text_available':any(x['readings'] for x in lines),'warning':'No verified transcription: absence of KWIC hits is not evidence of lexical absence.'}
    else: result={'inscriptions':inscriptions,'lines':lines,'warning':'Export includes provisional bibliographic targets; not an authenticated text edition.'}
    emit(result,a,p)
def emit(result,a,p):
    if a.format=='json':print(json.dumps(result,ensure_ascii=False,indent=2))
    else:
        import csv,sys
        if not isinstance(result,list):p.error('CSV only supported for list-producing commands')
        if not result:print('No records');return
        fields=sorted({k for row in result for k in row})
        writer=csv.DictWriter(sys.stdout,fieldnames=fields);writer.writeheader()
        for row in result:writer.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else v for k,v in row.items()})
if __name__=='__main__':main()
