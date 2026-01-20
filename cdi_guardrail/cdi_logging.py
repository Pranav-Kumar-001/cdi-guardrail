# cdi_guardrail/logging.py

import time


class CDILogger:
    """
    Lightweight metrics logger for CDI Guardrail.

    Emits structured metrics suitable for:
    - Prometheus
    - OpenTelemetry
    - JSON logs
    """

    def __init__(self, service_name: str = "cdi_guardrail"):
        self.service_name = service_name

    def log_prediction(
        self,
        cdi_value: float,
        decision: str,
        latency_ms: float | None = None,
    ):
        """
        Log per-prediction metrics.
        """
        record = {
            "service": self.service_name,
            "event": "prediction",
            "timestamp": time.time(),
            "cdi": float(cdi_value),
            "decision": decision,
        }

        if latency_ms is not None:
            record["latency_ms"] = float(latency_ms)

        self.emit(record)

    def log_monitor_summary(self, summary: dict):
        """
        Log rolling CDI distribution stats.
        """
        record = {
            "service": self.service_name,
            "event": "cdi_summary",
            "timestamp": time.time(),
            **summary,
        }
        self.emit(record)

    def log_drift(self, ks_result: dict, psi_value: float):
        """
        Log drift detection result.
        """
        record = {
            "service": self.service_name,
            "event": "cdi_drift",
            "timestamp": time.time(),
            "ks_statistic": ks_result["statistic"],
            "ks_p_value": ks_result["p_value"],
            "ks_drift": ks_result["drift"],
            "psi": float(psi_value),
        }
        self.emit(record)

    def emit(self, record: dict):
        """
        Default emitter: stdout.
        Replace this with Prometheus / OTEL exporter.
        """
        print(record)
