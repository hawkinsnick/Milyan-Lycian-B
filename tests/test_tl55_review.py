import copy,json,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from tl55_review import REVIEW,PACKET,validate,audit_spans
class FullPassCoverage(unittest.TestCase):
 def setUp(self):
  self.review=json.loads((ROOT/REVIEW).read_text());self.rows=[r for r in json.loads((ROOT/'data/reference/lines.json').read_text()) if r['source_section']=='MIL-TL-055']
 def test_all_entries_and_markers(self):
  r=validate();self.assertEqual(r['apparatus_entries_reviewed'],74);self.assertEqual(r['digital_break_markers_accounted_for'],4);self.assertEqual(r['independent_reviews'],0)
 def test_gap_and_duplicate_rejected(self):
  spans=self.review['reference_span_accounting']
  for bad in [spans[1:],spans+[spans[-1]]]:
   with self.assertRaises(ValueError):audit_spans(self.rows,bad)
 def test_literal_and_carryover_loss_rejected(self):
  for key,value in [('literal_sha256','0'*64),('source_label',2)]:
   spans=copy.deepcopy(self.review['reference_span_accounting']);spans[0][key]=value
   with self.assertRaises(ValueError):audit_spans(self.rows,spans)
 def test_break_marker_is_not_a_sign(self):
  spans=copy.deepcopy(self.review['reference_span_accounting']);next(x for x in spans if x['kind']=='LITERAL_DIGITAL_BREAK_MARKER')['source_label']=2
  with self.assertRaises(ValueError):audit_spans(self.rows,spans)
 def test_missing_entry_or_fake_review_rejected(self):
  for target in [REVIEW,PACKET]:
   with tempfile.TemporaryDirectory() as d:
    root=Path(d)
    for p in [REVIEW,PACKET]:
     q=root/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes((ROOT/p).read_bytes())
    q=root/target;data=json.loads(q.read_text())
    if target==REVIEW:data['apparatus_entries'].pop()
    else:data.update(status='ACCEPTED',reviewer='AI')
    q.write_text(json.dumps(data))
    with self.assertRaises(ValueError):validate(root)
if __name__=='__main__':unittest.main()
