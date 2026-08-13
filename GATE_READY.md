# Publication gate

This repository is publication-ready as an **honest finite-proxy audit**.
It is not marked as a full reproduction of the paper.

## Gate decision

- Overall status: INCONCLUSIVE
- Finite diagnostics: 4/4 pass
- Paper claims independently verified: 0/6
- Full paper reproduction: false
- Gate: PASS for the stated audit scope

The gate passes only when the canonical verdict contains all six claims with
the expected conservative statuses:

- C1 FINITE_DEFINITION_PROXY
- C2 NOT_REPRODUCED
- C3 NOT_REPRODUCED
- C4 FINITE_NULL_SCALING_PROXY
- C5 FINITE_ALTERNATIVE_NORMALITY_PROXY
- C6 FINITE_PERMUTATION_CALIBRATION_PROXY

Run:

~~~bash
python3 repro/src/finalize_gate.py
~~~

The script validates outputs/verdict.json and writes
outputs/gate.json and publication_gate.json. A passing gate means the
documentation, evidence labels, and publication metadata agree; it does not
turn finite proxies into theorem verification.
