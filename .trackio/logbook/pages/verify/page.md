# verify

## Current verification record

The canonical verifier is repro/src/verify.py. It records six claims:

- C1: finite definition proxy passed.
- C2: direct first-order differentiability and EIF not reproduced.
- C3: direct second-order differentiability and EIF not reproduced.
- C4: finite null-scaling proxy passed.
- C5: finite alternative-normality proxy passed.
- C6: finite permutation-calibration proxy passed.

The canonical result is:

~~~text
Overall status: INCONCLUSIVE
Finite diagnostics: 4/4
Paper claims independently verified: 0/6
Full paper reproduction: false
~~~

Run repro/src/finalize_gate.py after the verifier to validate the publication
record. The old embedded 5/6 VERIFIED run is historical and is not the
authoritative result.
