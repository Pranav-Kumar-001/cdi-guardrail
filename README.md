# CDI Guardrail

**Defensible Risk Evidence for Deployed ML Models**

---

## What this is

CDI Guardrail is a lightweight library for generating defensible evidence about how a machine-learning model behaved over a specific time window.

It does **not** try to improve accuracy.  
It does **not** explain predictions.  
It does **not** replace monitoring dashboards.

It exists to answer one hard question:

> **“Can you prove how your model was behaving when it mattered?”**

---

## The problem this solves

When something goes wrong with a model, teams are asked questions like:

- Was the model already unstable before the incident?
- Did internal risk increase before failures were visible?
- Why were certain decisions automatically rejected?
- What changed between model version A and B?

Most teams respond with:

- accuracy metrics (insufficient)
- logs (not interpretable)
- dashboards (not frozen in time)

These are **not defensible evidence**.

CDI Guardrail generates **time-bounded risk evidence** that survives:

- audits
- post-mortems
- compliance reviews
- leadership scrutiny

---

## Core idea (plain English)

Every model experiences internal strain when making decisions.

**CDI (Consistency Deviation Index)** measures:

- how internally consistent the model was
- how much internal pressure it experienced
- whether that pressure stayed within calibrated bounds

This is done **without requiring labels** and **without knowing outcomes**.

That makes CDI suitable for:

- live systems
- delayed feedback
- regulated environments

---

## The paid use case (important)

### How teams use this for audit & incident response

**Typical workflow:**

1. A model runs in production
2. CDI, decision rates, and drift signals are collected
3. An incident occurs (or an audit is requested)
4. A **Time-Bounded Model Risk Evidence Report** is generated
5. The report is shared with:
   - risk & compliance
   - engineering leadership
   - auditors / regulators

The report answers:

- What did the model’s internal risk look like?
- Did it drift from its baseline?
- Were automated decisions justified under policy?

This shifts conversations from **opinions** to **evidence**.

---

## What the evidence report contains

A single report includes:

### Model identity
- version
- hash
- deployment environment

### Policy in effect
- calibrated thresholds
- expected reject rates

### Time window
- exact start/end
- number of predictions

### Risk summary
- mean / p95 / p99 CDI
- reject and warn rates

### Drift analysis
- KS test
- PSI
- interpretation

### Policy justification
- why thresholds exist
- what behavior was expected

### Machine-readable appendix
- JSON snapshot for archival or audit ingestion

The report is **frozen in time** and can be archived or signed.

---

## What this is NOT

To avoid misuse, CDI Guardrail explicitly does **not**:

- measure model correctness
- assess fairness or bias
- explain individual predictions
- replace monitoring dashboards
- provide a hosted SaaS

It measures **internal consistency under a fixed policy**.

---

## Where this fits in production

CDI Guardrail typically sits:

- alongside inference code
- inside ML platform infrastructure
- downstream of model deployment

It does **not** require retraining or labels.

---

## Installation

### From source (recommended for evaluation and pilots)

```bash
git clone https://github.com/Pranav-Kumar-001/cdi-guardrail.git
cd cdi-guardrail
pip install -e .

Optional dependencies
pip install -e ".[prometheus]"

Minimal usage example (Level-1: Standard)

A lightweight monitor aggregates CDI statistics over time.

from cdi_guardrail import CDIGuard, CDIMonitor

guard = CDIGuard(model, fast=True)
monitor = CDIMonitor()

# Labels are optional and may be unavailable in production
pred, cdi, decision = guard.forward_with_cdi(x, y)
monitor.update(cdi)


That’s enough to begin collecting defensible risk evidence.

⚠️ Advanced (Beta): Level-2 Audit Mode

Status: Advanced / Beta
Audience: Audit, risk, and platform engineers
Not required for standard usage

CDI Guardrail also provides an opt-in forensic audit path for advanced users who need to answer:

“Why did the risk signal spike?”

What Level-2 adds (and what it does not)
Adds

Decomposed boundary evidence

Local prediction stability analysis

Forensic inspection for audits and post-mortems

Does NOT

Change CDI scoring

Affect forward_with_cdi

Add overhead to the production path

Replace the scalar CDI signal

Level-1 remains the production risk signal.
Level-2 exists purely for inspection and evidence.

Boundary decomposition

In Level-2, boundary violations are decomposed into:

Calibration

Expected Calibration Error (ECE)

Stability

Sensitivity of output probabilities under bounded input perturbations

The stability boundary has an explicit sensitivity test and is verified to increase under controlled input perturbations.

Example: forensic inspection
from cdi_guardrail import CDIGuard

guard = CDIGuard(model, fast=True)

audit = guard.forward_detailed(x, y)

print(audit["prediction"])
print(audit["boundary_vector"])
print(audit["boundary_scalar"])

Example output (illustrative)
boundary_vector = {
  "calibration": 0.16,
  "stability":   0.001
}


Interpretation:

The model’s risk at this point was driven primarily by miscalibration, not local instability.

This kind of decomposition is useful for:

audit reports

incident reviews

regulator questions

internal root-cause analysis

Important guarantees

Level-2 is opt-in

Level-2 is read-only

Level-2 uses no gradients

Level-2 does not affect policy decisions

Level-2 may evolve (Beta)

Epistemic Integrity (Design Note)

CDI Guardrail focuses on generating defensible evidence about how a model behaved over a defined time window.

A related but distinct question is when belief escalation itself is justified, especially in the presence of:

self-referential model claims

repeated or stylistically varied signals

correlated internal or external evidence

To address this epistemic layer, a separate project — Sentinel — implements a normative belief gate that governs when belief may be escalated under correlated versus independent evidence.

Sentinel is model- and policy-agnostic and is designed to be robust against evidence inflation (e.g. echo chambers, repetition, fake probes).

Design note: notes/epistemic_integrity.md

Sentinel repository:
https://github.com/Pranav-Kumar-001/sentinel-epistemic-auditor

Commercial note

This library is used to generate formal model risk evidence reports.

Teams typically engage when they need an artifact they can hand to:

audit

legal

regulators

Organizations most often seek support for:

calibration

setup

report generation

audit or incident response

Status

Core CDI signal: stable

Fast inference path: validated

Monitoring & drift detection: tested

Prometheus integration: optional

Level-2 audit mode: advanced / beta

Report generation: defined, not automated

License & intent

CDI Guardrail is designed to be:

inspectable

auditable

boring (by design)

Because when risk is involved, boring is what survives scrutiny.

Final note

This project is not trying to be everything.

It is trying to be the thing you wish you had
when someone asks:

“Can you prove the model was behaving responsibly?”
