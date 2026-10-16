"""Reject false source completion and dropped boundary qualifications."""
import copy
import importlib.util
import json
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('checkpoint', ROOT / 'scripts/tl44_source_checkpoint.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class SourceBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.register = json.loads((ROOT / module.REGISTER).read_text())
        self.reference = json.loads((ROOT / 'data/reference/lines.json').read_text())
        self.metadata = {year: json.loads((ROOT / f'research/source-metadata/crossref-tl44-{year}.json').read_text()) for year in (2016, 2018)}
    def audit(self):
        return module.audit(self.register, self.reference, self.metadata)
    def test_current_receipt(self):
        self.assertEqual(module.validate()['tl44d_label_routes'], 71)
    def test_missing_row_rejected(self):
        self.register['rows'].pop()
        with self.assertRaises(ValueError): self.audit()
    def test_physical_identity_promotion_rejected(self):
        self.register['rows'][0]['physical_line_identity_verified'] = True
        with self.assertRaises(ValueError): self.audit()
    def test_page_transition_rejected(self):
        self.register['rows'][-18]['kalinka_pdf_ordinal'] = 53
        with self.assertRaises(ValueError): self.audit()
    def test_metadata_is_not_pdf_acquisition(self):
        self.register['editions'][0]['article_pdf_acquired'] = True
        with self.assertRaises(ValueError): self.audit()
    def test_pagination_conflict_cannot_be_closed(self):
        self.register['editions'][1]['pagination_conflict']['status'] = 'RESOLVED'
        with self.assertRaises(ValueError): self.audit()
    def test_frozen_fragment_cannot_be_moved(self):
        row = next(r for r in self.reference if r['id'] == 'EDIANA-MILYAN-1-ROW-33')
        row['text'] = row['text'].replace('//rã :', '')
        with self.assertRaises(ValueError): self.audit()

if __name__ == '__main__': unittest.main()
