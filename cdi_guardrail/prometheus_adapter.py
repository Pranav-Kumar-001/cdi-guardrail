# cdi_guardrail/prometheus_adapter.py

from prometheus_client import Counter, Histogram, Gauge


class PrometheusCDILogger:
    """
    Prometheus adapter for CDI Guardrail.

    This does NOT replace CDILogger.
    It consumes the same signals and exports metrics.
    """

    def __init__(self, namespace: str = "cdi"):
        self.namespace = namespace

        # Per-prediction metrics
        self.cdi_value = Histogram(
            name="cdi_value",
            documentation="CDI value per prediction",
            namespace=namespace,
            buckets=[0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99, 1.0],
        )

        self.prediction_latency = Histogram(
            name="prediction_latency_ms",
            documentation="Prediction latency in ms",
            namespace=namespace,
            buckets=[1, 5, 10, 20, 50, 100, 200, 500],
        )

        self.decision_count = Counter(
            name="decision_total",
            documentation="Decision counts by type",
            namespace=namespace,
            labelnames=["decision"],
        )

        # Monitoring metrics
        self.cdi_mean = Gauge(
            name="cdi_mean",
            documentation="Rolling mean CDI",
            namespace=namespace,
        )

        self.cdi_p95 = Gauge(
            name="cdi_p95",
            documentation="Rolling p95 CDI",
            namespace=namespace,
        )

        # Drift metrics
        self.ks_statistic = Gauge(
            name="cdi_ks_statistic",
            documentation="KS statistic for CDI drift",
            namespace=namespace,
        )

        self.psi_value = Gauge(
            name="cdi_psi",
            documentation="Population Stability Index for CDI",
            namespace=namespace,
        )

        self.ks_drift_flag = Gauge(
            name="cdi_ks_drift",
            documentation="KS drift detected (1 = drift)",
            namespace=namespace,
        )

    # -------- adapters --------

    def log_prediction(self, cdi_value, decision, latency_ms=None):
        self.cdi_value.observe(float(cdi_value))
        self.decision_count.labels(decision=decision).inc()

        if latency_ms is not None:
            self.prediction_latency.observe(float(latency_ms))

    def log_monitor_summary(self, summary: dict):
        if not summary:
            return

        self.cdi_mean.set(summary["mean"])
        self.cdi_p95.set(summary["p95"])

    def log_drift(self, ks_result: dict, psi_value: float):
        self.ks_statistic.set(ks_result["statistic"])
        self.psi_value.set(float(psi_value))
        self.ks_drift_flag.set(1.0 if ks_result["drift"] else 0.0)
