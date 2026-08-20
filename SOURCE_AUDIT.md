# Source and version audit

## Paper identity

- Title: Sinkhorn Treatment Effects: A Causal Optimal Transport Measure
- Authors: Medha Agarwal; Alex Luedtke
- arXiv: 2605.08485
- Collection anchor: HdhEFfEsoz
- Paper snapshot: docs/paper.txt and docs/paper.html

## Repository source boundary

The repository contains a bounded finite Sinkhorn-divergence audit and its
historical verdict. repro/src/core.py contains the finite primitives and
repro/src/verify.py contains the original diagnostic producer. The
authoritative claim record is outputs/verdict.json.

The repository is not the authors' implementation. It does not contain the
paper's direct pathwise derivatives, efficient influence functions, one-step
or cross-fitted nuisance estimators, STEAgg procedure, Gaussian simulation
protocol, PatchCamelyon experiment, or runtime/memory campaign.

The standardization pass only added documentation, machine-readable metadata,
and consistency gates. It did not run the scientific verifier or create new
scientific evidence.

## Pre-edit recovery

The source tip before this documentation pass was
fc288de69d46378409257efe27ae46a8dc93bd0a.

The pre-edit recovery bundle is stored outside the repository at:

~~~text
/tmp/icml26-sinkhorn-treatment-before-history.wyzMQz/icml26-sinkhorn-treatment-before-history.bundle
~~~

Its SHA-256 is:

~~~text
7561fb8726d5600197dd1441902af50d441e13dd111ed0a432b66e877b0f1142
~~~

The former repository name was
icml26-repro-HdhEFfEsoz-sinkhorn-treatment-effects. The former branch
layout had master as the old default branch; the published canonical branch
is now main, and the old branch is not published.

## Attribution boundary

Reachable commits are normalized to:

~~~text
MachineLearning-Nerd <MachineLearning-Nerd@users.noreply.github.com>
~~~

This attribution identifies the collection-maintenance commits. It does not
claim authorship of the paper or of the original scientific ideas.
