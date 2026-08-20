"""Verify the published repository's bounded-evidence documentation contract."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent
IDENTITY = "MachineLearning-Nerd"
EMAIL = "MachineLearning-Nerd@users.noreply.github.com"
EXPECTED = {
    "C1": "FINITE_DEFINITION_PROXY",
    "C2": "NOT_REPRODUCED",
    "C3": "NOT_REPRODUCED",
    "C4": "FINITE_NULL_SCALING_PROXY",
    "C5": "FINITE_ALTERNATIVE_NORMALITY_PROXY",
    "C6": "FINITE_PERMUTATION_CALIBRATION_PROXY",
}
REQUIRED_FILES = (
    "README.md",
    "STATUS.md",
    "BRANCH_AUDIT.md",
    "GATE_READY.md",
    "CLAIM_EVIDENCE.md",
    "SOURCE_AUDIT.md",
    "ENVIRONMENT.md",
    "REPORT.md",
    "AUTHOR_THANK_YOU.md",
    "CITATION.cff",
    "claims.json",
    "reproduction_verdicts.json",
    "AUTONOMOUS_STATE.json",
    "EVIDENCE_MANIFEST.json",
    "outputs/verdict.json",
    "outputs/gate.json",
    "publication_gate.json",
    "repro/src/finalize_gate.py",
)


def read_json(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def refs(scope: str) -> list[str]:
    return subprocess.check_output(
        [
            "git",
            "-C",
            str(ROOT),
            "for-each-ref",
            "--format=%(refname:short)",
            scope,
        ],
        text=True,
    ).splitlines()


def main() -> int:
    errors: list[str] = []
    for relative in REQUIRED_FILES:
        if not (ROOT / relative).is_file():
            errors.append(f"missing required file: {relative}")
    if errors:
        print("\n".join(errors))
        return 1

    verdict = read_json("outputs/verdict.json")
    gate = read_json("outputs/gate.json")
    publication_gate = read_json("publication_gate.json")
    claims = read_json("claims.json")
    verdicts = read_json("reproduction_verdicts.json")
    state = read_json("AUTONOMOUS_STATE.json")
    manifest = read_json("EVIDENCE_MANIFEST.json")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    if gate != publication_gate:
        errors.append("outputs/gate.json and publication_gate.json differ")
    for key, expected in (
        ("finite_proxy_diagnostics_passed", 4),
        ("finite_proxy_diagnostics_total", 4),
        ("paper_claims_verified", 0),
        ("paper_claims_total", 6),
        ("evidence_points_supported", 10),
        ("evidence_points_total", 12),
    ):
        if gate.get(key) != expected:
            errors.append(f"gate {key} is not {expected}")
    if gate.get("overall_status") != "INCONCLUSIVE":
        errors.append("gate overall status is not INCONCLUSIVE")
    if gate.get("full_paper_reproduction") is not False:
        errors.append("full_paper_reproduction is not false")
    if gate.get("current_score_claim") is not False:
        errors.append("current score claim is not false")
    if gate.get("publication_allowed") is not False:
        errors.append("publication_allowed is not false")
    if gate.get("tests_passed") is not True:
        errors.append("documentation gate did not pass")

    source_claims = verdict.get("claims", {})
    rows = {row.get("id"): row for row in claims.get("claims", [])}
    if set(source_claims) != set(EXPECTED):
        errors.append("outputs/verdict.json does not contain exactly C1-C6")
    if set(rows) != set(EXPECTED):
        errors.append("claims.json does not contain exactly C1-C6")
    for claim_id, status in EXPECTED.items():
        if source_claims.get(claim_id, {}).get("status") != status:
            errors.append(f"source status mismatch for {claim_id}")
        row = rows.get(claim_id, {})
        if row.get("source_key") != claim_id:
            errors.append(f"source key mismatch for {claim_id}")
        if row.get("status") != status:
            errors.append(f"claims.json status mismatch for {claim_id}")
        if row.get("paper_claim_verified") is not False:
            errors.append(f"{claim_id} is marked paper-verified")
        if source_claims.get(claim_id, {}).get("paper_claim_verified") is not False:
            errors.append(f"source {claim_id} is marked paper-verified")

    if verdicts.get("claims") != EXPECTED:
        errors.append("reproduction_verdicts.json statuses mismatch")
    if len(manifest.get("points", [])) != 12:
        errors.append("manifest does not contain 12 points")
    for key, expected in (
        ("evidence_points_supported", 10),
        ("evidence_points_total", 12),
    ):
        if manifest.get(key) != expected:
            errors.append(f"manifest {key} is not {expected}")
    if state.get("canonical_branch") != "main":
        errors.append("canonical branch is not main")
    if state.get("published_branch_count") != 1:
        errors.append("published branch count is not 1")
    if state.get("scientific_runner_executed_by_standardization_pass") is not False:
        errors.append("scientific runner execution flag is not false")
    if state.get("author_implementation_executed_by_standardization_pass") is not False:
        errors.append("author implementation execution flag is not false")

    for phrase in (
        "What the paper does",
        "Claim-to-evidence ledger",
        "How each claim is produced",
        "Branch and attribution policy",
        "Citation",
        "Thank you",
        "INCONCLUSIVE",
        "publication_allowed",
    ):
        if phrase not in readme:
            errors.append(f"README is missing phrase: {phrase}")

    heads = refs("refs/heads")
    remote_heads = [
        name.removeprefix("origin/")
        for name in refs("refs/remotes")
        if name.startswith("origin/") and not name.endswith("/HEAD")
    ]
    if heads != ["main"]:
        errors.append(f"local branches are not exactly main: {heads}")
    if remote_heads != ["main"]:
        errors.append(f"remote branches are not exactly origin/main: {remote_heads}")

    commits = subprocess.check_output(
        [
            "git",
            "-C",
            str(ROOT),
            "log",
            "--all",
            "--format=%H|%an|%ae|%cn|%ce",
        ],
        text=True,
    ).splitlines()
    for line in commits:
        _, author_name, author_email, committer_name, committer_email = line.split(
            "|", 4
        )
        if (author_name, author_email, committer_name, committer_email) != (
            IDENTITY,
            EMAIL,
            IDENTITY,
            EMAIL,
        ):
            errors.append(f"non-canonical commit identity: {line}")
            break

    if errors:
        print("FINAL_AUDIT=FAILED")
        print("\n".join(f"- {error}" for error in errors))
        return 1

    print(
        "FINAL_AUDIT=VERIFIED "
        "branches=1 "
        f"commits={len(commits)} "
        "claims=C1:finite,C2:not_reproduced,C3:not_reproduced,"
        "C4:finite,C5:finite,C6:finite "
        "finite_proxies=4/4 "
        "evidence_points=10/12 "
        "complete_paper_reproduction=false "
        "current_score_claim=false "
        "publication_allowed=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
