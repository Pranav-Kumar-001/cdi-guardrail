# cdi_guardrail/pressure_fast.py

import torch


def representation_pressure(
    logits,
    features,
    labels
):
    """
    Fast internal pressure proxy.

    Measures gradient norm of the
    true-vs-second-best logit margin
    with respect to last-layer features.

    Parameters
    ----------
    logits : torch.Tensor [B, C]
    features : torch.Tensor [B, D]
        Last hidden representation (retain_grad enabled)
    labels : torch.Tensor [B]

    Returns
    -------
    torch.Tensor (scalar)
    """
    batch_size = logits.size(0)

    # true class logit
    true_logits = logits[torch.arange(batch_size), labels]

    # second-best logit
    masked = logits.clone()
    masked[torch.arange(batch_size), labels] = -1e9
    second_logits = masked.max(dim=1).values

    # margin loss (decision tension)
    margin = true_logits - second_logits
    loss = -margin.mean()

    grad = torch.autograd.grad(
        loss,
        features,
        retain_graph=False
    )[0]

    return grad.norm()
