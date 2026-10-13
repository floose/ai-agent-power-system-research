# Retrieval correction after the historical benchmark

The PR #4 benchmark remains the baseline: 2/10 relevant controls retrieved, 0/10 retained, and 5/5 negative controls rejected.

This correction represents year-only and month-only dates as intervals. Records are retained only when the entire possible date interval lies within the report window. Boundary overlaps require manual review; no day is invented. A year-only record can pass a year-wide historical test but will remain unresolved in a narrow monthly report. Publication dates are not replaced by indexing dates.

IEEE Access, IEEE Open Journal of Power Electronics and Sustainable Energy, Grids and Networks join the journal scope; content checks still apply. Shorter topic-specific queries avoid over-constraining bibliographic searches with unrelated terms. BESS screening recognizes energy storage and batteries but still requires independent power-system and learning evidence. Energy management alone does not establish a battery application.

Offline development-set screening retains 9/10 relevant controls and rejects 5/5 negatives. The remaining flexible-demand microgrid paper lacks battery/storage evidence in its title and has no Crossref abstract; it requires verified source enrichment rather than automatic acceptance. These fractions are not held-out performance estimates. Full-text scientific acceptance remains separate.

Run `python scripts/validate_retrieval.py` to reproduce screening. Historical retrieval remains sensitive to online-first versus issue-year dates and the bounded search. A future revision must test date-aware retrieval and source enrichment on an independent set before unattended deployment. This change does not claim to complete scientific-agent validation.

Live historical search with the revised queries retrieved 8/10 controls, with no API errors, compared with 2/10 in the baseline. Final screening was evaluated separately on the same cached records and retained 9/10. Per-record outcomes are in retrieval-live-results.json. This remains development-set tuning, not independent validation.
