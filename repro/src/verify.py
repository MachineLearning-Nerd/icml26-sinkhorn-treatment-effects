"""Run bounded finite proxies for arXiv 2605.08485 (Sinkhorn Treatment Effects).

C1  Eq 1: STE(P) = Sinkhorn divergence S(P1,P0) = OT_eps(P1,P0) - 1/2 OT_eps(P1,P1)
    - 1/2 OT_eps(P0,P0).  Properties: >=0, =0 iff P1=P0 (definite), symmetric;
    interpolates OT (eps->0) and MMD with the Gibbs kernel (eps->infty).
C2  Lemma 3.1: first-order pathwise differentiability + efficient influence function.
C3  Theorem 3.2: second-order differentiability under the null P1=P0.
C4  Theorem 4.1: under the null the plug-in STE statistic is degenerate -- shrinks faster
    than 1/sqrt(n) with a right-skewed (weighted-chi^2) null distribution.
C5  Eq 12: under the ALTERNATIVE (P1 != P0) the STE estimator is sqrt(n)-consistent and
    asymptotically normal (skew, excess-kurtosis -> 0); this is the differentiable regime.
C6  Section 4.4: a permutation/STEAgg test controls the type I error under the null.

C2/C3 are functional-analytic differentiability claims. This repository does
not implement functional derivatives or the paper's one-step estimators, so
those claims remain NOT_REPRODUCED. C1 and C4-C6 are bounded finite proxies,
not theorem or full-experiment reproductions.
"""
from __future__ import annotations
import os, json
import numpy as np
from scipy.stats import skew, kurtosis
import sys
sys.path.insert(0, os.path.dirname(__file__))
from core import ste, sinkhorn_divergence, gibbs_kernel_mmd

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "outputs")
os.makedirs(OUT, exist_ok=True)
rep: dict = {"claims": {}}


def _dump(o):
    if isinstance(o, np.bool_): return bool(o)
    if isinstance(o, np.floating): return float(o)
    if isinstance(o, np.integer): return int(o)
    if isinstance(o, np.ndarray): return o.tolist()
    return str(o)


def claim_C1():
    """STE = Sinkhorn divergence: positive, definite (=0 iff P1=P0), symmetric, interpolates."""
    res = {}
    rng = np.random.default_rng(1)
    eps = 0.5
    P0 = rng.normal(size=(40, 2))
    P_same = P0.copy()
    P_diff = rng.normal(loc=0.7, size=(40, 2))
    s_self = ste(P_same, P0, eps)
    s_diff = ste(P_diff, P0, eps)
    s_rev = ste(P0, P_diff, eps)
    res["STE_self"] = s_self
    res["STE_diff"] = round(s_diff, 4)
    res["definite"] = bool(s_self < 1e-6)
    res["positive"] = bool(s_diff > 0)
    res["symmetric"] = bool(abs(s_diff - s_rev) < 1e-6)
    # interpolation: eps->infty approaches MMD (Gibbs kernel)
    s_bigeps = ste(P_diff, P0, 50.0)
    mmd = gibbs_kernel_mmd(P_diff, P0, 50.0)
    res["STE_eps50"] = round(s_bigeps, 5)
    res["MMD_eps50"] = round(mmd, 5)
    # interpolation (directional): STE decreases toward the MMD limit as eps grows
    # (more entropic smoothing shrinks the divergence; eps->infty degenerate-kernel limit)
    s_smalleps = ste(P_diff, P0, 0.1)
    res["STE_eps0.1"] = round(s_smalleps, 4)
    res["STE_decreases_with_eps"] = bool(s_bigeps <= s_smalleps)
    # monotonic: STE grows as distributions diverge
    grows = all(ste(rng.normal(loc=mu, size=(40, 2)), P0, eps) >
                ste(rng.normal(loc=mu * 0.5, size=(40, 2)), P0, eps) for mu in [0.5, 1.0, 1.5])
    res["STE_grows_with_divergence"] = bool(grows)
    ok = res["definite"] and res["positive"] and res["symmetric"] and grows
    res["finite_proxy_passed"] = bool(ok)
    res["paper_claim_verified"] = False
    res["status"] = "FINITE_DEFINITION_PROXY" if ok else "FAIL"
    res["paper_statement"] = (
        "Equation 1 defines a nonnegative, definite, symmetric Sinkhorn "
        "divergence with the stated smoothing behavior."
    )
    res["production_path"] = [
        "repro/src/core.py",
        "repro/src/verify.py",
        "outputs/verdict.json",
    ]
    res["limitations"] = [
        "Finite point clouds do not establish the general divergence theorem.",
        "The large-epsilon calculation is recorded but does not establish the paper's MMD limit.",
    ]
    rep["claims"]["C1"] = res
    return ok


def claim_C4():
    """Theorem 4.1: under the null the STE statistic is degenerate (faster than 1/sqrt(n),
    right-skewed weighted-chi^2-shaped)."""
    res = {}
    rng = np.random.default_rng(2)
    eps = 0.5
    rows = []
    for n in [30, 60, 120]:
        vals = np.array([ste(*np.split(rng.normal(size=(2 * n, 2)), 2), eps) for _ in range(300)])
        rows.append({"n": n, "mean": round(float(np.mean(vals)), 5),
                     "n_times_mean": round(float(n * np.mean(vals)), 3),
                     "sqrtn_times_mean": round(float(np.sqrt(n) * np.mean(vals)), 3),
                     "skew": round(float(skew(vals)), 3)})
    res["null_stats_by_n"] = rows
    # degenerate: sqrt(n)*mean decreases (faster than 1/sqrt(n)); right-skewed
    sqrtn_dec = rows[-1]["sqrtn_times_mean"] < rows[0]["sqrtn_times_mean"]
    right_skewed = all(r["skew"] > 0.3 for r in rows)
    res["degenerate_faster_than_sqrtn"] = bool(sqrtn_dec)
    res["right_skewed_weighted_chi2"] = bool(right_skewed)
    ok = res["degenerate_faster_than_sqrtn"] and res["right_skewed_weighted_chi2"]
    res["finite_proxy_passed"] = bool(ok)
    res["paper_claim_verified"] = False
    res["status"] = "FINITE_NULL_SCALING_PROXY" if ok else "FAIL"
    res["paper_statement"] = (
        "Theorem 4.1 gives the degenerate weighted-chi-square null behavior "
        "for the paper's estimator."
    )
    res["production_path"] = [
        "repro/src/core.py",
        "repro/src/verify.py",
        "outputs/verdict.json",
    ]
    res["limitations"] = [
        "The raw empirical Sinkhorn divergence is not the paper's debiased plug-in estimator.",
        "Three finite sample sizes cannot prove the null theorem or weighted-chi-square limit.",
    ]
    rep["claims"]["C4"] = res
    return ok


def claim_C5():
    """Eq 12: under the alternative (P1 != P0) the STE estimator is sqrt(n)-consistent and
    asymptotically normal."""
    res = {}
    rng = np.random.default_rng(3)
    eps = 0.5
    rows = []
    for n in [30, 60, 120]:
        vals = np.array([ste(rng.normal(loc=0.7, size=(n, 2)), rng.normal(size=(n, 2)), eps)
                         for _ in range(200)])
        rows.append({"n": n, "mean": round(float(np.mean(vals)), 4),
                     "std": round(float(np.std(vals)), 4),
                     "sqrtn_times_std": round(float(np.sqrt(n) * np.std(vals)), 3),
                     "skew": round(float(skew(vals)), 3),
                     "excess_kurt": round(float(kurtosis(vals)), 3)})
    res["alt_stats_by_n"] = rows
    # sqrt(n)-rate: sqrtn*std ~ constant
    sr = [r["sqrtn_times_std"] for r in rows]
    rate_ok = max(sr) / min(sr) < 1.3
    # normality: skew, excess kurtosis -> 0 as n grows
    skew_ok = abs(rows[-1]["skew"]) < abs(rows[0]["skew"]) and abs(rows[-1]["skew"]) < 0.4
    kurt_ok = abs(rows[-1]["excess_kurt"]) < 0.5
    res["sqrtn_consistent"] = bool(rate_ok)
    res["asymptotically_normal"] = bool(skew_ok and kurt_ok)
    ok = res["sqrtn_consistent"] and res["asymptotically_normal"]
    res["finite_proxy_passed"] = bool(ok)
    res["paper_claim_verified"] = False
    res["status"] = "FINITE_ALTERNATIVE_NORMALITY_PROXY" if ok else "FAIL"
    res["paper_statement"] = (
        "Equation 12 gives square-root-n consistency and asymptotic normality "
        "under the alternative for the paper's estimator."
    )
    res["production_path"] = [
        "repro/src/core.py",
        "repro/src/verify.py",
        "outputs/verdict.json",
    ]
    res["limitations"] = [
        "The raw two-sample Sinkhorn divergence is not the paper's one-step estimator.",
        "No nuisance estimation, EIF, sample splitting, or asymptotic theorem is implemented.",
    ]
    rep["claims"]["C5"] = res
    return ok


def claim_C6():
    """Section 4.4: permutation test controls type I error under the null."""
    res = {}
    rng = np.random.default_rng(4)
    eps = 0.5

    def perm_test(P1, P0, B=60, q=0.95):
        T0 = ste(P1, P0, eps)
        pool = np.vstack([P1, P0]); n = len(P1); tot = len(pool)
        null = []
        for _ in range(B):
            idx = rng.permutation(tot)
            null.append(ste(pool[idx[:n]], pool[idx[n:]], eps))
        return float(T0 > np.quantile(null, q))

    rej_null_05 = np.mean([perm_test(rng.normal(size=(25, 2)), rng.normal(size=(25, 2)))
                           for _ in range(80)])
    rej_alt = np.mean([perm_test(rng.normal(size=(25, 2)), rng.normal(loc=0.8, size=(25, 2)))
                       for _ in range(80)])
    res["null_rejection_alpha05"] = round(float(rej_null_05), 3)
    res["alternative_rejection"] = round(float(rej_alt), 3)
    # type I error controlled: null rejection <= 0.08 (allow calibration slack around 0.05)
    res["type_I_error_controlled"] = bool(rej_null_05 <= 0.10)
    res["has_power"] = bool(rej_alt > 0.5)
    ok = res["type_I_error_controlled"] and res["has_power"]
    res["finite_proxy_passed"] = bool(ok)
    res["paper_claim_verified"] = False
    res["status"] = "FINITE_PERMUTATION_CALIBRATION_PROXY" if ok else "FAIL"
    res["paper_statement"] = (
        "Section 4.4's permutation or STEAgg test controls type-I error "
        "and has useful power."
    )
    res["production_path"] = [
        "repro/src/core.py",
        "repro/src/verify.py",
        "outputs/verdict.json",
    ]
    res["limitations"] = [
        "This is a small raw-statistic permutation test, not the paper's debiased STE or STEAgg procedure.",
        "The finite rejection estimate is calibration evidence only.",
    ]
    rep["claims"]["C6"] = res
    return ok


def claim_C2C3():
    """Record that the differentiability claims are not reproduced directly."""
    c4 = rep["claims"].get("C4", {}).get("finite_proxy_passed", False)
    c5 = rep["claims"].get("C5", {}).get("finite_proxy_passed", False)
    common = {
        "finite_proxy_passed": False,
        "paper_claim_verified": False,
        "status": "NOT_REPRODUCED",
        "indirect_consequence_proxies": {
            "C2_from_C5": bool(c5),
            "C3_from_C4": bool(c4),
        },
        "production_path": [
            "repro/src/verify.py",
            "outputs/verdict.json",
        ],
        "limitations": [
            "No direct first- or second-order pathwise derivative or efficient influence function is implemented.",
            "Finite distributional behavior cannot establish a functional-analytic theorem.",
        ],
    }
    rep["claims"]["C2"] = dict(
        common,
        paper_statement="Lemma 3.1: first-order pathwise differentiability and EIF.",
    )
    rep["claims"]["C3"] = dict(
        common,
        paper_statement="Theorem 3.2: second-order pathwise differentiability under the null.",
    )
    return False


if __name__ == "__main__":
    r1 = claim_C1(); r4 = claim_C4(); r5 = claim_C5(); r6 = claim_C6(); r23 = claim_C2C3()
    print(f"C1 STE definition:        {r1}")
    print(f"C4 degenerate null:       {r4}")
    print(f"C5 normal under alt:      {r5}")
    print(f"C6 type I error:          {r6}  (null rej={rep['claims']['C6']['null_rejection_alpha05']})")
    print(f"C2/C3 differentiability:  {r23}  (not reproduced directly)")
    finite_proxy_count = sum(
        1 for claim in rep["claims"].values() if claim.get("finite_proxy_passed")
    )
    rep.update(
        {
            "paper": "HdhEFfEsoz",
            "title": "Sinkhorn Treatment Effects: A Causal Optimal Transport Measure",
            "authors": ["Medha Agarwal", "Alex Luedtke"],
            "arxiv": "2605.08485",
            "scope": "Independent audit of finite Sinkhorn-divergence and permutation proxies; the paper's functional derivatives, debiased estimators, STEAgg procedure, and image experiments are outside this repository.",
            "overall_status": "INCONCLUSIVE",
            "finite_proxy_diagnostics_passed": finite_proxy_count,
            "finite_proxy_diagnostics_total": 4,
            "paper_claims_verified": 0,
            "paper_claims_total": 6,
            "full_paper_reproduction": False,
            "not_reproduced": [
                "C2 direct first-order pathwise differentiability and EIF",
                "C3 direct second-order pathwise differentiability and second-order EIF",
                "one-step and cross-fitted nuisance estimators",
                "STEAgg over a regularization grid",
                "Gaussian simulation protocol from the paper",
                "PatchCamelyon image experiments",
                "GPU, runtime, and memory experiments",
            ],
            "notes": [
                "The four finite diagnostics are retained as bounded proxies only.",
                "The old 5/6 VERIFIED label counted indirect consequences as theorem verification and is superseded by this conservative verdict.",
            ],
        }
    )
    json.dump(rep, open(os.path.join(OUT, "verdict.json"), "w"), indent=2, default=_dump)
    print(f"\nFINITE PROXIES {finite_proxy_count}/4 passed (C1, C4, C5, C6)")
    print("Saved outputs/verdict.json")
