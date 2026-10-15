import json,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from build_collection_handoff import build,CONFIG,OUTPUTS
class TypedGlyphInputs(unittest.TestCase):
 def test_complete_hash_remains_while_glyphs_are_not_new_source_leads(self):
  with tempfile.TemporaryDirectory() as td:
   root=Path(td);(root/'research').mkdir();p=root/'research/glyphs.json';p.write_text(json.dumps({'source_label':'glyph','items':[{'status':'PENDING'}]}))
   cfg={'repository':'fixture/test','source_files':['research/glyphs.json'],'record_sets':[],'native_review_links':['research/glyphs.json'],'non_discovery_inputs':['research/glyphs.json']};(root/CONFIG).write_text(json.dumps(cfg));a=build(root)[OUTPUTS[0]]
   self.assertIn('research/glyphs.json',a['input_sha256']);self.assertEqual(a['source_leads'],[]);self.assertEqual(a['tasks'],[]);self.assertFalse(a['scientific_approval_granted'])
   p.write_text(p.read_text()+'\n');b=build(root)[OUTPUTS[0]];self.assertNotEqual(a['evidence_fingerprint'],b['evidence_fingerprint'])
   cfg['non_discovery_inputs']=['missing.json'];(root/CONFIG).write_text(json.dumps(cfg))
   with self.assertRaises(ValueError):build(root)
if __name__=='__main__':unittest.main()
