import copy,csv,io,json,subprocess,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from tl55_documentary_review import REGISTER,validate,audit_cases,audit_source_pairs
class DocumentaryCompletion(unittest.TestCase):
 def setUp(self):
  self.review=json.loads((ROOT/REGISTER).read_text());self.alignment=json.loads((ROOT/'research/tl55-sign-alignment.json').read_text());self.packet=json.loads((ROOT/'review/tl55-sign-adjudication.json').read_text())
 def test_every_flag_has_one_documentary_disposition_and_expert_pending(self):
  report=validate();self.assertEqual(report['remaining_unreviewed_flagged_records'],0);self.assertEqual(report['flagged_records_reviewed'],152);self.assertEqual(report['positional_explanation_records']+report['repeated_run_records_without_unique_point_pairing']+report['range_only_records_without_unique_point_pairing'],36);self.assertEqual(report['expert_adjudication'],'OPEN');self.assertEqual(self.packet['status'],'PREPARED_NOT_REVIEWED')
 def test_no_missing_or_duplicated_case_coverage(self):
  for mutate in [lambda r:r['cases'][0]['alignment_ids'].pop(),lambda r:r['cases'][1]['alignment_ids'].append(r['cases'][0]['alignment_ids'][0]),lambda r:r['cases'][0]['algorithm_ambiguous_records'].pop()]:
   bad=copy.deepcopy(self.review);mutate(bad)
   with self.assertRaises(ValueError):audit_cases(bad,self.alignment,self.packet)
 def test_range_correspondence_cannot_claim_unique_epigraphic_pair(self):
  bad=copy.deepcopy(self.review);next(c for c in bad['cases'] if c['ambiguity_disposition']=='RANGE_ONLY_NO_UNIQUE_POINT_MAPPING')['unique_point_mapping_claimed']=True
  with self.assertRaises(ValueError):audit_cases(bad,self.alignment,self.packet)
 def test_extra_repeated_ancient_sign_identity_not_claimed(self):
  bad=copy.deepcopy(self.review);next(c for c in bad['cases'] if 'repeated_run' in c)['repeated_run']['identity_of_extra_ancient_sign_established']=True
  with self.assertRaises(ValueError):audit_cases(bad,self.alignment,self.packet)
 def test_source_placeholder_is_not_a_bracket_or_an_accepted_letter(self):
  review={'cases':[{'preferred_documentary_correspondences':[{'reference_unit':'r','source_unit':'s','relation':'RESTORED_TO_UNKNOWN_POSITION'}]}]};refs={'r':{'kind':'LETTER'}}
  audit_source_pairs(review,refs,{'s':{'text':'.'}})
  for text in [']','a']:
   with self.assertRaises(ValueError):audit_source_pairs(review,refs,{'s':{'text':text}})
 def test_public_api_retains_range_only_status_and_csv_context(self):
  def api(*args):return subprocess.check_output([sys.executable,str(ROOT/'scripts/research_api.py'),'sign-review','--text','TL55-REVIEW-55',*args],text=True)
  row=json.loads(api())[0];self.assertEqual(row['ambiguity_disposition'],'REPEATED_RUN_NO_UNIQUE_POINT_MAPPING');self.assertFalse(row['unique_point_mapping_claimed']);c=list(csv.DictReader(io.StringIO(api('--format','csv'))))[0];self.assertEqual(json.loads(c['repeated_run']),row['repeated_run'])
  signs=json.loads(subprocess.check_output([sys.executable,str(ROOT/'scripts/research_api.py'),'signs','--text','TL55-L8-A062'],text=True));self.assertTrue(signs[0]['alignment_ambiguous']);self.assertEqual(signs[0]['documentary_review']['id'],'TL55-REVIEW-55');self.assertEqual(signs[0]['expert_adjudication'],'PENDING')
 def test_report_cannot_be_rewritten_as_expert_acceptance(self):
  with tempfile.TemporaryDirectory() as td:
   root=Path(td);p=root/REGISTER;p.parent.mkdir(parents=True);self.review['scope']['accepted_readings_added']=1;p.write_text(json.dumps(self.review))
   with self.assertRaises(ValueError):validate(root)
if __name__=='__main__':unittest.main()
