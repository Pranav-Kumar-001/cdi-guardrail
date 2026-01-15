# cdi_guardrail/pressure.py

import torch
import torch.nn.functional as F

def activation_and_param_pressure(
    loss,
    activations,
    model
):
    """
    Computes internal pressure as:
    - sum of activation gradient norms
    - parameter gradient norm

    Parameters
    ----------
    loss : torch.Tensor (scalar)
    activations : dict[str, torch.Tensor]
        Forward-hooked activations with retain_grad()
    model : torch.nn.Module

    Returns
    -------
    torch.Tensor (scalar)
    """
    # Backward pass
    model.zero_grad()
    loss.backward(retain_graph=True)

    # Activation pressure
    act_pressure = torch.zeros((), device=loss.device)
    for v in activations.values():
        if v.grad is not None:
            act_pressure += v.grad.norm()

    # Parameter pressure
    param_pressure = torch.sqrt(
        sum(
            (p.grad ** 2).sum()
            for p in model.parameters()
            if p.grad is not None
        )
    )

    return act_pressure + param_pressure
