import csv,io,json,subprocess,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from tl55_collation import REGISTER,OUTPUT,build,validate
class CollationBoundary(unittest.TestCase):
 def reject(self,path,mutate):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d)
   for p in [REGISTER,OUTPUT,'data/reference/lines.json','data/reference/ediana-milyan-source.json']:
    q=root/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes((ROOT/p).read_bytes())
   q=root/path;x=json.loads(q.read_text());mutate(x);q.write_text(json.dumps(x))
   with self.assertRaises(ValueError):validate(root)
 def test_all_nine_labels_and_original_source_fields(self):
  data=build();native=json.loads((ROOT/'data/reference/lines.json').read_text())
  self.assertEqual([r['source_reference_row'] for r in data['rows']],[r for r in native if r['source_section']=='MIL-TL-055'])
  self.assertEqual([r['source_label'] for r in data['rows']],list(range(1,10)))
  self.assertEqual(data['selected_issue_count'],6);self.assertTrue(all(not r['full_row_text_equivalence_established'] for r in data['rows']))
  validate()
 def test_frozen_row_cannot_be_corrected(self):self.reject('data/reference/lines.json',lambda x:x[0].update(text='corrected'))
 def test_alternative_cannot_be_erased(self):self.reject(REGISTER,lambda x:x['issues'][2]['source'].update(claim='Certain l only'))
 def test_qualified_preference_cannot_be_certain(self):self.reject(REGISTER,lambda x:x['issues'][1]['source'].update(qualification='certain'))
 def test_reconstruction_cannot_become_graphic_layer(self):self.reject(REGISTER,lambda x:x['source_layers'][2].update(id='revised_transcription_and_apparatus'))
 def test_access_does_not_grant_bulk_rights(self):self.reject(REGISTER,lambda x:x['rights'].update(permission_for_bulk_republication_established=True))
 def test_source_labels_do_not_certify_physical_lines(self):self.reject(REGISTER,lambda x:x['source_line_structure'].update(physical_line_count_certified=True))
 def test_missing_context_rejected(self):self.reject(OUTPUT,lambda x:x['rows'][3].pop('issues'))
 def test_api_csv_roundtrip_and_no_canonical_growth(self):
  def api(*args):return subprocess.check_output([sys.executable,str(ROOT/'scripts/research_api.py'),*args],text=True)
  rows=json.loads(api('collation'));self.assertEqual(len(rows),9)
  csvrows=list(csv.DictReader(io.StringIO(api('collation','--format','csv'))))
  for r,c in zip(rows,csvrows):
   self.assertEqual(r['source_reference_row'],json.loads(c['source_reference_row']));self.assertEqual(r['issues'],json.loads(c['issues']))
  self.assertEqual(json.loads(api('lines')),[])
  self.assertEqual(json.loads(api('coverage'))['verified_lines'],0)
  self.assertEqual(len(json.loads(api('lines','--layer','reference'))),114)
if __name__=='__main__':unittest.main()
