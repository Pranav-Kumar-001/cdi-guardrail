# test_forward_detailed.py

import torch
from torchvision import models

from cdi_guardrail.wrapper import CDIGuard


def test_forward_detailed_basic():
    """
    Sanity test:
    - forward_detailed runs
    - expected keys exist
    """
    model = models.resnet18(weights=None).eval()

    guard = CDIGuard(
        model,
        activation_layers=["layer4"],
        fast=True,
    )

    x = torch.randn(1, 3, 224, 224)
    y = torch.tensor([0])

    out = guard.forward_detailed(x, y)

    assert isinstance(out, dict)
    assert "prediction" in out
    assert "boundary_vector" in out
    assert "boundary_scalar" in out


def test_boundary_vector_contents():
    """
    Boundary vector must contain known components
    and all values must be non-negative.
    """
    model = models.resnet18(weights=None).eval()
    guard = CDIGuard(model, activation_layers=["layer4"], fast=True)

    x = torch.randn(1, 3, 224, 224)
    y = torch.tensor([0])

    out = guard.forward_detailed(x, y)
    bv = out["boundary_vector"]

    assert "calibration" in bv
    assert "stability" in bv

    for k, v in bv.items():
        assert torch.is_tensor(v)
        assert v.ndim == 0
        assert v.item() >= 0.0


def test_boundary_scalar_consistency():
    """
    Reduced boundary scalar must be >=
    each individual boundary component (L2 reduction).
    """
    model = models.resnet18(weights=None).eval()
    guard = CDIGuard(model, activation_layers=["layer4"], fast=True)

    x = torch.randn(1, 3, 224, 224)
    y = torch.tensor([0])

    out = guard.forward_detailed(x, y)

    scalar = out["boundary_scalar"]
    components = out["boundary_vector"].values()

    for v in components:
        assert scalar.item() >= v.item()


def test_no_grad_safety():
    """
    forward_detailed must not require gradients
    and must not crash in no-grad mode.
    """
    model = models.resnet18(weights=None).eval()
    guard = CDIGuard(model, activation_layers=["layer4"], fast=True)

    x = torch.randn(1, 3, 224, 224)
    y = torch.tensor([0])

    with torch.no_grad():
        out = guard.forward_detailed(x, y)

    assert out["boundary_scalar"].requires_grad is False


def test_forward_with_cdi_unchanged():
    """
    Ensure forward_detailed does not affect
    the original CDI-v0 behavior.
    """
    model = models.resnet18(weights=None).eval()
    guard = CDIGuard(model, activation_layers=["layer4"], fast=True)

    x = torch.randn(1, 3, 224, 224)
    y = torch.tensor([0])

    pred, cdi, decision = guard.forward_with_cdi(x, y)

    assert isinstance(cdi, float)
    assert 0.0 < cdi <= 1.0
    assert decision in {"accept", "warn", "reject"}
