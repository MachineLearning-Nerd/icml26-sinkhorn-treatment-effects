# Sinkhorn Treatment Effects audit report

## Executive result

The repository is internally documented and structurally gated, but the
paper is not fully reproduced. Four bounded finite diagnostics pass, while
none of the six paper-level claims is independently verified.

| Measure | Result |
|---|---:|
| Overall status | INCONCLUSIVE |
| Finite proxy diagnostics | 4/4 |
| Evidence points | 10/12 |
| Paper claims verified | 0/6 |
| Complete paper reproduction | false |
| Current score claim | false |
| Publication allowed | false |

## Scope

The audit covers finite point-cloud Sinkhorn-divergence properties, finite
null scaling, finite alternative behavior, and a small permutation
calibration proxy. It does not cover the paper's functional-analytic
derivations, debiased estimators, STEAgg aggregation, Gaussian simulations,
PatchCamelyon experiments, or resource measurements.

## Claim outcomes

- C1: FINITE_DEFINITION_PROXY
- C2: NOT_REPRODUCED
- C3: NOT_REPRODUCED
- C4: FINITE_NULL_SCALING_PROXY
- C5: FINITE_ALTERNATIVE_NORMALITY_PROXY
- C6: FINITE_PERMUTATION_CALIBRATION_PROXY

The exact production paths and limitations are in CLAIM_EVIDENCE.md. The
machine-readable source is outputs/verdict.json; the generated structural
decision is publication_gate.json.

## Interpretation

The four finite passes are useful local sanity checks. They do not establish
theorems, asymptotic limits, or the validity of the paper's causal estimator.
The conservative result is retained so users can see exactly what is and is
not supported.

## Repository state

The canonical repository is
MachineLearning-Nerd/icml26-sinkhorn-treatment-effects, with one published
branch named main. The branch and history transition are documented in
BRANCH_AUDIT.md.
