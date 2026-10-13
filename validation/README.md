# Historical retrieval and screening validation — 2026-10-13

## Protocol

Ten relevant journal articles covering OPF, load forecasting, DLR, BESS and grid-connected converter control were selected from publisher and author-institution records. Five off-topic records from the initial report provide negative controls. DOIs and journal-article identity were independently checked through Crossref. Relevance labels reflect titles and available source abstracts; this is not a full-text scientific appraisal. Bibliographic snapshots omit abstracts; the positive Crossref records did not contain abstracts.

Each positive was searched using the configured topic query in its historical publication year, with a 50-record cutoff. The monthly recency window was deliberately not applied to historical controls. Screening was tested independently on DOI metadata, before deduplication and the five-paper reporting limit. Search errors are reported separately from misses.

## Results

- Relevant records retrieved by bounded search: 2/10.
- API errors during search: 0.
- Relevant records retained by screening: 0/10.
- Off-topic records rejected: 5/5.

| Article | Journal | Expected topic | Found in search | Screening | Reason |
|---|---|---|---|---|---|
| [Deep Learning for Household Load Forecasting—A Novel Pooling Deep RNN](https://doi.org/10.1109/tsg.2017.2686012) | IEEE Transactions on Smart Grid | load-forecasting | No | Rejected | Exact publication date unavailable |
| [Hybrid Ensemble Deep Learning for Deterministic and Probabilistic Low-Voltage Load Forecasting](https://doi.org/10.1109/tpwrs.2019.2946701) | IEEE Transactions on Power Systems | load-forecasting | No | Rejected | Exact publication date unavailable |
| [Improving Load Forecasting Process for a Power Distribution Network Using Hybrid AI and Deep Learning Algorithms](https://doi.org/10.1109/access.2019.2923796) | IEEE Access | load-forecasting | No | Rejected | Journal outside configured scope |
| [Dynamic Line Rating Using Numerical Weather Predictions and Machine Learning: A Case Study](https://doi.org/10.1109/tpwrd.2016.2543818) | IEEE Transactions on Power Delivery | dynamic-line-rating | Yes | Rejected | Exact publication date unavailable |
| [DeepOPF: A Deep Neural Network Approach for Security-Constrained DC Optimal Power Flow](https://doi.org/10.1109/tpwrs.2020.3026379) | IEEE Transactions on Power Systems | optimal-power-flow | No | Rejected | Exact publication date unavailable |
| [Review of machine learning techniques for optimal power flow](https://doi.org/10.1016/j.apenergy.2025.125637) | Applied Energy | optimal-power-flow | Yes | Rejected | Exact publication date unavailable |
| [Energy management of a microgrid considering nonlinear losses in batteries through Deep Reinforcement Learning](https://doi.org/10.1016/j.apenergy.2024.123435) | Applied Energy | bess | No | Rejected | Exact publication date unavailable |
| [Deep reinforcement learning for energy management in a microgrid with flexible demand](https://doi.org/10.1016/j.segan.2020.100413) | Sustainable Energy, Grids and Networks | bess | No | Rejected | Journal outside configured scope |
| [Deep Reinforcement Learning Based Control of a Grid Connected Inverter With LCL-Filter for Renewable Solar Applications](https://doi.org/10.1109/access.2024.3364058) | IEEE Access | converter-control | No | Rejected | Journal outside configured scope |
| [Model-Free Deep Reinforcement Learning Control for Grid-Connected Packed U-Cell Multilevel Inverters](https://doi.org/10.1109/ojpel.2026.3684829) | IEEE Open Journal of Power Electronics | converter-control | No | Rejected | Journal outside configured scope |
| [Unveiling Hidden Patterns in Electrode‐Electrolyte Interphase Chemistry and Architecture Through Machine Learning‐Assisted Mass Spectrometry Analysis](https://doi.org/10.1002/smtd.71113) | Small Methods | Outside scope | Not tested (negative) | Rejected | Journal outside configured scope |
| [Orthogonally Constrained Operator Learning for Bias-Aware Digital Twins: A PBDW-DeepONet Framework](https://doi.org/10.1007/s10915-026-03482-7) | Journal of Scientific Computing | Outside scope | Not tested (negative) | Rejected | Journal outside configured scope |
| [The Development of Dynamic Constitutive Models for Inconel 690 Based on Isothermal True Stress-Strain Curves](https://doi.org/10.1007/s11665-026-15126-w) | Journal of Materials Engineering and Performance | Outside scope | Not tested (negative) | Rejected | Journal outside configured scope |
| [Bifurcation of periodic and antiperiodic solutions in non-autonomous potential-type delay systems](https://doi.org/10.1007/s11784-026-01348-x) | Journal of Fixed Point Theory and Applications | Outside scope | Not tested (negative) | Rejected | Journal outside configured scope |
| [Study on marketing dynamics on sales of electric vehicles and SWOT analysis](https://doi.org/10.1007/s12046-026-03412-1) | Sādhanā | Outside scope | Not tested (negative) | Rejected | Journal outside configured scope |

## Interpretation and next correction

The pipeline is not ready for unattended scientific selection. Rejecting the five earlier false positives does not compensate for losing relevant papers. Exact-date screening rejects legitimate year-only and month-only records. IEEE Access, IEEE Open Journal of Power Electronics and Sustainable Energy, Grids and Networks are outside the current journal list despite relevant applications in the controls. Crossref publication filters can use online-first dates that precede the issue-based published date used to select a benchmark year; this can exclude a control before ranking. This test therefore measures the configured query/year retrieval, not topic ranking alone. Query recall is bounded by the first 50 records; a miss is not evidence that Crossref lacks the article.

Next: model partial dates as intervals, accepting only dates demonstrably inside the reporting window and routing ambiguous dates to review; expand journal scope with explicit content checks; enrich sparse metadata from verified publisher sources; test on a separate held-out set before changing acceptance rules. BESS classification also needs energy-storage synonyms backed by application evidence. No fabricated dates or summaries should be introduced to force acceptance.

No production filters are changed by this validation PR. All known false negatives remain visible. This development sample is small and purposive; its fractions are not general recall or precision estimates. The benchmark does not validate full-text extraction, scientific claims, PR creation or notification delivery.

## Reproduction

```bash
python scripts/validate_retrieval.py
python scripts/validate_retrieval.py --live --output validation/new-live-results.json
```

Offline execution reproduces metadata screening. Live execution repeats the bounded searches; results can change with Crossref indexing. See fixtures.json for source URLs and results.json for individual dates, windows and errors. The report does not add historical control DOIs to production seen state.
