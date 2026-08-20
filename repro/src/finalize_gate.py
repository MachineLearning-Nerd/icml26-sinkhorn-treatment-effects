"""Validate and publish the conservative evidence gate."""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
VERDICT_PATH = ROOT / "outputs" / "verdict.json"
OUTPUT_GATE_PATH = ROOT / "outputs" / "gate.json"
PUBLICATION_GATE_PATH = ROOT / "publication_gate.json"
MANIFEST_PATH = ROOT / "EVIDENCE_MANIFEST.json"

EXPECTED_STATUSES = {
    "C1": "FINITE_DEFINITION_PROXY",
    "C2": "NOT_REPRODUCED",
    "C3": "NOT_REPRODUCED",
    "C4": "FINITE_NULL_SCALING_PROXY",
    "C5": "FINITE_ALTERNATIVE_NORMALITY_PROXY",
    "C6": "FINITE_PERMUTATION_CALIBRATION_PROXY",
}


def main() -> int:
    verdict = json.loads(VERDICT_PATH.read_text())
    manifest = json.loads(MANIFEST_PATH.read_text())
    claims = verdict.get("claims", {})
    errors: list[str] = []

    if set(claims) != set(EXPECTED_STATUSES):
        errors.append("verdict must contain exactly C1 through C6")
    statuses_ok = all(
        claims.get(name, {}).get("status") == status
        for name, status in EXPECTED_STATUSES.items()
    )
    if not statuses_ok:
        errors.append("claim statuses do not match the conservative policy")
    finite_count = sum(
        bool(claim.get("finite_proxy_passed")) for claim in claims.values()
    )
    if finite_count != 4 or verdict.get("finite_proxy_diagnostics_passed") != 4:
        errors.append("finite diagnostic count must be 4")
    if verdict.get("finite_proxy_diagnostics_total") != 4:
        errors.append("finite diagnostic total must be 4")
    if verdict.get("paper_claims_verified") != 0:
        errors.append("paper claim count must be 0")
    if verdict.get("paper_claims_total") != 6:
        errors.append("paper claim total must be 6")
    if verdict.get("overall_status") != "INCONCLUSIVE":
        errors.append("overall status must be INCONCLUSIVE")
    if verdict.get("full_paper_reproduction") is not False:
        errors.append("full_paper_reproduction must be false")
    if any(claim.get("paper_claim_verified") for claim in claims.values()):
        errors.append("no paper claim may be marked verified")
    if manifest.get("evidence_points_supported") != 10:
        errors.append("supported evidence-point count must be 10")
    if manifest.get("evidence_points_total") != 12:
        errors.append("evidence-point total must be 12")

    checks = {
        "six_claims_present": set(claims) == set(EXPECTED_STATUSES),
        "conservative_statuses": statuses_ok,
        "finite_proxy_count_is_four": finite_count == 4,
        "paper_claim_count_is_zero": verdict.get("paper_claims_verified") == 0,
        "overall_status_is_inconclusive": verdict.get("overall_status")
        == "INCONCLUSIVE",
        "full_reproduction_is_false": verdict.get("full_paper_reproduction")
        is False,
        "no_paper_claim_overclaim": not any(
            claim.get("paper_claim_verified") for claim in claims.values()
        ),
        "evidence_point_count": (
            manifest.get("evidence_points_supported") == 10
            and manifest.get("evidence_points_total") == 12
        ),
    }
    passed = not errors and all(checks.values())
    gate = {
        "paper": verdict.get("paper"),
        "title": verdict.get("title"),
        "authors": verdict.get("authors"),
        "arxiv": verdict.get("arxiv"),
        "slug": "icml26-sinkhorn-treatment-effects",
        "gate_date": date.today().isoformat(),
        "status": "PASS" if passed else "FAIL",
        "scope": verdict.get("scope"),
        "overall_status": verdict.get("overall_status"),
        "finite_proxy_diagnostics_passed": finite_count,
        "finite_proxy_diagnostics_total": 4,
        "paper_claims_verified": verdict.get("paper_claims_verified"),
        "paper_claims_total": verdict.get("paper_claims_total"),
        "evidence_points_supported": manifest["evidence_points_supported"],
        "evidence_points_total": manifest["evidence_points_total"],
        "full_paper_reproduction": verdict.get("full_paper_reproduction"),
        "current_score_claim": False,
        "publication_allowed": False,
        "documentation_gate_passed": passed,
        "checks": checks,
        "authoritative_verdict": "outputs/verdict.json",
        "tests_passed": passed,
        "publication_gate_passed": passed,
        "errors": errors,
        "notes": [
            "PASS means the finite-proxy audit is internally consistent and honestly scoped.",
            "PASS does not mean the paper's asymptotic claims or experiments were reproduced.",
        ],
    }
    serialized = json.dumps(gate, indent=2) + "\n"
    OUTPUT_GATE_PATH.write_text(serialized)
    PUBLICATION_GATE_PATH.write_text(serialized)
    print(
        "Publication gate: "
        f"{'PASS' if passed else 'FAIL'}; finite proxies {finite_count}/4; "
        f"paper claims {verdict.get('paper_claims_verified')}/6; "
        "evidence points 10/12; overall INCONCLUSIVE"
    )
    for error in errors:
        print(f"- {error}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
