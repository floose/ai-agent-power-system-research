# Scope audit of the initial candidate report

The 2026-10-12 report on research/2026-W42 must not be accepted as a power-systems bibliography. The previous implementation sorted fuzzy Crossref searches by publication date and assigned topics from query membership, without content screening. DOI validation did not correct this relevance defect.

| DOI | Journal | Screening decision |
|---|---|---|
| 10.1002/smtd.71113 | Small Methods | Exclude: electrode/interphase chemistry is outside grid operation and control; no demonstrated OPF application. |
| 10.1007/s10915-026-03482-7 | Journal of Scientific Computing | Exclude from this report: generic operator learning/digital twins do not establish an electrical power-system application. |
| 10.1007/s11665-026-15126-w | Journal of Materials Engineering and Performance | Exclude: constitutive material modeling does not establish dynamic line rating. |
| 10.1007/s11784-026-01348-x | Journal of Fixed Point Theory and Applications | Exclude: delay-system analysis does not establish optimal dispatch or OPF. |
| 10.1007/s12046-026-03412-1 | Sādhanā | Exclude: vehicle marketing and sales are not electrical load forecasting. |

Decisions above use the titles and journals recorded in the initial report, not a claim of full-text review. The operator-learning paper may be reconsidered separately if source evidence establishes a relevant application. No connection should be inferred from generic terms such as learning, dynamics, energy or digital twin.

The corrected pipeline uses relevance-ranked search, a configurable journal scope, exact publication dates within the report window, and independent title/abstract evidence for power-system context, an AI method and each assigned topic. Query membership never assigns a topic. Screening decisions are preserved in the JSON audit. An empty report is preferable to irrelevant substitutions.

This conservative filter can miss relevant articles with sparse metadata or journals outside the configured scope. Such records require a documented expert review, not automatic acceptance. The journal list is a scope policy, not a journal-quality ranking or proof of peer review. Conventional optimization without AI/learning evidence is excluded from this AI digest; foundational optimization papers require a separate curated track.
