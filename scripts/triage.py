"""Deterministic, evidence-bearing triage; no model inference or training."""
import calendar
from datetime import date
import html
import re


def evidence(text, patterns):
    return list(dict.fromkeys(m.group(0) for p in patterns for m in re.finditer(p, text, re.I)))


def triage(item, config, since, until):
    title = html.unescape(' '.join(item.get('title', [])))
    abstract = html.unescape(re.sub(r'<[^>]+>', ' ', item.get('abstract', '')))
    text = title + ' ' + abstract
    grid = evidence(text, config['grid_patterns'])
    method = evidence(text, config['ai_patterns'])
    topics = {t['id']: evidence(text, t['patterns']) for t in config['topics']}
    topics = {k: v for k, v in topics.items() if v}
    exclusions = evidence(title, config.get('exclude_title_patterns', []))
    journals = {j.casefold() for j in config['journals']}
    preferred = any(j.casefold() in journals for j in item.get('container-title', []))
    result = {'status': 'pending', 'reason': '', 'topics': list(topics),
              'evidence': {'grid': grid, 'method': method, 'topics': topics,
                           'exclusions': exclusions}, 'preferred_journal': preferred,
              'rules_version': config.get('rules_version', '1'),
              'metadata_source': 'title+abstract' if abstract else 'title only'}
    def finish(status, reason):
        result.update(status=status, reason=reason)
        return result
    if exclusions and not grid:
        return finish('out_of_scope', 'Explicit non-grid application in title')
    if not (grid and method and topics):
        return finish('pending', 'Insufficient evidence for grid application, method or topic')
    parts = item.get('published', {}).get('date-parts', [[]])[0]
    try:
        if len(parts) == 1:
            earliest, latest = date(parts[0], 1, 1), date(parts[0], 12, 31)
        elif len(parts) == 2:
            earliest = date(parts[0], parts[1], 1)
            latest = date(parts[0], parts[1], calendar.monthrange(*parts)[1])
        elif len(parts) == 3:
            earliest = latest = date(*parts)
        else:
            return finish('pending', 'Publication date unavailable')
    except (ValueError, TypeError):
        return finish('pending', 'Invalid publication date')
    result['date_interval'] = [str(earliest), str(latest)]
    lower, upper = date.fromisoformat(str(since)), date.fromisoformat(str(until))
    if latest < lower or earliest > upper:
        return finish('out_of_scope', 'Outside report publication window')
    if earliest < lower or latest > upper:
        return finish('pending', 'Partial date overlaps window boundary')
    return finish('candidate', 'Explicit grid, method and topic evidence; date interval contained')
