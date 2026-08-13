# Branch and attribution audit

## Historical state

Before normalization, the repository was:

- Name: icml26-repro-HdhEFfEsoz-sinkhorn-treatment-effects
- Remote: MachineLearning-Nerd/icml26-repro-HdhEFfEsoz-sinkhorn-treatment-effects
- Default branch: master
- Historical master tip: db5b7a0e1a8c2bb1eacb1f1f3bf261fa5840441a
- Branches observed: master only

The historical commit used DineshAI / dinesh@local and included a Claude
co-author trailer. That attribution is not retained in the normalized
published history.

## Canonical state

- Repository: MachineLearning-Nerd/icml26-sinkhorn-treatment-effects
- Canonical branch: main
- Legacy master branch: removed after main was published
- Expected branch count: one

All reachable published commits are normalized to:

~~~text
MachineLearning-Nerd
37579156+MachineLearning-Nerd@users.noreply.github.com
~~~

No Claude co-author trailer is permitted in the canonical history.

## Verification checklist

The final publication check must confirm:

1. GitHub metadata uses the canonical repository name and main as default.
2. The only remote branch is main.
3. The main tip contains README.md, STATUS.md, GATE_READY.md,
   BRANCH_AUDIT.md, the canonical verdict, and the publication gate.
4. Paginated commit attribution reports MachineLearning-Nerd for every
   reachable commit.
5. No reachable commit contains the old Claude co-author trailer.
