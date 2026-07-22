"""Clean-room Sinkhorn Treatment Effects (arXiv 2605.08485, OpenReview HdhEFfEsoz).

The Sinkhorn Treatment Effect is the Sinkhorn divergence between the two counterfactual
outcome distributions P1 (treated) and P0 (control):

    STE(P) = OT_eps(P1, P0) - 1/2 OT_eps(P1, P1) - 1/2 OT_eps(P0, P0)   (Eq 1)

where OT_eps is the entropy-regularized OT cost with quadratic cost c(x,y) = 1/2 ||x-y||^2.
The centered form (Feydy et al. 2019) makes STE a proper divergence: STE >= 0 with equality
iff P1 = P0.  It interpolates unregularized OT (eps -> 0) and MMD with the Gibbs kernel
(exp(-c/eps))  (eps -> infinity).
"""
from __future__ import annotations
import numpy as np
from scipy.special import logsumexp as _logsumexp


def cost_matrix(X, Y):
    """c(x,y) = 1/2 ||x - y||^2  for row point sets X, Y."""
    X = np.atleast_2d(X); Y = np.atleast_2d(Y)
    return 0.5 * (np.sum(X**2, axis=1)[:, None] + np.sum(Y**2, axis=1)[None, :]
                  - 2 * X @ Y.T)


def entropic_ot(C, eps, n_iter=60):
    """Sinkhorn entropic OT cost <pi*, c> for precomputed cost matrix C, regularization eps.
    Direct (kernel) Sinkhorn iterations: K = exp(-C/eps), scaling vectors u,v.  Uniform marginals."""
    n, m = C.shape
    K = np.exp(-C / eps)
    u = np.ones(n) / n
    for _ in range(n_iter):
        v = 1.0 / (K.T @ u * m)
        u = 1.0 / (K @ v * n)
    pi = u[:, None] * K * v[None, :]
    return float(np.sum(pi * C))


def sinkhorn_divergence(X, Y, eps, n_iter=80):
    """S(P_X, P_Y) = OT_eps(X,Y) - 0.5 OT_eps(X,X) - 0.5 OT_eps(Y,Y).  (Feydy et al. 2019)"""
    Cxy = cost_matrix(X, Y); Cxx = cost_matrix(X, X); Cyy = cost_matrix(Y, Y)
    return entropic_ot(Cxy, eps, n_iter) - 0.5 * entropic_ot(Cxx, eps, n_iter) \
        - 0.5 * entropic_ot(Cyy, eps, n_iter)


def ste(P1, P0, eps, n_iter=80):
    """Sinkhorn Treatment Effect = Sinkhorn divergence between P1 (treated) and P0 (control)."""
    return sinkhorn_divergence(P1, P0, eps, n_iter)


def gibbs_kernel_mmd(X, Y, eps):
    """MMD with the Gibbs kernel exp(-c/eps) = exp(-||x-y||^2/(2 eps)).
    The eps->infty limit of the Sinkhorn divergence (up to the standard MMD centering)."""
    Kxx = np.mean(np.exp(-cost_matrix(X, X) / eps))
    Kyy = np.mean(np.exp(-cost_matrix(Y, Y) / eps))
    Kxy = np.mean(np.exp(-cost_matrix(X, Y) / eps))
    return Kxx + Kyy - 2 * Kxy


# --------------------------------------------------------------------------- #
#  C4 : degenerate-null distribution of the plug-in STE statistic
# --------------------------------------------------------------------------- #
def ste_null_spectrum(P_null, eps, n_iter=200):
    """Under the null P1=P0=P_null, the (scaled) Sinkhorn-divergence V-statistic has the
    degenerate form  T = sum_i lambda_i (chi^2_1 - 1),  where lambda_i are the eigenvalues of
    the centered Gibbs-kernel Gram operator.  Returns the spectrum (eigenvalues)."""
    X = np.atleast_2d(P_null)
    n = X.shape[0]
    K = np.exp(-cost_matrix(X, X) / eps)        # Gibbs kernel
    H = np.eye(n) - np.ones((n, n)) / n          # centering
    Kc = H @ K @ H                                # centered kernel
    eig = np.linalg.eigvalsh(Kc) / n             # lambda_i (population-ish)
    return np.sort(eig)[::-1]


def weighted_chi2_samples(lambdas, n_mc, rng):
    """Draw samples from sum_i lambda_i (chi^2_1 - 1)."""
    z = rng.standard_normal(size=(n_mc, len(lambdas)))
    chi2 = z**2                                    # chi^2_1 samples
    return chi2 @ lambdas - lambdas.sum()
