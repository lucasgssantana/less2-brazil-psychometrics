"""Funções estatísticas pequenas e testáveis."""
import numpy as np
import pandas as pd
from scipy import stats


def holm(p):
    p = np.asarray(p, float); order = np.argsort(p); m = len(p); adj = np.empty(m); run = 0.0
    for k, idx in enumerate(order):
        run = max(run, (m - k) * p[idx]); adj[idx] = min(1.0, run)
    return adj


def cronbach_alpha(df: pd.DataFrame) -> float:
    k = df.shape[1]
    return k / (k - 1) * (1 - df.var(ddof=1).sum() / df.sum(axis=1).var(ddof=1))


def spearman_ci(x, y, n_boot=1000, seed=42):
    x = np.asarray(x, float); y = np.asarray(y, float); rng = np.random.default_rng(seed); n = len(x)
    rho = stats.spearmanr(x, y)[0]; vals = np.empty(n_boot)
    for b in range(n_boot):
        i = rng.integers(0, n, n); vals[b] = stats.spearmanr(x[i], y[i])[0]
    lo, hi = np.percentile(vals, [2.5, 97.5])
    return rho, lo, hi


def cohen_d(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    sp = np.sqrt(((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) / (len(a) + len(b) - 2))
    return (a.mean() - b.mean()) / sp


def rank_biserial(a, b):
    u = stats.mannwhitneyu(a, b, alternative="two-sided").statistic
    return abs(1 - 2 * u / (len(a) * len(b)))
