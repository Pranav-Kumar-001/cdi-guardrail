from prometheus_client import CollectorRegistry
from prometheus_client.exposition import generate_latest

from cdi_guardrail import PrometheusCDILogger

print("\n[TEST] Prometheus Adapter")

# Use isolated registry (important for tests)
registry = CollectorRegistry()

# Monkey-patch registry into metrics
logger = PrometheusCDILogger(namespace="test")

# =========================
# Prediction logging
# =========================
logger.log_prediction(cdi_value=0.85, decision="warn", latency_ms=12.0)
logger.log_prediction(cdi_value=0.95, decision="reject")

# =========================
# Monitor logging
# =========================
logger.log_monitor_summary({
    "mean": 0.78,
    "p95": 0.92
})

# =========================
# Drift logging
# =========================
logger.log_drift(
    ks_result={"statistic": 0.91, "p_value": 0.001, "drift": True},
    psi_value=0.42
)

# =========================
# Scrape metrics
# =========================
metrics = generate_latest()

metrics_text = metrics.decode("utf-8")
print(metrics_text)

# Assertions
assert "cdi_value_bucket" in metrics_text
assert "decision_total" in metrics_text
assert "cdi_mean" in metrics_text
assert "cdi_p95" in metrics_text
assert "cdi_ks_drift" in metrics_text
assert "cdi_psi" in metrics_text

print("[SUCCESS] Prometheus adapter tests PASSED.")
