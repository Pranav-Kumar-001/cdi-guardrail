# cdi_guardrail/policy.py

class CDIPolicy:
    """
    Threshold-based CDI policy.
    """

    def __init__(
        self,
        warn_threshold: float,
        reject_threshold: float
    ):
        assert 0 < warn_threshold < reject_threshold < 1
        self.warn_threshold = warn_threshold
        self.reject_threshold = reject_threshold

    def decide(self, cdi_value: float) -> str:
        if cdi_value >= self.reject_threshold:
            return "reject"
        elif cdi_value >= self.warn_threshold:
            return "warn"
        else:
            return "accept"
