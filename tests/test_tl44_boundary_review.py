import copy,json,sys,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'scripts'))
import tl44_boundary_review as m
import evidence_query as q
class BoundaryTests(unittest.TestCase):
    def setUp(self):
        self.d=json.loads((R/m.PACKET).read_text());self.ref=json.loads((R/'data/reference/lines.json').read_text());self.req=json.loads((R/'review/tl44-boundary-human-request.json').read_text())
    def test_current_exact_inventory_and_query_context(self):
        self.assertEqual(m.validate()['literal_boundary_markers'],47)
        e=q.Evidence(R);d=e.dossier('TL44-C40-MARKER-1','tl44-boundary-contexts');self.assertEqual(d['native_record']['proposed_printed_context'],['c39','c40']);self.assertEqual(d['collection_context']['limits']['canonical_readings_added'],0)
    def test_omission_and_normalized_brackets_rejected(self):
        d=copy.deepcopy(self.d);d['markers'].pop()
        with self.assertRaises(ValueError):m.audit(d,self.ref,self.req)
        d=copy.deepcopy(self.d);next(x for x in d['markers'] if x['id']=='TL44-C42-MARKER-1')['literal_suffix']='adi'
        with self.assertRaises(ValueError):m.audit(d,self.ref,self.req)
    def test_exception_cannot_use_generic_next_label(self):
        d=copy.deepcopy(self.d);next(x for x in d['markers'] if x['id']=='TL44-C40-MARKER-1')['proposed_printed_context']=['c40','c41']
        with self.assertRaises(ValueError):m.audit(d,self.ref,self.req)
    def test_gaps_overlaps_or_invented_sign_units_rejected(self):
        for key,value in [('start',1),('role','ancient_sign')]:
            d=copy.deepcopy(self.d);d['rows'][0]['spans'][0][key]=value
            with self.assertRaises(ValueError):m.audit(d,self.ref,self.req)
    def test_comparison_cannot_become_review(self):
        d=copy.deepcopy(self.d);d['markers'][0]['independent_review']=True
        with self.assertRaises(ValueError):m.audit(d,self.ref,self.req)
        r=copy.deepcopy(self.req);r['reviewer']='AI'
        with self.assertRaises(ValueError):m.audit(self.d,self.ref,r)
    def test_wrong_page_context_rejected(self):
        d=copy.deepcopy(self.d);d['markers'][0]['printed_pages']=[44]
        with self.assertRaises(ValueError):m.audit(d,self.ref,self.req)
    def test_boolean_cannot_replace_count(self):
        d=copy.deepcopy(self.d);d['limits']['canonical_readings_added']=False
        with self.assertRaises(ValueError):m.audit(d,self.ref,self.req)
if __name__=='__main__':unittest.main()
