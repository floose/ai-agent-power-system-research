"""Real bibliographic controls: reject prior off-topic records and expose retention losses."""
import json
from pathlib import Path
import unittest
from scripts.validate_retrieval import evaluate

class ValidationTests(unittest.TestCase):
    def test_labeled_controls(self):
        fixtures = json.loads(Path('validation/fixtures.json').read_text())
        self.assertEqual(len({r['metadata']['DOI'] for r in fixtures}), 15)
        self.assertEqual(sum(r['label'] == 'relevant' for r in fixtures), 10)
        self.assertTrue(all(r['source_url'].startswith('https://') for r in fixtures))
        results = evaluate(fixtures, json.loads(Path('config/topics.json').read_text()))
        for result in results:
            if result['label'] == 'irrelevant':
                self.assertEqual(result['screen_topics'], [], result['title'])
        self.assertTrue(all(r['search_found'] is None for r in results))
