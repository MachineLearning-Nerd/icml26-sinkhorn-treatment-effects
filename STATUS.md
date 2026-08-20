# Status — icml26-sinkhorn-treatment-effects

**Paper:** Sinkhorn Treatment Effects: A Causal Optimal Transport Measure
**Authors:** Medha Agarwal and Alex Luedtke
**Reference:** arXiv:2605.08485
**Collection anchor:** HdhEFfEsoz

## Result

**INCONCLUSIVE**

| Evidence unit | Result |
|---|---:|
| Finite deterministic diagnostics | 4/4 passed |
| Scoped evidence points | 10/12 supported |
| Paper-level claims independently verified | 0/6 |
| Complete paper reproduction | false |
| Publication allowed | false |

## Claim statuses

| Claim | Status |
|---|---|
| C1 finite definition and properties | FINITE_DEFINITION_PROXY |
| C2 first-order differentiability and EIF | NOT_REPRODUCED |
| C3 second-order differentiability and EIF | NOT_REPRODUCED |
| C4 null scaling | FINITE_NULL_SCALING_PROXY |
| C5 alternative normality | FINITE_ALTERNATIVE_NORMALITY_PROXY |
| C6 permutation calibration and power | FINITE_PERMUTATION_CALIBRATION_PROXY |

C2 and C3 have indirect consequence metadata only; it is not promoted to
theorem verification.

## Metadata-only checks

~~~bash
python3 -m py_compile repro/src/finalize_gate.py verify_final.py
python3 repro/src/finalize_gate.py
python3 verify_final.py
~~~

The standardization pass does not run repro/src/verify.py, the finite
simulation, or any author implementation. The missing one-step estimators,
EIFs, STEAgg grid, Gaussian protocol, PatchCamelyon experiments, and
runtime/memory study remain outside the audit.
