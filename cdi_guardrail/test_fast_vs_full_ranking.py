import torch
import numpy as np
from torch.utils.data import DataLoader
from torchvision import datasets, transforms, models
from scipy.stats import spearmanr

from cdi_guardrail import CDIGuard, CDIPolicy

# =========================
# A) Setup
# =========================
device = "cuda" if torch.cuda.is_available() else "cpu"
torch.manual_seed(0)

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

model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
model.to(device)
model.eval()

activation_layers = ["layer4"]  # last block only (important)

# =========================
# B) Guards
# =========================
policy = CDIPolicy(
    warn_threshold=0.7,
    reject_threshold=0.9
)

guard_full = CDIGuard(
    model,
    policy=policy,
    activation_layers=activation_layers,
    fast=False
)

guard_fast = CDIGuard(
    model,
    policy=policy,
    activation_layers=activation_layers,
    fast=True
)

# =========================
# C) Collect CDI scores
# =========================
print("\n[TEST] Collecting CDI scores (full vs fast)...")

full_scores = []
fast_scores = []

for i, (x, y) in enumerate(loader):
    if i == 50:  # keep test fast
        break

    x = x.to(device)
    y = y.to(device)

    _, cdi_full, _ = guard_full.forward_with_cdi(x, y)
    _, cdi_fast, _ = guard_fast.forward_with_cdi(x, y)

    full_scores.append(cdi_full)
    fast_scores.append(cdi_fast)

full_scores = np.array(full_scores)
fast_scores = np.array(fast_scores)

# =========================
# D) Rank correlation
# =========================
rho, p = spearmanr(full_scores, fast_scores)

print("\n[RESULT] Fast vs Full CDI ranking")
print("--------------------------------")
print(f"Spearman rho: {rho:.4f}")
print(f"P-value:     {p:.4e}")

# =========================
# E) Assertions
# =========================
assert not np.isnan(rho), "Correlation is NaN"
assert rho > 0.7, "Ranking correlation too low — fast CDI not valid"

print("\n[SUCCESS] Fast CDI preserves ranking (rho > 0.7)")
