import json,tempfile,unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from validate_tl55_reconciliation import ROOT,REGISTER,validate
class SourceBoundary(unittest.TestCase):
 def test_native(self):validate()
 def reject(self,fn):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d)
   for p in ['research/tl55-count-reconciliation-2026-10-14.json', 'data/reference/lines.json']:
    f=root/p;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes((ROOT/p).read_bytes())
   f=root/REGISTER;x=json.loads(f.read_text());fn(x);f.write_text(json.dumps(x))
   with self.assertRaises(ValueError):validate(root)
 def test_false_authority(self):self.reject(lambda x:x['historical_count'].update(voice='KALINKA_EDITION_COUNT'))
 def test_false_semantics(self):self.reject(lambda x:x.update(physical_line_count_certified=True))
 def test_scope_drift(self):self.reject(lambda x:x['reference'].update(rows=8))
if __name__=='__main__':unittest.main()
