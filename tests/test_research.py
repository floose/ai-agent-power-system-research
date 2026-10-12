import io
import unittest
from unittest.mock import Mock
from urllib.error import HTTPError, URLError
from scripts.research import Crossref, discover, markdown, normalize_doi
# Synthetic fixtures, not scientific references.
DOI = '10.99999/test-fixture'
ITEM = {'DOI': DOI, 'type': 'journal-article', 'title': ['Synthetic fixture'], 'publisher': 'IEEE'}
CONFIG = {'topics': [{'id': 'opf', 'query': 'opf'}, {'id': 'bess', 'query': 'bess'}], 'rows_per_topic': 5, 'max_papers': 5, 'preferred_publishers': ['IEEE']}
class Tests(unittest.TestCase):
    def test_normalization(self):
        self.assertEqual(normalize_doi(' HTTPS://DOI.ORG/10.99999/TEST-FIXTURE '), DOI)
        self.assertEqual(normalize_doi('doi: 10.99999/Test-Fixture'), DOI)
        for bad in ['', 'abc', '10.12/x', '10.99999/has space']:
            with self.assertRaises(ValueError): normalize_doi(bad)
    def test_duplicates_and_seen(self):
        client = Mock()
        client.search.return_value = [ITEM, ITEM, {'DOI': 'bad'}]
        client.validate.return_value = ITEM
        papers = discover(client, CONFIG, [], '2026-01-01', '2026-01-30')
        self.assertEqual(len(papers), 1)
        self.assertEqual(papers[0]['topics'], ['opf', 'bess'])
        client.validate.assert_called_once_with(DOI)
        self.assertEqual(discover(client, CONFIG, [DOI.upper()], '2026-01-01', '2026-01-30'), [])
        self.assertIn('Results: not assessed', markdown(papers, 'start', 'end'))
    def test_validation(self):
        client = Crossref()
        for fields in [{'DOI': '10.99999/other'}, {'type': 'posted-content'}, {'title': []}]:
            client.get = Mock(return_value={**ITEM, **fields})
            with self.assertRaises(ValueError): client.validate(DOI)
    def test_retry(self):
        opener = Mock(side_effect=[HTTPError('url',429,'limited',{},None), io.BytesIO(b'{"status":"ok","message":{}}')])
        sleeper = Mock()
        self.assertEqual(Crossref(opener=opener, sleeper=sleeper).get('/works'), {})
        self.assertEqual(opener.call_count, 2)
        self.assertEqual(opener.call_args.kwargs['timeout'], 30)
        sleeper.assert_called_once()
    def test_permanent_errors(self):
        opener = Mock(side_effect=HTTPError('url',404,'missing',{},None))
        with self.assertRaises(HTTPError): Crossref(opener=opener).get('/works')
        self.assertEqual(opener.call_count,1)
        opener = Mock(side_effect=URLError('offline'))
        with self.assertRaises(URLError): Crossref(opener=opener,sleeper=Mock()).get('/works')
        self.assertEqual(opener.call_count,3)
    def test_failure_aborts(self):
        client = Mock()
        client.search.return_value = [ITEM]
        client.validate.side_effect = URLError('offline')
        with self.assertRaises(URLError): discover(client,CONFIG,[],'start','end')
    def test_empty(self):
        self.assertIn('No new DOI-validated', markdown([], 'start', 'end'))
if __name__ == '__main__': unittest.main()
