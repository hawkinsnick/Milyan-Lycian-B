import importlib.util,os,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class UpstreamTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  if not os.environ.get('EPIDOC_SCHEMA') or not os.environ.get('SCHEMATRON_COMPILER'):raise unittest.SkipTest('Upstream integration runs in the dedicated pinned-schema CI job')
  from lxml import etree
  cls.etree=etree;s=importlib.util.spec_from_file_location('upstream',ROOT/'scripts/validate_upstream_epidoc.py');cls.m=importlib.util.module_from_spec(s);s.loader.exec_module(cls.m);cls.schema=Path(os.environ['EPIDOC_SCHEMA']);cls.compiler=Path(os.environ['SCHEMATRON_COMPILER']);cls.xml=ROOT/'interchange/epidoc/milyan-reference.xml'
 def test_actual_upstream_rules_execute(self):
  d=self.m.validate(self.schema,self.compiler,self.xml);self.assertEqual(d['active_patterns'],57);self.assertGreater(d['fired_rules'],0);self.assertEqual(d['failed_asserts'],0)
 def test_schema_digest_mismatch_rejected(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'schema.rng';p.write_bytes(self.schema.read_bytes()+b'\n')
   with self.assertRaisesRegex(ValueError,'digest mismatch'):self.m.validate(p,self.compiler,self.xml)
 def test_compiler_digest_mismatch_rejected(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'iso_dsdl_include.xsl';p.write_text('tampered')
   with self.assertRaisesRegex(ValueError,'digest mismatch'):self.m.validate(self.schema,Path(d),self.xml)
 def test_upstream_nonfatal_report_rejects_adversarial_date(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'bad.xml';doc=self.etree.parse(str(self.xml));ns={'t':'http://www.tei-c.org/ns/1.0'};paragraph=doc.xpath('//t:sourceDesc/t:p',namespaces=ns)[0];date=self.etree.SubElement(paragraph,'{http://www.tei-c.org/ns/1.0}date',when='2026-10-11',notBefore='2026-10-10');date.text='Adversarial fixture';doc.write(str(p))
   with self.assertRaisesRegex(ValueError,'upstream Schematron findings'):self.m.validate(self.schema,self.compiler,p)
if __name__=='__main__':unittest.main()
