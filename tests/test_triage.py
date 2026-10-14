import json
from pathlib import Path
import unittest
from scripts.triage import triage

class TriageTests(unittest.TestCase):
    def setUp(self):
        self.config = json.loads(Path('config/topics.json').read_text())
        self.item = {'title': ['Machine learning optimal power flow for power systems'],
                     'container-title': ['Unlisted journal'], 'published': {'date-parts': [[2024]]}}
    def test_journal_is_not_gate(self):
        d = triage(self.item, self.config, '2024-01-01', '2024-12-31')
        self.assertEqual(d['status'], 'candidate')
        self.assertFalse(d['preferred_journal'])
        self.assertTrue(d['evidence']['grid'])
    def test_chemistry_rejected(self):
        item = {**self.item, 'title': ['Machine learning electrode-electrolyte interphase chemistry']}
        self.assertEqual(triage(item,self.config,'2024-01-01','2024-12-31')['status'],'out_of_scope')
    def test_sparse_metadata_abstains(self):
        item = {**self.item, 'title': ['Operator learning for digital twins']}
        self.assertEqual(triage(item,self.config,'2024-01-01','2024-12-31')['status'],'pending')
    def test_date_abstention(self):
        self.assertEqual(triage(self.item,self.config,'2024-01-01','2024-02-01')['status'],'pending')
    def test_abstract_supplies_missing_context(self):
        item = {**self.item, 'title': ['A new learning architecture'], 'abstract': '<p>A neural network solves optimal power flow in power systems.</p>'}
        self.assertEqual(triage(item,self.config,'2024-01-01','2024-12-31')['status'],'candidate')
