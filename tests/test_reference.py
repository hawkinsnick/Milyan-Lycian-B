import copy,importlib.util,json,tempfile,unittest,xml.etree.ElementTree as ET,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('reference',ROOT/'scripts/build_reference.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class ReferenceTests(unittest.TestCase):
 def test_exact_source_replay_and_complete_rows(self):
  outputs=m.build();raw=json.loads((ROOT/m.RAW).read_text());lines=outputs['data/reference/lines.json'];self.assertEqual(len(lines),114)
  for row in lines:self.assertEqual(row['text'],raw[row['source_group']][row['source_row']]['sentence']);self.assertFalse(row['canonical_reading_admitted']);self.assertFalse(row['independent_review']);self.assertEqual(row['license'],'CC-BY-SA-4.0')
 def test_source_tampering_rejected(self):
  with tempfile.TemporaryDirectory() as t:
   root=Path(t);p=root/m.RAW;p.parent.mkdir(parents=True);p.write_bytes((ROOT/m.RAW).read_bytes()+b'\n')
   with self.assertRaisesRegex(ValueError,'digest drift'):m.build(root)
 def test_source_section_crosswalk_and_denominators(self):
  d=m.build();self.assertEqual(d['research/reference-manifest.json']['coverage']['section_rows'],{'MIL-TL-055':9,'MIL-TL-044-C':34,'MIL-TL-044-D':71});self.assertEqual(len(d['research/ediana-reference-crosswalk.json']),3)
  self.assertTrue(all(x['relation']=='source_label_correspondence' for x in d['research/ediana-reference-crosswalk.json']))
 def test_xml_roundtrip_every_field_and_text(self):
  d=m.build();doc=ET.fromstring(d['interchange/epidoc/milyan-reference.xml']);ns={'t':m.NS};self.assertEqual([json.loads(x.text) for x in doc.findall('.//t:note',ns)],d['data/reference/lines.json']);self.assertEqual([x.text for x in doc.findall('.//t:ab',ns)],[x['text'] for x in d['data/reference/lines.json']])
 def test_api_layers_do_not_promote_reference(self):
  def api(*args):return json.loads(subprocess.check_output([sys.executable,str(ROOT/'scripts/research_api.py'),*args],text=True))
  self.assertEqual(api('lines'),[]);self.assertEqual(len(api('lines','--layer','reference')),114);self.assertEqual(api('coverage')['verified_lines'],0);self.assertEqual(api('coverage','--layer','reference')['verified_readings'],0)
  self.assertEqual(api('kwic','--text','mlutene'),[]);self.assertTrue(api('kwic','--text','mlutene','--layer','reference'));self.assertEqual(api('kwic','--text','definitely-absent-token','--layer','reference'),[])
 def test_api_json_and_csv_retain_provenance(self):
  export=json.loads(subprocess.check_output([sys.executable,str(ROOT/'scripts/research_api.py'),'export','--layer','reference'],text=True));self.assertEqual(len(export['lines']),114);self.assertFalse(export['manifest']['scientific_approval_granted'])
  import csv,io
  rows=list(csv.DictReader(io.StringIO(subprocess.check_output([sys.executable,str(ROOT/'scripts/research_api.py'),'lines','--layer','reference','--format','csv'],text=True))));self.assertEqual(len(rows),114);self.assertEqual(rows[0]['source_sha256'],m.RAW_SHA);self.assertEqual(rows[0]['text'],export['lines'][0]['text'])
if __name__=='__main__':unittest.main()
