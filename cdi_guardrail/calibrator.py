# cdi_guardrail/calibrator.py

import torch
import numpy as np


class CDICalibrator:
    """
    Learns CDI thresholds from calibration data.
    """

    def __init__(
        self,
        warn_percentile: float = 0.85,
        reject_percentile: float = 0.95,
    ):
        assert 0 < warn_percentile < reject_percentile < 1
        self.warn_percentile = warn_percentile
        self.reject_percentile = reject_percentile

        self.warn_threshold = None
        self.reject_threshold = None

    def fit(self, cdi_scores):
        """
        Fit thresholds from CDI scores.

        Parameters
        ----------
        cdi_scores : list[float] or 1D np.ndarray
        """
        cdi_scores = np.asarray(cdi_scores)

        self.warn_threshold = float(
            np.quantile(cdi_scores, self.warn_percentile)
        )
        self.reject_threshold = float(
            np.quantile(cdi_scores, self.reject_percentile)
        )

        return self.warn_threshold, self.reject_threshold

    def summary(self):
        return {
            "warn_threshold": self.warn_threshold,
            "reject_threshold": self.reject_threshold,
            "warn_percentile": self.warn_percentile,
            "reject_percentile": self.reject_percentile,
        }
