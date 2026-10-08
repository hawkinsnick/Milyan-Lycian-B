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
    a=p.parse_args()
    inscriptions=load('inscriptions.json');lines=load('lines.json')
    if a.command=='inscriptions': result=[r for r in inscriptions if a.text.casefold() in json.dumps(r,ensure_ascii=False).casefold()]
    elif a.command=='lines': result=lines
    elif a.command=='kwic':
        if not a.text: p.error('kwic requires --text')
        result=[{'id':line['id'],'line':line['line_label'],'reading':reading['text'],'source':reading['source']} for line in lines for reading in line['readings'] if a.text.casefold() in reading['text'].casefold()]
    elif a.command=='coverage':
        result={'inscription_segments':len(inscriptions),'verified_segments':sum(x['status']=='verified' for x in inscriptions),'line_records':len(lines),'verified_lines':sum(x['status']=='verified' for x in lines),'text_available':any(x['readings'] for x in lines),'warning':'No verified transcription: absence of KWIC hits is not evidence of lexical absence.'}
    else: result={'inscriptions':inscriptions,'lines':lines,'warning':'Export includes provisional bibliographic targets; not an authenticated text edition.'}
    if a.format=='json':print(json.dumps(result,ensure_ascii=False,indent=2))
    else:
        import csv,sys
        if not isinstance(result,list):p.error('CSV only supported for list-producing commands')
        if not result:print('No records');return
        fields=sorted({k for row in result for k in row})
        writer=csv.DictWriter(sys.stdout,fieldnames=fields);writer.writeheader()
        for row in result:writer.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else v for k,v in row.items()})
if __name__=='__main__':main()
