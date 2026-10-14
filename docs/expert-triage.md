# Low-cost expert triage

## Scope

This stage uses deterministic Python rules, not a trained classifier or an LLM. It consumes DOI metadata already returned by retrieval. There are no GPT calls, model weights or API keys in the routine screening path.

Three decisions are explicit:

- `candidate`: independent evidence for a grid application, an in-scope method and a topic, with a publication-date interval fully inside the window. This is permission to investigate, not scientific acceptance.
- `out_of_scope`: explicit non-grid application or a date interval wholly outside the report window.
- `pending`: incomplete application/method evidence, absent dates or ambiguous date boundaries. Missing metadata is not treated as irrelevance.

Journal membership influences ranking only. It cannot override content evidence or reject an otherwise relevant application. Title exclusions are applied only when grid evidence is absent, to reduce accidental rejection of interdisciplinary work. Every decision includes matched terms, rule version, metadata availability and reason in `screening_audit`.

## GPT handoff

`reports/YYYY-MM-DD.handoff.json` contains at most five selected candidates with DOI, title, journal, topic and source URL. It contains no fabricated methods or results. Python does not invoke GPT. A future reading stage obtains legitimate source text, confirms relevance, extracts supported scientific findings and proposes a Markdown entry through a PR. If only an abstract is available, label the analysis accordingly; do not present it as full-text review.

The reading stage should flag a false positive with DOI, evidence and proposed rule correction. Expert feedback becomes reviewed test cases. Never alter rules automatically from a GPT suggestion. Reuse existing DOI reports and scientific analyses; do not ask GPT to reread unchanged sources. Crossref results still need periodic refresh when source status changes.

## Validation and limits

The current 15-record development set yields 9/10 relevant candidates and no accepted negative controls. The remaining relevant record is pending because its title does not establish battery storage and the cached metadata lacks an abstract. No independent performance claim is made. A larger, source-verified set can be built incrementally; GPT may propose labels, but references must come from retrieved records and labels need evidence. It is an evaluation set, not training data for this rule engine.

The held-out evaluation should include grid-context negative examples, not only chemistry and materials journals. Current term co-occurrence can still produce false positives. Retrieval omissions remain independent from screening quality. This PR does not implement automatic abstract enrichment, GPT scientific reading, notifications or automatic acceptance into the bibliography.

## Commands

```bash
python -m unittest discover -s tests -v
python scripts/validate_retrieval.py
python scripts/research.py --since 2026-09-01 --until 2026-10-13
```

The existing monthly workflow commits reports and the handoff file in its report PR. Pending records are retained in the audit and counted in Markdown; they are not added to the accepted bibliography or to reported DOI state. The previous negative controls remain validation artifacts only.
