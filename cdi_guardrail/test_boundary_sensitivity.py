# cdi_guardrail/test_boundary_sensitivity.py

import torch
from torchvision import models

from cdi_guardrail.wrapper import CDIGuard


print("\n[TEST] Boundary stability sensitivity")

model = models.resnet18(weights=None).eval()

guard = CDIGuard(
    model,
    activation_layers=["layer4"],
    fast=True,
)

x = torch.randn(1, 3, 224, 224)
y = torch.tensor([0])

# Small perturbation
out_small = guard.forward_detailed(
    x,
    y,
    stability_eps=1e-4,
    stability_samples=1,
)

# Larger perturbation
out_large = guard.forward_detailed(
    x,
    y,
    stability_eps=1e-1,
    stability_samples=1,
)

stability_small = out_small["boundary_vector"]["stability"].item()
stability_large = out_large["boundary_vector"]["stability"].item()

print("Stability (small eps):", stability_small)
print("Stability (large eps):", stability_large)

assert stability_small >= 0.0
assert stability_large >= 0.0
assert stability_large > stability_small, (
    "Stability boundary did not increase under larger perturbation"
)

print("[PASS] Stability sensitivity detected")
