#!/usr/bin/env python3
"""Validate the frozen Milyan reference against hash-pinned upstream RNG and embedded rules."""
import argparse,hashlib,json,tempfile
from pathlib import Path
from lxml import etree,isoschematron
from saxonche import PySaxonProcessor
ROOT=Path(__file__).resolve().parents[1]
SCH='http://purl.oclc.org/dsdl/schematron';SVRL='http://purl.oclc.org/dsdl/svrl'
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def verified(path,expected):
 if digest(path)!=expected:raise ValueError('upstream digest mismatch: '+str(path))
def validate(schema,compiler,xml):
 pins=json.loads((ROOT/'interchange/epidoc/upstream-pins.json').read_text());schema=Path(schema);compiler=Path(compiler);xml=Path(xml)
 verified(schema,pins['schema']['sha256'])
 for rel,sha in pins['compiler']['files_sha256'].items():verified(compiler/rel,sha)
 parser=etree.XMLParser(resolve_entities=False,no_network=True)
 native=etree.parse(str(schema),parser);doc=etree.parse(str(xml),parser)
 rng=etree.RelaxNG(native)
 if not rng.validate(doc):raise ValueError('upstream Relax NG rejected: '+str(rng.error_log))
 extracted=isoschematron.extract_rng(native);extracted.getroot().set('queryBinding','xslt2')
 patterns=len(extracted.xpath('//s:pattern',namespaces={'s':SCH}));rules=len(extracted.xpath('//s:rule',namespaces={'s':SCH}))
 if (patterns,rules)!=(pins['schema']['embedded_patterns'],pins['schema']['embedded_rules']):raise ValueError('incomplete upstream rule extraction')
 with tempfile.TemporaryDirectory() as tmp:
  p=Path(tmp);extracted.write(str(p/'extracted.sch'))
  with PySaxonProcessor(license=False) as processor:
   xslt=processor.new_xslt30_processor();source=p/'extracted.sch'
   for style,target in [('iso_dsdl_include.xsl','included.sch'),('iso_abstract_expand.xsl','expanded.sch'),('iso_svrl_for_xslt2.xsl','validator.xsl')]:
    out=p/target;xslt.transform_to_file(source_file=str(source),stylesheet_file=str(compiler/style),output_file=str(out));source=out
   xslt.transform_to_file(source_file=str(xml.resolve()),stylesheet_file=str(source),output_file=str(p/'result.xml'))
  result=etree.parse(str(p/'result.xml'),parser);ns={'s':SVRL}
  events=result.xpath('//s:failed-assert|//s:successful-report',namespaces=ns)
  active=len(result.xpath('//s:active-pattern',namespaces=ns));fired=len(result.xpath('//s:fired-rule',namespaces=ns))
  if active!=patterns or fired==0:raise ValueError('upstream rules not executed')
  if events:raise ValueError('upstream Schematron findings: '+ '; '.join(' '.join(x.itertext()).strip() for x in events))
 return {'status':'PASS_FROZEN_EDIANA_REFERENCE_VIEW_ONLY','schema_sha256':digest(schema),'xml_sha256':digest(xml),'embedded_patterns':patterns,'embedded_rules':rules,'active_patterns':active,'fired_rules':fired,'failed_asserts':0,'successful_reports':0,'scope':'114 eDiAna source text rows; not complete epigraphic corpus coverage or independent expert acceptance','all_schematron_reports_block_acceptance':True}
def main():
 a=argparse.ArgumentParser();a.add_argument('--schema',type=Path,required=True);a.add_argument('--compiler',type=Path,required=True);a.add_argument('--write',action='store_true');args=a.parse_args();d=validate(args.schema,args.compiler,ROOT/'interchange/epidoc/milyan-reference.xml');p=ROOT/'analysis/upstream-epidoc-validation.json';text=json.dumps(d,indent=2)+'\n'
 if args.write:p.write_text(text)
 elif not p.exists() or p.read_text()!=text:raise SystemExit('upstream validation report stale')
 print(text,end='')
if __name__=='__main__':main()
