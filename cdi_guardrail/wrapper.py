# cdi_guardrail/wrapper.py

import torch
import torch.nn.functional as F

from .pressure import activation_and_param_pressure
from .pressure_fast import representation_pressure
from .boundary import expected_calibration_error
from .scorer import compute_cdi
from .policy import CDIPolicy


class CDIGuard:
    """
    Wraps a PyTorch classification model with CDI risk scoring.
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
            reject_threshold=0.9
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
            out.retain_grad()
            self.activations[name] = out
        return hook

    @torch.no_grad()
    def predict(self, x):
        logits = self.model(x)
        return logits.argmax(dim=1)

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
                y
            )
        else:
            internal_pressure = activation_and_param_pressure(
                loss,
                self.activations,
                self.model
            )

        boundary = expected_calibration_error(
            logits.detach(),
            y.detach()
        )

        cdi = compute_cdi(
            internal_pressure,
            boundary
        ).item()

        decision = self.policy.decide(cdi)
        pred = logits.argmax(dim=1)

        return pred, cdi, decision
