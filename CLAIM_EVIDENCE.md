# Claim-to-evidence contract

This file defines the boundary between the paper's statements and the
finite evidence already recorded in this repository. A FINITE_* status is
an observed finite diagnostic, not verification of a theorem or asymptotic
claim. Every paper_claim_verified field is false.

## Claim ledger

| ID | Paper statement | Producer and output | Status | What the result does not establish |
|---|---|---|---|---|
| C1 | Equation 1 defines a nonnegative, definite, symmetric Sinkhorn divergence with the stated smoothing behavior. | repro/src/core.py and repro/src/verify.py → outputs/verdict.json:claims.C1 | FINITE_DEFINITION_PROXY | General divergence properties or the MMD limit |
| C2 | Lemma 3.1 gives first-order pathwise differentiability and an efficient influence function. | repro/src/verify.py records the missing direct path → outputs/verdict.json:claims.C2 | NOT_REPRODUCED | A functional derivative, EIF, nuisance path, or one-step estimator |
| C3 | Theorem 3.2 gives second-order pathwise differentiability under the null. | repro/src/verify.py records the missing direct path → outputs/verdict.json:claims.C3 | NOT_REPRODUCED | A second-order derivative, second-order EIF, or debiased null estimator |
| C4 | Theorem 4.1 gives degenerate weighted-chi-square null behavior for the paper's estimator. | repro/src/core.py and repro/src/verify.py → outputs/verdict.json:claims.C4 | FINITE_NULL_SCALING_PROXY | The theorem or its limit law for the paper's debiased estimator |
| C5 | Equation 12 gives square-root-n consistency and asymptotic normality under the alternative for the paper's estimator. | repro/src/core.py and repro/src/verify.py → outputs/verdict.json:claims.C5 | FINITE_ALTERNATIVE_NORMALITY_PROXY | The paper's one-step estimator, EIF, nuisance estimation, or asymptotic normality |
| C6 | Section 4.4's permutation/STEAgg test controls type-I error and has useful power. | repro/src/core.py and repro/src/verify.py → outputs/verdict.json:claims.C6 | FINITE_PERMUTATION_CALIBRATION_PROXY | The debiased STE, STEAgg grid, or paper-scale testing procedure |

## Production path

~~~text
finite inputs
  -> repro/src/core.py
       entropic OT, Sinkhorn divergence, MMD, and finite test statistics
  -> repro/src/verify.py
       historical finite diagnostics and explicit missing-path records
  -> outputs/verdict.json
       authoritative six-claim evidence record
  -> repro/src/finalize_gate.py
       metadata-only count and consistency gate
  -> outputs/gate.json and publication_gate.json
       conservative publication decision
  -> verify_final.py
       repository, branch, identity, and documentation checks
~~~

The standardization pass did not execute repro/src/verify.py. The committed
finite records are retained as bounded historical evidence and are not
upgraded into paper-level claims.

## Evidence interpretation

- FINITE_* means the named local finite diagnostic passed its narrow condition.
- NOT_REPRODUCED means the repository does not contain a direct implementation
  and evidence path for that paper statement.
- paper_claim_verified: false is intentional for all six rows.
- The complete-paper result remains false because the direct pathwise,
  debiasing, aggregation, image, and paper-scale experiment paths are absent.
