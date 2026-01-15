CDI Guardrail

Defensible Risk Evidence for Deployed ML Models

What this is

CDI Guardrail is a lightweight library for generating defensible evidence about how a machine-learning model behaved over a specific time window.

It does not try to improve accuracy.
It does not explain predictions.
It does not replace monitoring dashboards.

It exists to answer one hard question:

“Can you prove how your model was behaving when it mattered?”

The problem this solves

When something goes wrong with a model, teams are asked questions like:

“Was the model already unstable before the incident?”

“Did internal risk increase before failures were visible?”

“Why were certain decisions automatically rejected?”

“What changed between model version A and B?”

Most teams respond with:

accuracy metrics (insufficient)

logs (not interpretable)

dashboards (not frozen in time)

These are not defensible evidence.

CDI Guardrail generates time-bounded risk evidence that survives:

audits

post-mortems

compliance reviews

leadership scrutiny

Core idea (plain English)

Every model experiences internal strain when making decisions.

CDI (Consistency Deviation Index) measures:

how internally consistent the model was

how much internal pressure it experienced

whether that pressure stayed within calibrated bounds

This is done without requiring labels and without knowing outcomes.

That makes CDI suitable for:

live systems

delayed feedback

regulated environments

The paid use case (important)
How teams use this for audit & incident response

Typical workflow:

A model runs in production.

CDI, decision rates, and drift signals are collected.

An incident occurs (or an audit is requested).

A Time-Bounded Model Risk Evidence Report is generated.

That report is shared with:

risk & compliance

engineering leadership

auditors / regulators

The report answers:

What did the model’s internal risk look like?

Did it drift from its baseline?

Were automated decisions justified under policy?

This shifts conversations from opinions to evidence.

What the evidence report contains

A single report includes:

Model identity

version, hash, deployment environment

Policy in effect

calibrated thresholds, expected reject rates

Time window

exact start/end, number of predictions

Risk summary

mean / p95 / p99 CDI

reject and warn rates

Drift analysis

KS test

PSI

interpretation

Policy justification

why thresholds exist

what behavior was expected

Machine-readable appendix

JSON snapshot for archival or audit ingestion

The report is frozen in time and can be archived or signed.

What this is NOT

To avoid misuse, CDI Guardrail explicitly does not:

measure model correctness

assess fairness or bias

explain individual predictions

replace monitoring dashboards

provide a hosted SaaS

It measures internal consistency under a fixed policy.

Where this fits in production

CDI Guardrail typically sits:

alongside inference code

inside ML platform infrastructure

downstream of model deployment

It does not require retraining or labels.

Installation
pip install cdi-guardrail


Optional extras:

pip install cdi-guardrail[prometheus]

Minimal usage example

A lightweight monitor aggregates CDI statistics over time.

from cdi_guardrail import CDIGuard, CDIMonitor

guard = CDIGuard(model, fast=True)
monitor = CDIMonitor()

# Labels are optional and may be unavailable in production
pred, cdi, decision = guard.forward_with_cdi(x)
monitor.update(cdi)


That’s enough to begin collecting evidence.

Commercial note

This library is used to generate formal model risk evidence reports.

Teams typically engage us when they need a report they can hand to audit, legal, or regulators.

Organizations most often seek support for:

calibration

setup

report generation

audit or incident response

Status

Core signal: stable

Fast inference path: validated

Monitoring & drift detection: tested

Prometheus integration: optional

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