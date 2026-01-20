# cdi_guardrail/statistics.py

import numpy as np


def bootstrap_ci(
    values,
    confidence: float = 0.95,
    n_bootstrap: int = 1000,
    random_state: int | None = None,
):
    """
    Bootstrap confidence interval for CDI values.

    Parameters
    ----------
    values : array-like
        Sequence of CDI values.
    confidence : float
        Confidence level (e.g., 0.95).
    n_bootstrap : int
        Number of bootstrap samples.
    random_state : int | None
        Random seed for reproducibility.

    Returns
    -------
    dict
        {
          "mean": float,
          "lower": float,
          "upper": float,
          "confidence": float
        }
    """
    values = np.asarray(values)
    if values.size == 0:
        raise ValueError("Cannot compute CI on empty array")

    rng = np.random.default_rng(random_state)

    means = []
    n = values.size

    for _ in range(n_bootstrap):
        sample = rng.choice(values, size=n, replace=True)
        means.append(sample.mean())

    means = np.asarray(means)

    alpha = 1.0 - confidence
    lower = np.quantile(means, alpha / 2.0)
    upper = np.quantile(means, 1.0 - alpha / 2.0)

    return {
        "mean": float(values.mean()),
        "lower": float(lower),
        "upper": float(upper),
        "confidence": confidence,
    }


def zscore(
    value: float,
    reference_values,
):
    """
    Z-score of a CDI value relative to a reference distribution.

    Parameters
    ----------
    value : float
        Current CDI value.
    reference_values : array-like
        Baseline CDI distribution.

    Returns
    -------
    float
        Z-score (standard deviations from mean).
    """
    ref = np.asarray(reference_values)
    if ref.size < 2:
        raise ValueError("Reference distribution too small")

    mean = ref.mean()
    std = ref.std()

    if std == 0.0:
        return 0.0

    return float((value - mean) / std)
