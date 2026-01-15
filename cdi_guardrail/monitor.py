# cdi_guardrail/monitor.py

import collections
import numpy as np


class CDIMonitor:
    """
    Rolling monitor for CDI values.
    """

    def __init__(self, window_size: int = 1000):
        self.window_size = window_size
        self.buffer = collections.deque(maxlen=window_size)

    def update(self, cdi_value: float):
        self.buffer.append(float(cdi_value))

    def summary(self):
        if len(self.buffer) == 0:
            return {}

        arr = np.asarray(self.buffer)

        return {
            "count": len(arr),
            "mean": float(arr.mean()),
            "std": float(arr.std()),
            "p50": float(np.percentile(arr, 50)),
            "p90": float(np.percentile(arr, 90)),
            "p95": float(np.percentile(arr, 95)),
            "p99": float(np.percentile(arr, 99)),
        }
