import copy,json,sys,tempfile,unittest,csv,io,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from tl55_sign_alignment import REGISTER,validate,reference_units,align,relation
from tl55_source_glyphs import decode,extract

def r(text,**extra):
 return dict(id=text,base=text,literal=text,kind='LETTER',marks=[],editorial_context={'square':False,'curly':False,'angle_entity':False},**extra)
def s(text):return dict(id=text,base=text,text=text,kind='LETTER',marks=[],square_bracket_context=False)
class SignAlignment(unittest.TestCase):
 def test_exhaustive_literal_coverage_and_source_position_accounting(self):
  report=validate();self.assertEqual(report['reference_grapheme_or_notation_units'],1348);self.assertEqual(report['source_rendered_glyph_or_notation_units'],1233);self.assertEqual(report['independent_reviews_added'],0)
  data=json.loads((ROOT/REGISTER).read_text());rows={r['id']:r['text'] for r in json.loads((ROOT/'data/reference/lines.json').read_text())}
  for rid in {u['row_id'] for u in data['reference_units']}:
   units=[u for u in data['reference_units'] if u['row_id']==rid]
   self.assertEqual(''.join(u['literal'] for u in units),rows[rid])
   self.assertEqual([u['start'] for u in units],[0]+[u['end'] for u in units[:-1]])
 def test_all_optimal_repeat_alignments_flagged(self):
  pairs,_=align([r('a'),r('a')],[s('a')]);self.assertTrue(all(p[2] for p in pairs))
  pairs,_=align([r('a')],[s('a'),s('a')]);self.assertTrue(all(p[2] for p in pairs))
 def test_unique_letter_difference_not_agreement(self):
  pairs,_=align([r('t')],[s('r')]);self.assertFalse(pairs[0][2]);self.assertEqual(relation(*pairs[0][:2]),'DIFFERENT_BASE_OR_NOTATION')
 def test_custom_fonts_and_unknown_source_fail_closed(self):
  self.assertEqual(decode('SabonLinguistic-Italic','r'),('m̃',[]));self.assertEqual(decode('SabonLinguistic-Italic','\\'),('ẽ',[]));self.assertEqual(decode('KronosPunkt','x'),('χ',['underdot']))
  with self.assertRaises(ValueError):decode('unknown','r')
  with tempfile.NamedTemporaryFile() as f:
   f.write(b'wrong edition');f.flush()
   with self.assertRaises(ValueError):extract(f.name)
 def test_qualifications_and_editorial_context_not_erased(self):
  a=r('a');b=s('a');b['marks']=['underdot'];self.assertEqual(relation(a,b),'BASE_AGREEMENT_QUALIFICATION_DIFFERS')
  a['editorial_context']['curly']=True;b['marks']=[];b['square_bracket_context']=True
  self.assertEqual(relation(a,b),'BASE_AGREEMENT_QUALIFICATION_DIFFERS')
 def test_alternative_does_not_become_single_accepted_reading(self):
  a=r('l');b=s('p/l');b.update(kind='ALTERNATIVE',alternatives=['p','l'])
  self.assertEqual(relation(a,b),'ALTERNATIVE_OVERLAP')
 def test_convention_and_unicode_not_literal_equality(self):
  self.assertEqual(relation(r('x'),s('χ')),'DECLARED_TRANSLITERATION_CONVENTION')
  a=r('ẽ');a['literal']='ẽ';self.assertEqual(relation(a,s('ẽ')),'UNICODE_REPRESENTATION_ONLY')
  self.assertEqual(relation(r('m͂'),s('m̃')),'DIFFERENT_BASE_OR_NOTATION')
 def test_public_data_excludes_source_transcription_and_no_acceptance(self):
  data=json.loads((ROOT/REGISTER).read_text());self.assertFalse(data['full_epigraphic_collation_certified']);self.assertEqual(data['independent_review_status'],'PENDING')
  self.assertTrue(all(not ({'text','base','raw_glyph','font'}&u.keys()) for u in data['source_positions']))
  self.assertEqual(sum(u['kind']=='ALTERNATIVE' for u in data['source_positions']),1)
  self.assertEqual(sum('underline' in u['marks'] for u in data['source_positions']),4)
 def test_api_json_csv_retains_source_and_reference_context(self):
  def api(*args):return subprocess.check_output([sys.executable,str(ROOT/'scripts/research_api.py'),'signs','--text','TL55-L2-A087',*args],text=True)
  rows=json.loads(api());self.assertEqual(len(rows),1);self.assertEqual(rows[0]['reference_position']['literal'],'ṭ');self.assertEqual(rows[0]['source_position']['marks'],['underdot']);self.assertEqual(rows[0]['expert_adjudication'],'PENDING')
  out=list(csv.DictReader(io.StringIO(api('--format','csv'))));self.assertEqual(json.loads(out[0]['reference_position']),rows[0]['reference_position']);self.assertEqual(json.loads(out[0]['source_position']),rows[0]['source_position'])
 def test_pending_adjudication_packet_cannot_claim_review(self):
  with tempfile.TemporaryDirectory() as td:
   root=Path(td);paths=[REGISTER,'review/tl55-sign-adjudication.json','review/tl55-independent-review.json']+list(json.loads((ROOT/REGISTER).read_text())['inputs'])
   for path in paths:
    q=root/path;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes((ROOT/path).read_bytes())
   q=root/'review/tl55-sign-adjudication.json';packet=json.loads(q.read_text());packet['reviewer']='AI';packet['status']='ACCEPTED';q.write_text(json.dumps(packet))
   with self.assertRaises(ValueError):validate(root)
 def test_omission_uncertainty_loss_and_fake_review_rejected(self):
  for mutate in [lambda d:d['alignments'].pop(),lambda d:d.update(independent_review_status='ACCEPTED'),lambda d:next(a for a in d['alignments'] if a['alignment_ambiguous']).update(status='AGREED')]:
   with tempfile.TemporaryDirectory() as td:
    root=Path(td);p=root/REGISTER;p.parent.mkdir(parents=True);data=json.loads((ROOT/REGISTER).read_text());mutate(data);p.write_text(json.dumps(data))
    with self.assertRaises(ValueError):validate(root)
if __name__=='__main__':unittest.main()
