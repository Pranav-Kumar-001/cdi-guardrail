# cdi_guardrail/drift.py

import numpy as np
from scipy.stats import ks_2samp


def ks_drift(reference, current, alpha: float = 0.05):
    """
    Kolmogorov–Smirnov test on CDI distributions.
    """
    reference = np.asarray(reference)
    current = np.asarray(current)

    stat, p_value = ks_2samp(reference, current)

    return {
        "statistic": float(stat),
        "p_value": float(p_value),
        "drift": bool(p_value < alpha),
    }


def population_stability_index(
    reference,
    current,
    n_bins: int = 10,
    eps: float = 1e-6,
):
    """
    Population Stability Index (PSI).
    """
    reference = np.asarray(reference)
    current = np.asarray(current)

    bins = np.linspace(0, 1, n_bins + 1)

    ref_hist, _ = np.histogram(reference, bins=bins)
    cur_hist, _ = np.histogram(current, bins=bins)

    ref_pct = ref_hist / max(ref_hist.sum(), eps)
    cur_pct = cur_hist / max(cur_hist.sum(), eps)

    psi = np.sum(
        (cur_pct - ref_pct)
        * np.log((cur_pct + eps) / (ref_pct + eps))
    )

    return float(psi)
