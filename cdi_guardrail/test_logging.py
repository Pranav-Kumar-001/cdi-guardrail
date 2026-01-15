import time
import json
import numpy as np

from cdi_guardrail import CDILogger, CDIMonitor, ks_drift, population_stability_index

print("\n[TEST] CDI Logging")

# =========================
# A) Capture logs instead of printing
# =========================
records = []

class TestLogger(CDILogger):
    def emit(self, record: dict):
        # Ensure JSON-serializable
        json.dumps(record)
        records.append(record)

logger = TestLogger(service_name="test_service")

# =========================
# B) Test prediction logging
# =========================
logger.log_prediction(
    cdi_value=0.82,
    decision="warn",
    latency_ms=12.3
)

assert len(records) == 1
rec = records[-1]

print("\n[TEST] Prediction log")
print(rec)

assert rec["service"] == "test_service"
assert rec["event"] == "prediction"
assert isinstance(rec["cdi"], float)
assert rec["decision"] in {"accept", "warn", "reject"}
assert isinstance(rec["timestamp"], float)
assert isinstance(rec["latency_ms"], float)

print("[PASS] Prediction logging")

# =========================
# C) Test monitor summary logging
# =========================
monitor = CDIMonitor(window_size=100)

for v in np.random.uniform(0.6, 0.9, size=100):
    monitor.update(float(v))

summary = monitor.summary()

logger.log_monitor_summary(summary)
rec = records[-1]

print("\n[TEST] Monitor summary log")
print(rec)

assert rec["event"] == "cdi_summary"
assert rec["count"] == 100
assert "mean" in rec
assert "p95" in rec

print("[PASS] Monitor summary logging")

# =========================
# D) Test drift logging
# =========================
baseline = np.random.normal(0.7, 0.05, size=500)
current = np.random.normal(0.9, 0.03, size=500)

ks = ks_drift(baseline, current)
psi = population_stability_index(baseline, current)

logger.log_drift(ks, psi)
rec = records[-1]

print("\n[TEST] Drift log")
print(rec)

assert rec["event"] == "cdi_drift"
assert isinstance(rec["ks_statistic"], float)
assert isinstance(rec["ks_p_value"], float)
assert isinstance(rec["ks_drift"], bool)
assert isinstance(rec["psi"], float)

print("[PASS] Drift logging")

# =========================
# E) Final check
# =========================
assert len(records) == 3

print("\n[SUCCESS] Logging tests PASSED.")
