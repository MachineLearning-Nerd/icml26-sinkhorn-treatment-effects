# Sinkhorn Treatment Effects — audit status

Paper: Sinkhorn Treatment Effects: A Causal Optimal Transport Measure
Authors: Medha Agarwal and Alex Luedtke
Reference: arXiv:2605.08485

## Conservative result

**Overall: INCONCLUSIVE**

- Finite diagnostics passed: 4/4 (C1 and C4–C6).
- Paper-level claims independently verified: 0/6.
- Full paper reproduction: no.

The previous 5/6 VERIFIED label counted indirect finite behavior as
verification of functional-analytic theorems. It is superseded by the
claim-level record in outputs/verdict.json.

| Claim | Current status |
| --- | --- |
| C1 definition and finite properties | FINITE_DEFINITION_PROXY |
| C2 first-order differentiability and EIF | NOT_REPRODUCED |
| C3 second-order differentiability under the null | NOT_REPRODUCED |
| C4 null scaling behavior | FINITE_NULL_SCALING_PROXY |
| C5 alternative normality behavior | FINITE_ALTERNATIVE_NORMALITY_PROXY |
| C6 permutation calibration and power | FINITE_PERMUTATION_CALIBRATION_PROXY |

Run repro/src/verify.py for the bounded diagnostics and
repro/src/finalize_gate.py for the publication gate. The missing one-step
estimators, EIFs, STEAgg grid, and image experiments are documented in the
README and canonical verdict.
