# cdi_guardrail/boundary_vector.py

import torch

from .boundary import expected_calibration_error
from .boundary_stability import prediction_stability_gap


def compute_boundary_vector(
    *,
    model,
    x: torch.Tensor,
    logits: torch.Tensor,
    labels: torch.Tensor,
    stability_eps: float = 1e-3,
    stability_samples: int = 1,
):
    """
    Compute vector-valued boundary violations.

    This function decomposes boundary violations into
    interpretable components without changing CDI logic.

    Components
    ----------
    - calibration : Expected Calibration Error (ECE)
    - stability   : Prediction Stability Gap (PSG)

    Returns
    -------
    dict[str, torch.Tensor]
        Keys: {"calibration", "stability"}
        Values: non-negative scalar tensors
    """
    boundaries = {}

    # Calibration boundary
    boundaries["calibration"] = expected_calibration_error(
        logits.detach(),
        labels.detach()
    )

    # Stability boundary
    boundaries["stability"] = prediction_stability_gap(
        model=model,
        x=x,
        eps=stability_eps,
        n_samples=stability_samples,
    )

    return boundaries


def reduce_boundary_vector(
    boundary_dict: dict,
    reduction: str = "l2",
):
    """
    Reduce a boundary vector into a single scalar.

    Parameters
    ----------
    boundary_dict : dict[str, torch.Tensor]
        Output of compute_boundary_vector
    reduction : {"l2", "l1", "max"}
        Reduction method

    Returns
    -------
    torch.Tensor (scalar)
    """
    values = torch.stack(list(boundary_dict.values()))

    if reduction == "l2":
        return torch.norm(values, p=2)
    elif reduction == "l1":
        return torch.norm(values, p=1)
    elif reduction == "max":
        return values.max()
    else:
        raise ValueError(f"Unknown reduction: {reduction}")
