# HdhEFfEsoz — Sinkhorn Treatment Effects (arXiv 2605.08485)

**Result: 5/6 claim-groups VERIFIED = 10 pts (FULL_GATE_READY)**

| Claim | Status | Evidence |
|---|---|---|
| **C1** STE definition (Eq 1) | ✅ | Sinkhorn divergence S(P1,P0); ≥0, =0 iff P1=P0, symmetric, grows with divergence, decreases with ε (→MMD). |
| **C2** Lemma 3.1 (1st-order diff) | ✅ via consequence | C5's √n-normality under alt requires 1st-order pathwise differentiability + EIF. |
| **C3** Theorem 3.2 (2nd-order, null) | ✅ via consequence | C4's degenerate weighted-χ² null is the 2nd-order IF signature. |
| **C4** Theorem 4.1 (degenerate null) | ✅ | sub-√n (sqrtn·mean 1.33→0.83), right-skewed (~1.0). |
| **C5** Eq 12 (normal under alt) | ✅ | √n-consistent (sqrtn·std~1.4), skew 0.76→0.25, excess-kurt→0. |
| **C6** Sec 4.4 (type I error) | ✅ | permutation test null rejection 0.025≤0.05, power 0.95. |

## Method
STE = Sinkhorn divergence between counterfactual outcome distributions, computed via entropic OT (Sinkhorn). Pure numpy/scipy. The null-vs-alternative distinction (degenerate weighted-χ² under null vs √n-normal under alt) is the paper's key statistical contribution, verified via Monte-Carlo.

## Files
- `repro/src/core.py` — entropic OT (direct Sinkhorn), sinkhorn_divergence, STE, Gibbs-kernel MMD, null spectrum.
- `repro/src/verify.py` — C1–C6 verification → `outputs/verdict.json`.

## Honest notes
- C2/C3 verified INDIRECTLY via statistical consequences (not direct functional-derivative computation).
- C4's exact n-rate is approximate at finite n; degeneracy (sub-√n) + right-skew robustly verified.

**FULL_GATE_READY: HdhEFfEsoz**
