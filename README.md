# CDI Guardrail

**Audit-Grade Evidence for Deployed ML Model Behavior**

---

## What this is

CDI Guardrail is a lightweight, open-source library for generating **defensible evidence**
about how a machine-learning model behaved over a specific time window.

It does **not** try to improve accuracy.  
It does **not** explain individual predictions.  
It does **not** replace monitoring or observability dashboards.

It exists to answer one hard question:

> **“Can you show how the model was behaving when it mattered?”**

---

## The problem this solves

When something goes wrong with a model, teams are asked questions like:

- Was the model already unstable before the incident?
- Did internal risk increase before failures were visible?
- Why were certain decisions automatically rejected?
- What changed between model version A and B?

Most teams respond with:

- accuracy metrics (lagging and insufficient)
- raw logs (hard to interpret)
- dashboards (not frozen in time)

These are **not defensible evidence**.

CDI Guardrail generates **time-bounded, reproducible risk evidence** suitable for:

- audits
- post-mortems
- compliance reviews
- leadership scrutiny

---

## Core idea (plain English)

Every model experiences internal stress when making decisions.

**CDI (Consistency Deviation Index)** measures:

- how internally consistent the model was
- whether internal instability increased
- whether behavior stayed within calibrated policy bounds

This is done **without requiring immediate labels**
and **without knowing outcomes at inference time**.

That makes CDI suitable for:

- live systems
- delayed feedback environments
- regulated domains

---

## Mathematical definition

CDI is **not a novel uncertainty theory**.

It is a **composite statistic** that aggregates known, inspectable signals
(entropy, calibration residuals, stability proxies) over a defined time window.

For a rigorous, implementation-level definition of the mathematical signals,
aggregation logic, and theoretical scope, see:

**THEORY.md**

That document defines what CDI measures, what it does not measure,
and the constraints on interpretation.

---

## What this is NOT

To avoid misuse, CDI Guardrail explicitly does **not**:

- measure model correctness
- provide causal explanations
- assess fairness or bias
- replace monitoring or observability stacks
- act as a real-time risk gate
- provide compliance or regulatory guarantees

It measures **behavioral consistency under a fixed policy**.

---

## Where this fits in production

CDI Guardrail typically sits:

- alongside inference pipelines
- inside ML platform infrastructure
- in batch replay or audit workflows
- downstream of model deployment

It does **not** require retraining.
It does **not** require labels at inference time.

It is additive, not invasive.

---

## Installation

### From source (recommended)

```bash
git clone https://github.com/Pranav-Kumar-001/cdi-guardrail.git
cd cdi-guardrail
pip install -e .

Optional Prometheus integration:

pip install -e ".[prometheus]"

Minimal usage example (Level-1: Standard)
from cdi_guardrail import CDIGuard, CDIMonitor

guard = CDIGuard(model, fast=True)
monitor = CDIMonitor()

pred, cdi, decision = guard.forward_with_cdi(x, y)
monitor.update(cdi)


This is sufficient to begin collecting audit-grade behavioral evidence.

Advanced (Beta): Level-2 Forensic Audit Mode

Status: Advanced / Beta
Audience: Audit, risk, and ML platform engineers
Scope: Offline, post-hoc analysis only

Level-2 exists to answer:

“Why did the risk signal spike?”

It is opt-in and does not affect the standard inference path.

What Level-2 adds

Boundary decomposition (vector form)

Local prediction stability analysis

Forensic inspection for audits and post-mortems

What Level-2 does NOT do

Change CDI scoring

Affect forward_with_cdi

Add overhead to production inference

Replace the scalar CDI signal

Act as a policy gate

Level-1 remains the only production signal.

Boundary decomposition (Level-2)

In forensic mode, boundary violations are decomposed into components such as:

Calibration

Expected Calibration Error (ECE)

Stability

Sensitivity of outputs under bounded input perturbations

The stability component includes an explicit sensitivity test and is verified
to increase under controlled perturbations.

Example
audit = guard.forward_detailed(x, y)

print(audit["prediction"])
print(audit["boundary_vector"])
print(audit["boundary_scalar"])


Illustrative output:

{
  "calibration": 0.16,
  "stability":   0.001
}


Interpretation:

The observed risk was driven primarily by miscalibration,
not local prediction instability.

Limitations (important)

CDI Guardrail is intentionally constrained.

Not causal
High CDI indicates instability, not the cause of failure.

Not correctness-aware
A stable model can be wrong; an unstable model can be correct.

Not per-sample meaningful
CDI is interpreted over time windows or populations.

Level-2 is offline only
Perturbation-based analysis is computationally expensive
and unsuitable for real-time serving.

No legal custody guarantees
CDI produces evidence inputs only.
Cryptographic signing, WORM storage, and chain-of-custody
must be handled externally.

Not a compliance substitute
CDI supports governance; it does not replace human judgment
or regulatory frameworks.

These limitations are by design, not omissions.

Commercial & open-source intent

CDI Guardrail is fully open source.

Organizations typically engage commercially when they need:

correct application of the methodology

defensible interpretation of results

audit-safe narratives

accountability during reviews or incidents

The paid value is professional risk evidence, not software access.

Status

Core CDI signal: stable

Level-1 audit path: validated

Level-2 forensic mode: advanced / beta

Drift statistics: tested

Prometheus integration: optional

Report generation: defined, not automated

Final note

CDI Guardrail is intentionally boring.

Because when models are questioned by auditors, regulators,
or leadership, boring is what survives scrutiny.