import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torchvision import datasets, transforms, models

from cdi_guardrail import CDIGuard, CDIPolicy, CDICalibrator

# =========================
# A) Setup
# =========================
device = "cuda" if torch.cuda.is_available() else "cpu"

torch.manual_seed(0)

# Simple CIFAR transform
transform = transforms.Compose([
    transforms.Resize(224),
    transforms.ToTensor()
])

dataset = datasets.CIFAR10(
    root="./data",
    train=False,
    download=True,
    transform=transform
)

loader = DataLoader(
    dataset,
    batch_size=1,
    shuffle=False
)

# Use pretrained ImageNet model intentionally
# (we want errors to exist)
model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
model.to(device)
model.eval()

# =========================
# B) Wrap with CDI Guard
# =========================
guard = CDIGuard(
    model,
    activation_layers=[
        "layer1",
        "layer2",
        "layer3",
        "layer4"
    ]
)

# =========================
# C) Collect CDI scores
# =========================
print("\n[TEST] Collecting CDI scores...")
cdi_scores = []
decisions = []

for i, (x, y) in enumerate(loader):
    if i == 50:  # keep test fast
        break

    x = x.to(device)
    y = y.to(device)

    pred, cdi, decision = guard.forward_with_cdi(x, y)

    # Assertions (hard failures)
    assert isinstance(cdi, float), "CDI is not a float"
    assert 0.0 < cdi <= 1.0, f"Invalid CDI value: {cdi}"
    assert decision in {"accept", "warn", "reject"}

    cdi_scores.append(cdi)
    decisions.append(decision)

print("[PASS] CDI computed for samples")

# =========================
# D) Calibrate thresholds
# =========================
print("\n[TEST] Calibrating thresholds...")
calibrator = CDICalibrator(
    warn_percentile=0.8,
    reject_percentile=0.95
)

warn_t, reject_t = calibrator.fit(cdi_scores)

assert 0 < warn_t < reject_t < 1, "Invalid calibrated thresholds"

print("Calibrated thresholds:")
print(calibrator.summary())

# =========================
# E) Apply calibrated policy
# =========================
policy = CDIPolicy(
    warn_threshold=warn_t,
    reject_threshold=reject_t
)

guard.policy = policy

print("\n[TEST] Re-running with calibrated policy...")

counts = {"accept": 0, "warn": 0, "reject": 0}

for cdi in cdi_scores:
    d = guard.policy.decide(cdi)
    counts[d] += 1

print("Decision counts after calibration:")
print(counts)

assert counts["reject"] > 0, "No rejects — calibration failed?"
assert counts["accept"] > 0, "No accepts — calibration failed?"

print("\n[SUCCESS] CDI Guardrail integration test PASSED.")
