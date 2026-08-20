# Gate readiness — Sinkhorn treatment-effects audit

This repository is ready only for a conservative, documentation-level gate.

## Required conditions

- outputs/verdict.json contains C1 through C6 with the expected statuses.
- C1 and C4–C6 remain finite proxies; C2 and C3 remain NOT_REPRODUCED.
- Four of four finite diagnostics and zero of six paper claims are recorded.
- The scoped evidence manifest records 10/12 supported points.
- overall_status remains INCONCLUSIVE.
- full_paper_reproduction is false.
- current_score_claim is false and publication_allowed is false.
- verify_final.py passes locally and in a fresh clone.

publication_gate_passed means that the metadata and evidence boundary are
internally consistent. It does not mean that the paper's asymptotic claims or
experiments were reproduced.
