# Power Systems AI Research

Phase A: reproducible candidate discovery and DOI validation for an expert-reviewed power-systems bibliography. Python 3.12+, standard library only; no paid API or LLM key required.

## Local usage

```bash
python -m unittest discover -s tests -v
python scripts/research.py --since 2026-09-01 --until 2026-10-12 --contact your-email@example.org
```

Supply your real email for Crossref's polite pool. Configure OPF/dispatch, load forecasting, DLR, BESS and converter control in `config/topics.json`. IEEE/Elsevier receive publisher ranking preference; other journals remain eligible. Queries are relevance searches, not strict Boolean filters. The default 20 records per topic and 30-day overlapping window are non-exhaustive.

Outputs: `reports/YYYY-MM-DD.md`, JSON provenance with source metadata, and `data/seen_dois.json`. At most five unique unseen candidates are reported. Matching DOI registration and journal-article metadata are verified; peer review, topical relevance, methods, results and significance require publisher/full-text review. Phase A explicitly leaves scientific claims unassessed. No references are preloaded; synthetic test fixtures never enter reports. API failures abort rather than generate a success-shaped partial report.

Commit report and deduplication state together. State tracks reported candidates, not all hits; remove a DOI in a reviewed PR to reconsider an excluded candidate. Missing/corrupt state fails. Same-date runs can replace that date's report; use a fresh output folder for ad hoc experiments.

## Workflow

PRs and feature/main pushes run offline tests and compile checks. Manual dispatch and Monday 09:00 Europe/Madrid runs generate a candidate report and open a weekly PR. Timezone scheduling handles DST; GitHub may delay execution. Schedules only activate after the workflow reaches the default branch. No auto-merge.

After reviewing this foundation PR, enable Actions and, if permitted by account policy, **Settings → Actions → General → Workflow permissions → Allow GitHub Actions to create and approve pull requests**. Manually run the workflow once to validate live API access. The report job uses scoped `GITHUB_TOKEN` write permissions; no PAT required. An existing weekly branch blocks another run to preserve unmerged work; finish its PR before retrying. Tests also run before report PR creation.

This schedule is independent from the ChatGPT task “Power Systems AI Research”. Phase A neither alters that task nor invokes ChatGPT or delivers Android notifications. GitHub PR notifications can be enabled separately. Phase B can add evidence-backed extraction, curated acceptance state and notification integration.

## Scientific acceptance

Verify publisher page, journal review policy, identity, publication status, corrections/retractions and full text. Record methods, objectives/constraints, datasets, leakage controls, baselines, quantitative results with units, feasibility and limitations, citing exact source pages/sections. Separate optimization from learning and simulation from field validation. Use IEEE numbered citations only after validating complete bibliographic fields.

Documentation: [Crossref REST API](https://github.com/Crossref/rest-api-doc), [Crossref filters](https://www.crossref.org/documentation/retrieve-metadata/rest-api/rest-api-filters/), [GitHub scheduled events](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows).

## Scope correction

The initial 2026-10-12 candidate report contained off-topic records and must not be accepted. See `docs/screening-review.md`. The corrected search ranks by relevance and requires configured journal scope, exact in-window publication date, and separate title/abstract evidence for grid context, AI method and assigned topics. The JSON report records screening decisions. Conservative screening can produce zero candidates; journal additions and sparse metadata require expert review. This is still metadata screening, not verified scientific synthesis.
