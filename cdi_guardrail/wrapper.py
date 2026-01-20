# cdi_guardrail/wrapper.py

import torch
import torch.nn.functional as F

from .boundary_vector import compute_boundary_vector, reduce_boundary_vector
from .pressure import activation_and_param_pressure
from .pressure_fast import representation_pressure
from .boundary import expected_calibration_error
from .scorer import compute_cdi
from .policy import CDIPolicy


class CDIGuard:
    """
    Wraps a PyTorch classification model with CDI risk scoring.

    Level 1:
        - forward_with_cdi : fast scalar risk signal (CDI-v0)

    Level 2:
        - forward_detailed : forensic boundary decomposition (audit path)
    """

    def __init__(
        self,
        model,
        policy: CDIPolicy | None = None,
        activation_layers: list[str] | None = None,
        fast: bool = False,
    ):
        self.model = model
        self.model.eval()

        # Conservative default policy (pre-calibration safe)
        self.policy = policy or CDIPolicy(
            warn_threshold=0.7,
            reject_threshold=0.9,
        )

        self.fast = fast
        self.activations = {}
        self.hooks = []

        if activation_layers is not None:
            self._register_hooks(activation_layers)

    def _register_hooks(self, layer_names):
        for name, module in self.model.named_modules():
            if name in layer_names:
                hook = module.register_forward_hook(
                    self._make_hook(name)
                )
                self.hooks.append(hook)

    def _make_hook(self, name):
        def hook(module, inp, out):
            # Only retain gradients if autograd is enabled
            if torch.is_grad_enabled() and out.requires_grad:
                out.retain_grad()
            self.activations[name] = out

        return hook

    @torch.no_grad()
    def predict(self, x):
        logits = self.model(x)
        return logits.argmax(dim=1)

    # ==========================================================
    # LEVEL 1 — Production / Hot Path (UNCHANGED)
    # ==========================================================
    def forward_with_cdi(self, x, y):
        """
        Forward pass + CDI computation.

        Returns:
        - prediction
        - CDI value
        - decision ('accept' | 'warn' | 'reject')
        """
        self.activations.clear()

        logits = self.model(x)
        loss = F.cross_entropy(logits, y)

        if self.fast:
            # use last activation only
            last_feature = list(self.activations.values())[-1]
            internal_pressure = representation_pressure(
                logits,
                last_feature,
                y,
            )
        else:
            internal_pressure = activation_and_param_pressure(
                loss,
                self.activations,
                self.model,
            )

        boundary = expected_calibration_error(
            logits.detach(),
            y.detach(),
        )

        cdi = compute_cdi(
            internal_pressure,
            boundary,
        ).item()

        decision = self.policy.decide(cdi)
        pred = logits.argmax(dim=1)

        return pred, cdi, decision

    # ==========================================================
    # LEVEL 2 — Forensic / Audit Path (NEW, OPT-IN)
    # ==========================================================
    def forward_detailed(
        self,
        x: torch.Tensor,
        y: torch.Tensor,
        *,
        boundary_reduction: str = "l2",
        stability_eps: float = 1e-3,
        stability_samples: int = 1,
    ):
        """
        Level-2 forensic audit path.

        Provides decomposed boundary evidence without
        affecting CDI-v0 behavior or performance.

        Returns
        -------
        dict:
            {
              "prediction": torch.Tensor,
              "boundary_vector": dict[str, torch.Tensor],
              "boundary_scalar": torch.Tensor
            }
        """
        self.activations.clear()

        with torch.no_grad():
            logits = self.model(x)
            pred = logits.argmax(dim=1)

        boundary_vector = compute_boundary_vector(
            model=self.model,
            x=x,
            logits=logits,
            labels=y,
            stability_eps=stability_eps,
            stability_samples=stability_samples,
        )

        boundary_scalar = reduce_boundary_vector(
            boundary_vector,
            reduction=boundary_reduction,
        )

        return {
            "prediction": pred,
            "boundary_vector": boundary_vector,
            "boundary_scalar": boundary_scalar,
        }
