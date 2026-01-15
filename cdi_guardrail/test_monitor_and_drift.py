import numpy as np
import random

from cdi_guardrail import CDIMonitor, ks_drift, population_stability_index

# =========================
# A) Setup
# =========================
random.seed(0)
np.random.seed(0)

print("\n[TEST] CDI Monitor + Drift Detection")

# Simulate baseline CDI distribution (healthy system)
baseline_cdi = np.clip(
    np.random.normal(loc=0.75, scale=0.05, size=1000),
    0.0,
    1.0
)

# =========================
# B) Monitor sanity check
# =========================
monitor = CDIMonitor(window_size=1000)

for v in baseline_cdi:
    monitor.update(v)

summary = monitor.summary()

print("\n[TEST] Monitor summary")
print(summary)

# Assertions
assert summary["count"] == 1000
assert 0.6 < summary["mean"] < 0.9
assert summary["p95"] >= summary["p90"] >= summary["p50"]

print("[PASS] Monitor statistics sane")

# =========================
# C) No-drift case
# =========================
current_same = np.clip(
    np.random.normal(loc=0.75, scale=0.05, size=1000),
    0.0,
    1.0
)

ks_same = ks_drift(baseline_cdi, current_same)
psi_same = population_stability_index(baseline_cdi, current_same)

print("\n[TEST] No-drift case")
print("KS:", ks_same)
print("PSI:", psi_same)

assert ks_same["drift"] is False
assert psi_same < 0.1

print("[PASS] No false drift detected")

# =========================
# D) Drift case (high CDI shift)
# =========================
current_drift = np.clip(
    np.random.normal(loc=0.92, scale=0.03, size=1000),
    0.0,
    1.0
)

ks_d = ks_drift(baseline_cdi, current_drift)
psi_d = population_stability_index(baseline_cdi, current_drift)

print("\n[TEST] Drift case")
print("KS:", ks_d)
print("PSI:", psi_d)

assert ks_d["drift"] is True
assert psi_d > 0.2

print("[PASS] Drift correctly detected")

# =========================
# E) Edge case: empty monitor
# =========================
empty_monitor = CDIMonitor(window_size=100)
empty_summary = empty_monitor.summary()

assert empty_summary == {}

print("\n[PASS] Empty monitor handled correctly")

print("\n[SUCCESS] Monitor + Drift tests PASSED.")
