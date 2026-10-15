# Scientific reading pilot — 2026-10-14

This historical pilot tests evidence-backed reading, not monthly discovery. The entries below are proposed review notes, not accepted bibliography entries. No GPT API workflow is activated, and no production DOI state is changed.

## Engineering review

| Paper | Application | Source coverage | Review state |
|---|---|---|---|
| DeepOPF [1] | Preventive security-constrained DC dispatch | arXiv v3 full text | Awaiting expert review and published-version reconciliation |
| Augmented RL dispatch [2] | Microgrid BESS dispatch | arXiv v2 full text | Awaiting expert review and published-version reconciliation |
| Packed-U-cell inverter [3] | Grid-connected converter control | Author-institution abstract only | Incomplete scientific reading |

## 1. Learning a feasible dispatch mapping

Pan et al. [1] learn generator outputs from load inputs, reconstruct voltage angles through DC power-flow equations, and apply an l1 projection when predictions violate feasibility. The contribution is a physics-structured surrogate for repeated preventive SC-DCOPF, rather than an unconstrained prediction of operating points. Table II reports 100% feasible solutions for the IEEE 118-bus case, optimality loss below 0.2%, and a 281-fold speedup against Gurobi under the tested typical conditions. These results concern numerical test systems and a DC formulation; they do not establish AC voltage/reactive-power feasibility or deployment performance. For this review, the study illustrates why computational acceleration must be assessed jointly with constraint satisfaction.

**Evidence:** [arXiv:1910.14448v3 full text](https://arxiv.org/html/1910.14448v3), Sec. III, Sec. IV-D and IV-F, Sec. VI-A–B, Table II. The journal record is verified separately by DOI. Performance values are attributed to the consulted author version; equivalence with the version of record has not been established.

## 2. Combining reinforcement learning with dispatch knowledge

Shang et al. [2] formulate stochastic BESS dispatch with a nonlinear degradation cost and augment approximate Q-learning with multistep Monte Carlo tree search and dispatch rules. The rules restrict exploration using state-of-charge and point-of-common-coupling requirements. In the 72-hour comparison of Table 2, the proposed method yields normalized electricity revenue of 1.05, degradation cost of 0.92 and PCC deviation metric of 0.79, relative to Algorithm 2 at 1.00. Algorithm 2 incorporates knowledge but uses one-stage bootstrapping; the comparison is not against a global stochastic optimum. The study is relevant to interpretable, operationally constrained learning for storage. Transfer to other tariffs, degradation models and network constraints requires additional validation.

**Evidence:** [arXiv:1910.04541v2 PDF](https://arxiv.org/pdf/1910.04541v2), Sec. II–III, Sec. IV-A, Figs. 5–8 and Table 2, printed p. 8. The consulted version supplies source evidence; author listings differ between arXiv metadata and the publisher DOI record and require reconciliation before final citation acceptance.

## 3. Learning switching control for a grid-connected inverter

The institutional abstract for Alquennah et al. [3] describes an actor–critic controller trained using proximal policy optimization for a grid-connected five-level packed-U-cell inverter. It regulates grid current and floating-capacitor voltage and supports active/reactive exchanges. The abstract reports a real-time implementation and laboratory-prototype evaluation. This is pertinent to converter control, but the abstract does not establish numerical performance, operating envelopes or comparative robustness. Quantitative claims are therefore withheld.

**Evidence:** [TU Delft author-institution record](https://research.tudelft.nl/en/publications/model-free-deep-reinforcement-learning-control-for-grid-connected/), Abstract, paragraphs 1–4. Full-text scientific reading is pending. The institution and Crossref author lists are not identical; use the publisher record to resolve authorship before acceptance.

## Preliminary synthesis

These three examples suggest an organizing axis for the review: **where physical knowledge enters the learning pipeline**. It may enter through algebraic reconstruction and feasibility restoration [1], dispatch-rule constraints [2], or the control environment and reward design [3]. This is an editorial interpretation of a small purposive pilot, not a demonstrated literature-wide trend.

## References

Bibliographic title, DOI, journal, volume and pagination were checked against Crossref on 2026-10-14. Publisher corrections/retractions and complete source-version agreement remain to be checked before acceptance.

[1] X. Pan, T. Zhao, M. Chen, and S. Zhang, “DeepOPF: A Deep Neural Network Approach for Security-Constrained DC Optimal Power Flow,” *IEEE Transactions on Power Systems*, vol. 36, no. 3, pp. 1725–1735, May 2021, doi: [10.1109/TPWRS.2020.3026379](https://doi.org/10.1109/TPWRS.2020.3026379).

[2] Y. Shang et al., “Stochastic dispatch of energy storage in microgrids: An augmented reinforcement learning approach,” *Applied Energy*, vol. 261, Art. no. 114423, Mar. 2020, doi: [10.1016/j.apenergy.2019.114423](https://doi.org/10.1016/j.apenergy.2019.114423).

[3] A. N. Alquennah et al., “Model-Free Deep Reinforcement Learning Control for Grid-Connected Packed U-Cell Multilevel Inverters,” *IEEE Open Journal of Power Electronics*, vol. 7, pp. 1360–1376, 2026, doi: [10.1109/OJPEL.2026.3684829](https://doi.org/10.1109/OJPEL.2026.3684829).

## Next gate

Review the electrical application and evidence for each entry. Reconcile published versions and authorship, complete the third full-text reading, and validate triage on independent articles. Only then consider a recurring reading workflow. This pilot does not establish general retrieval quality or autonomous scientific acceptance.
