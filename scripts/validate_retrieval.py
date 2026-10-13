"""Reproduce a labeled historical retrieval benchmark without changing DOI state."""
import argparse
from datetime import date
import json
from pathlib import Path
try:
    from .research import Crossref, normalize_doi, screen
except ImportError:
    from research import Crossref, normalize_doi, screen


def evaluate(records, config, live=False):
    client = Crossref()
    results = []
    for record in records:
        item = record['metadata']
        year = item['published']['date-parts'][0][0]
        since, until = f'{year}-01-01', f'{year}-12-31'
        topics, reason = screen(item, config, since, until)
        found, error = None, None
        if live and record['label'] == 'relevant':
            topic = next(t for t in config['topics'] if t['id'] == record['expected_topic'])
            try:
                items = client.search(topic['query'], since, until, config['rows_per_topic'])
                found = normalize_doi(item['DOI']) in {normalize_doi(x['DOI']) for x in items if x.get('DOI')}
            except Exception as exc:
                error = type(exc).__name__ + ': ' + str(exc)
        results.append({'doi': normalize_doi(item['DOI']), 'title': item['title'][0],
            'journal': item['container-title'][0], 'label': record['label'],
            'expected_topic': record['expected_topic'], 'publication_date': item['published']['date-parts'][0],
            'window': [since, until], 'source_url': record['source_url'],
            'search_found': found, 'search_error': error, 'screen_topics': topics, 'screen_reason': reason})
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--live', action='store_true', help='Repeat bounded Crossref search; otherwise evaluate cached bibliographic metadata only')
    parser.add_argument('--output', default='validation/offline-results.json')
    args = parser.parse_args()
    records = json.loads(Path('validation/fixtures.json').read_text())
    config = json.loads(Path('config/topics.json').read_text())
    results = evaluate(records, config, args.live)
    Path(args.output).write_text(json.dumps({'run_date': str(date.today()), 'live_search': args.live,
        'rows_per_topic': config['rows_per_topic'], 'results': results}, indent=2) + '\n')
    positive = [r for r in results if r['label'] == 'relevant']
    negative = [r for r in results if r['label'] == 'irrelevant']
    print(f'Positive screening retention: {sum(bool(r["screen_topics"]) for r in positive)}/{len(positive)}')
    print(f'Negative rejection: {sum(not r["screen_topics"] for r in negative)}/{len(negative)}')
    if args.live:
        print(f'Search retrieval: {sum(r["search_found"] is True for r in positive)}/{len(positive)}; API errors: {sum(bool(r["search_error"]) for r in positive)}')
    print('This small development set is not an independent estimate of production recall or precision.')


if __name__ == '__main__':
    main()
