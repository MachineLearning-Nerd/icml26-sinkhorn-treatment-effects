# ICML 2026 — Sinkhorn Treatment Effects

Independent, clean-room evidence audit of **Sinkhorn Treatment Effects: A
Causal Optimal Transport Measure** by Medha Agarwal and Alex Luedtke.

- Repository: https://github.com/MachineLearning-Nerd/icml26-sinkhorn-treatment-effects
- Paper: https://arxiv.org/abs/2605.08485
- HTML paper: https://arxiv.org/html/2605.08485
- Version reference: arXiv source pinned by outputs/verdict.json
- Collection anchor: HdhEFfEsoz

This repository audits finite point-cloud and permutation behavior. It is not
the authors' implementation and does not reproduce the paper's functional
derivatives, debiased estimators, STEAgg procedure, or image experiments.

## Current result

**Overall status: INCONCLUSIVE**

| Boundary | Result |
|---|---:|
| Finite deterministic proxy diagnostics | 4/4 pass |
| Scoped evidence points | 10/12 supported |
| Paper-level claims independently verified | 0/6 |
| Complete paper reproduction | false |
| Current score claim | false |
| Publication allowed | false |

The four finite passes are C1 and C4–C6. C2 and C3 are explicitly
NOT_REPRODUCED. The old 5/6 VERIFIED wording counted indirect finite behavior
as theorem verification and is superseded by the claim-level record.

This documentation/attribution pass did not run repro/src/verify.py, SciPy,
or any author implementation. It preserved and audited the committed
outputs/verdict.json.

## What the paper does

The paper proposes a causal measure based on the entropic optimal-transport
divergence between counterfactual outcome distributions. It studies the
measure as a smooth transformation of counterfactual mean embeddings, derives
first- and second-order pathwise results, constructs debiased estimators, and
uses them for testing. It also introduces aggregation over a regularization
grid and reports Gaussian simulations and PatchCamelyon image experiments.

## Claim-to-evidence ledger

| ID | Paper statement | Evidence production path | Status | Boundary |
|---|---|---|---|---|
| C1 | Equation 1 defines a nonnegative, definite, symmetric Sinkhorn divergence with smoothing behavior | repro/src/core.py and repro/src/verify.py → outputs/verdict.json:C1 | FINITE_DEFINITION_PROXY | Finite point clouds do not establish the general divergence theorem or MMD limit |
| C2 | Lemma 3.1: first-order pathwise differentiability and EIF | repro/src/verify.py records absence and indirect consequence metadata | NOT_REPRODUCED | No derivative, EIF, nuisance, or one-step implementation |
| C3 | Theorem 3.2: second-order pathwise differentiability under the null | repro/src/verify.py records absence and indirect consequence metadata | NOT_REPRODUCED | No second-order derivative, EIF, or debiased null estimator |
| C4 | Theorem 4.1: degenerate weighted-chi-square null behavior | repro/src/core.py and repro/src/verify.py → outputs/verdict.json:C4 | FINITE_NULL_SCALING_PROXY | Raw empirical STE at three finite sample sizes is not the paper estimator |
| C5 | Equation 12: square-root-n consistency and asymptotic normality under the alternative | repro/src/core.py and repro/src/verify.py → outputs/verdict.json:C5 | FINITE_ALTERNATIVE_NORMALITY_PROXY | Raw two-sample STE lacks nuisance estimation, EIF, and sample splitting |
| C6 | Section 4.4: permutation/STEAgg test controls type-I error and has power | repro/src/core.py and repro/src/verify.py → outputs/verdict.json:C6 | FINITE_PERMUTATION_CALIBRATION_PROXY | Small raw-statistic permutation test, not debiased STE or STEAgg |

Every paper claim remains paper_claim_verified: false. A finite proxy pass
means only that its local finite condition was observed.

## How each claim is produced

~~~text
finite point clouds and permutation setup
  -> repro/src/core.py
       entropic OT, Sinkhorn divergence, MMD, and finite STE statistic
  -> repro/src/verify.py
       C1 and C4-C6 finite diagnostics
       C2-C3 NOT_REPRODUCED records
  -> outputs/verdict.json
       six-claim evidence record and limitations
  -> repro/src/finalize_gate.py
       metadata-only status, count, and evidence-manifest validation
  -> outputs/gate.json and publication_gate.json
       conservative documentation gate; publication_allowed=false
  -> verify_final.py
       repository, branch, identity, file, and gate consistency checks
~~~

The standardization workflow did not invoke repro/src/verify.py. The existing
finite records are bounded historical evidence and are not silently upgraded
to asymptotic results.

## Repository map

- repro/src/core.py — finite entropic OT and Sinkhorn calculations.
- repro/src/verify.py — bounded finite diagnostics and claim records.
- docs/paper.txt and docs/paper.html — pinned paper snapshot.
- outputs/verdict.json — authoritative six-claim verdict.
- outputs/gate.json — generated structural gate result.
- publication_gate.json — root-level gate summary.
- CLAIM_EVIDENCE.md — claim-to-evidence contract.
- SOURCE_AUDIT.md — source and recovery boundary.
- ENVIRONMENT.md — execution and dependency boundary.
- EVIDENCE_MANIFEST.json — scoped evidence inventory.
- claims.json and reproduction_verdicts.json — machine-readable summaries.
- REPORT.md — standardized audit report.
- verify_final.py — dependency-light final-state verifier.

## Branch and attribution policy

The canonical repository is icml26-sinkhorn-treatment-effects and the
canonical branch is main; it is the sole published branch. The former
repository name was icml26-repro-HdhEFfEsoz-sinkhorn-treatment-effects. The
old master branch is documented in BRANCH_AUDIT.md and was removed after main
was published.

Reachable commits are normalized to:

~~~text
MachineLearning-Nerd <MachineLearning-Nerd@users.noreply.github.com>
~~~

## Citation

~~~bibtex
@article{agarwal2026sinkhorn,
  title = {Sinkhorn Treatment Effects: A Causal Optimal Transport Measure},
  author = {Agarwal, Medha and Luedtke, Alex},
  journal = {arXiv preprint arXiv:2605.08485},
  year = {2026},
  doi = {10.48550/arXiv.2605.08485}
}
~~~

The machine-readable citation is in CITATION.cff.

## Thank you

Thank you to Medha Agarwal and Alex Luedtke for developing and sharing this
connection between causal inference and entropic optimal transport. This
repository is an independent educational evidence audit, not an official
implementation or endorsement by the authors. The explicit C2/C3 boundary is
kept so finite observations are not mistaken for functional-analytic proofs.
