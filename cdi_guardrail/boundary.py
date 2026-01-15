# cdi_guardrail/boundary.py

import torch
import torch.nn.functional as F

def expected_calibration_error(
    logits,
    labels,
    n_bins: int = 10
):
    """
    Expected Calibration Error (ECE)

    Works per-batch; for per-sample CDI, batch size = 1.
    """
    probs = F.softmax(logits, dim=1)
    conf, pred = probs.max(dim=1)
    correct = (pred == labels).float()

    bins = torch.linspace(0, 1, n_bins + 1, device=logits.device)
    ece = torch.zeros((), device=logits.device)

    for i in range(n_bins):
        mask = (conf >= bins[i]) & (conf < bins[i + 1])
        if mask.any():
            ece += mask.float().mean() * (
                correct[mask].mean() - conf[mask].mean()
            ).abs()

    return ece
