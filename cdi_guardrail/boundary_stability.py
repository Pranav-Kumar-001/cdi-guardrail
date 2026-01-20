# cdi_guardrail/boundary_stability.py

import torch
import torch.nn.functional as F


def prediction_stability_gap(
    model,
    x: torch.Tensor,
    eps: float = 1e-3,
    noise: str = "gaussian",
    n_samples: int = 1,
):
    """
    Prediction Stability Gap (PSG)

    Measures how much the model's output distribution
    changes under small, bounded input perturbations.

    This is a boundary / constraint violation signal:
    small input change -> should imply small output change.

    Parameters
    ----------
    model : torch.nn.Module
        Model in eval mode.
    x : torch.Tensor
        Input batch [B, ...]
    eps : float
        Perturbation magnitude (L-infinity scale).
    noise : {"gaussian", "uniform"}
        Perturbation type.
    n_samples : int
        Number of perturbation samples (>=1).

    Returns
    -------
    torch.Tensor (scalar)
        Mean L2 distance between original and perturbed
        output probability vectors.
    """
    assert n_samples >= 1

    model.eval()

    with torch.no_grad():
        # Original prediction
        logits = model(x)
        p = F.softmax(logits, dim=-1)

        gap = torch.zeros((), device=x.device)

        for _ in range(n_samples):
            if noise == "gaussian":
                delta = eps * torch.randn_like(x)
            elif noise == "uniform":
                delta = eps * (2.0 * torch.rand_like(x) - 1.0)
            else:
                raise ValueError(f"Unknown noise type: {noise}")

            x_perturbed = x + delta

            logits_eps = model(x_perturbed)
            p_eps = F.softmax(logits_eps, dim=-1)

            # L2 distance per sample, mean over batch
            gap += torch.norm(p - p_eps, p=2, dim=1).mean()

        gap = gap / float(n_samples)

    return gap
