"""Crossref candidate discovery; never infer scientific results from metadata."""
import argparse
from datetime import date, timedelta
import json
from pathlib import Path
import re
import time
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

try:
    from .triage import triage
except ImportError:
    from triage import triage

API = 'https://api.crossref.org'


def normalize_doi(value):
    value = re.sub(r'^https?://(?:dx\.)?doi\.org/', '', value.strip(), flags=re.I)
    value = re.sub(r'^doi:\s*', '', value, flags=re.I).lower()
    if not re.fullmatch(r'10\.\d{4,9}/\S+', value):
        raise ValueError('Invalid DOI syntax')
    return value


class Crossref:
    def __init__(self, contact='', opener=urlopen, sleeper=time.sleep):
        self.opener, self.sleeper = opener, sleeper
        self.agent = 'PowerSystemsAIResearch/0.1' + (f' (mailto:{contact})' if contact else '')

    def get(self, path, params=None):
        url = API + path + ('?' + urlencode(params) if params else '')
        for attempt in range(3):
            try:
                with self.opener(Request(url, headers={'User-Agent': self.agent}), timeout=30) as response:
                    payload = json.load(response)
                if payload.get('status') != 'ok' or 'message' not in payload:
                    raise ValueError('Malformed Crossref response')
                return payload['message']
            except HTTPError as exc:
                if exc.code not in (429, 500, 502, 503, 504) or attempt == 2:
                    raise
                self.sleeper(min(int(exc.headers.get('Retry-After', '2')) if exc.headers.get('Retry-After', '').isdigit() else 2 ** attempt, 60))
            except URLError:
                if attempt == 2:
                    raise
                self.sleeper(2 ** attempt)

    def search(self, query, since, until, rows):
        return self.get('/works', {'query.bibliographic': query,
            'filter': f'type:journal-article,from-pub-date:{since},until-pub-date:{until}',
            'rows': rows, 'sort': 'relevance', 'order': 'desc'})['items']

    def validate(self, doi):
        doi = normalize_doi(doi)
        item = self.get('/works/' + quote(doi, safe=''))
        if normalize_doi(item.get('DOI', '')) != doi:
            raise ValueError('DOI metadata mismatch')
        if item.get('type') != 'journal-article' or not item.get('title'):
            raise ValueError('Not a journal article with title')
        return item


def screen(item, config, since, until):
    decision = triage(item, config, since, until)
    return (decision['topics'] if decision['status'] == 'candidate' else []), decision['reason']


def discover(client, config, seen, since, until, audit=None):
    candidates = {}
    seen = {normalize_doi(x) for x in seen}
    for topic in config['topics']:
        for item in client.search(topic['query'], since, until, config['rows_per_topic']):
            try:
                doi = normalize_doi(item.get('DOI', ''))
            except ValueError:
                continue
            if doi in seen:
                continue
            if doi in candidates:
                continue
            preliminary_topics, reason = screen(item, config, since, until)
            if not preliminary_topics:
                if audit is not None:
                    audit.append({'doi': doi, 'query_topic': topic['id'], 'reason': reason,
                        'title': item.get('title', [''])[0], 'journal': item.get('container-title', []), **triage(item, config, since, until)})
                continue
            verified = client.validate(doi)  # API failures abort; no success-shaped partial report
            topics, reason = screen(verified, config, since, until)
            if audit is not None:
                audit.append({'doi': doi, 'query_topic': topic['id'], 'reason': reason,
                    'title': verified.get('title', [''])[0], 'journal': verified.get('container-title', []), **triage(verified, config, since, until)})
            if not topics:
                continue
            candidates[doi] = {'doi': doi, 'topics': topics,
                'title': verified['title'][0], 'journal': verified.get('container-title', [''])[0],
                'publisher': verified.get('publisher', ''), 'authors': verified.get('author', []),
                'publication_date': verified.get('published', {}).get('date-parts', []),
                'url': 'https://doi.org/' + quote(doi, safe='/'),
                'verification': 'Crossref DOI and journal-article metadata only',
                'peer_review': 'unconfirmed', 'relevance': reason + '; expert review required',
                'source_metadata': verified}
    priority = config['preferred_publishers']
    return sorted(candidates.values(), key=lambda p: (
        not any(j.casefold() in {name.casefold() for name in config['journals']} for j in p['source_metadata'].get('container-title', [])),
        not any(x.lower() in p['publisher'].lower() for x in priority), p['doi']))[:config['max_papers']]


def markdown(papers, since, until, audit=None):
    lines = [f'# Power Systems AI Research — {until}', '',
        f'Publication window: {since} to {until}. Discovery source: Crossref.', '',
        'Candidate report for expert review. DOI registration does not establish peer review, relevance, or scientific validity.', '',
        'Candidates passed publication-date interval, power-system context, AI-method and topic screening in title/abstract. This is not full-text acceptance.',
        'Search is bounded and non-exhaustive; publisher preference is not a quality guarantee.', '']
    if not papers:
        lines += ['No new DOI-validated candidates found in this bounded search.', '']
    for n, paper in enumerate(papers, 1):
        # Flatten metadata to prevent HTML/Markdown content injection.
        clean = lambda s: re.sub(r'[\r\n<>\[\]`*#]', ' ', str(s))
        lines += [f"## {n}. {clean(paper['title'])}", '',
            f"Journal: {clean(paper['journal'])}. Publisher: {clean(paper['publisher'])}.",
            f"DOI: [{clean(paper['doi'])}]({paper['url']})", '',
            f"Topics: {', '.join(paper['topics'])}.",
            'Verified: matching DOI and journal-article metadata returned by Crossref.',
            'Peer review and topical relevance: require publisher/expert verification.',
            'Methods: not assessed. Results: not assessed. Relevance: not assessed.',
            'Before inclusion: read the source and record methods, benchmarks, quantitative results, limitations and supporting page/section.', '']
    if audit is not None:
        pending = {r['doi']: r for r in audit if r.get('status') == 'pending'}
        lines += ['', '## Pending metadata review', '', f'{len(pending)} unique records require additional evidence. See JSON screening_audit; these records are not accepted papers.']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='config/topics.json')
    parser.add_argument('--since', type=date.fromisoformat)
    parser.add_argument('--until', type=date.fromisoformat, default=date.today())
    parser.add_argument('--output', default='reports')
    parser.add_argument('--seen', default='data/seen_dois.json')
    parser.add_argument('--contact', default='')
    args = parser.parse_args()
    config = json.loads(Path(args.config).read_text())
    since = args.since or args.until - timedelta(days=config['lookback_days'])
    if since > args.until:
        parser.error('--since must not exceed --until')
    seen_path = Path(args.seen)
    seen = json.loads(seen_path.read_text()) # missing/corrupt state must fail
    audit = []
    papers = discover(Crossref(args.contact), config, seen, since, args.until, audit)
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    # State, metadata and report are committed together by the PR workflow.
    (out / f'{args.until}.json').write_text(json.dumps({'window': [str(since), str(args.until)], 'papers': papers, 'screening_audit': audit}, indent=2) + '\n')
    handoff = [{'doi': p['doi'], 'title': p['title'], 'journal': p['journal'], 'topics': p['topics'], 'source_url': p['url'], 'state': 'awaiting_source_reading'} for p in papers]
    (out / f'{args.until}.handoff.json').write_text(json.dumps(handoff, indent=2) + '\n')
    (out / f'{args.until}.md').write_text(markdown(papers, since, args.until, audit))
    seen_path.write_text(json.dumps(sorted({normalize_doi(d) for d in seen} | {p['doi'] for p in papers}), indent=2) + '\n')


if __name__ == '__main__':
    main()
