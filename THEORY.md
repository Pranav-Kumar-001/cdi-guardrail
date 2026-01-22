---
# THEORY.md
---

## Consistency Deviation Index (CDI): Theory & Scope

---

## 1. Purpose of this document

This document defines the **theoretical scope** of the Consistency Deviation Index (CDI).

It answers:

- what CDI measures  
- what mathematical signals it aggregates  
- what CDI explicitly does **not** claim  

This document avoids product framing, governance language, and marketing terminology.

---

## 2. Problem setting

We consider a deployed machine learning model:

f_θ : X → Y


operating in a production environment where:

- ground-truth labels may be delayed, sparse, or unavailable  
- model behavior must be reviewed retrospectively  
- correctness cannot be directly evaluated at inference time  

The objective is **not** to estimate prediction error, but to quantify **behavioral instability** under operational conditions.

---

## 3. Definition: Behavioral consistency

We define **behavioral consistency** as:

> The degree to which a model produces stable, self-consistent outputs under small variations in input, time, or operating conditions.

Inconsistency is treated as a **risk signal**, not a failure signal.

---

## 4. What CDI is

**CDI is a composite statistic**, defined over a time window `T`, that aggregates multiple measurable indicators of model instability.

Formally:

CDI(T) = A( S1(T), S2(T), …, Sn(T) )


Where:

- `Si` are instability-related signals  
- `A` is a transparent aggregation function  
  (e.g., weighted sum, percentile statistics)

CDI is **not a new uncertainty measure** and does not introduce novel probability theory.

---

## 5. Signal families used in CDI

CDI may include one or more of the following signal families.

The exact combination is implementation- and policy-dependent.

---

### 5.1 Confidence / uncertainty proxies

These are per-inference quantities derived from model outputs.

#### Prediction entropy

H(x) = - Σk p_k(x) · log p_k(x)


#### Softmax margin

M(x) = 1 − max_k p_k(x)


These quantities measure **model indecision**, not correctness.

---

### 5.2 Calibration residuals (population-level)

Calibration is evaluated **over time windows**, not individual predictions.

Given confidence bins `Bj`:

ECE = Σj ( |Bj| / N ) · | acc(Bj) − conf(Bj) |


Notes:

- CDI does not assume immediate labels  
- calibration may be evaluated using delayed or proxy feedback  
- calibration is optional and policy-gated  

---

### 5.3 Stability under local perturbations (optional)

Given an input `x` and a perturbation distribution  
`δ ~ B_ε`:

Stability(x) = E_δ [ D( f(x), f(x + δ) ) ]


Where:

- `D` is a divergence measure  
  (e.g., KL divergence, L2 norm, class-flip indicator)  
- `ε` defines a local neighborhood  

This captures **local sensitivity**, not global drift.

---

### 5.4 Distributional drift statistics (contextual)

CDI may be reported alongside classical drift measures such as:

- Kolmogorov–Smirnov test  
- Population Stability Index (PSI)  

These are **not part of CDI**, but provide contextual evidence.

---

## 6. Aggregation over time

CDI is meaningful only when aggregated over a time window `T`.

Typical statistics include:

- mean  
- p95 / p99  
- threshold exceedance rate  

Per-sample CDI values are **not interpreted in isolation**.

---

## 7. What CDI does NOT measure

CDI explicitly does **not** measure:

- prediction correctness  
- causal model failure  
- fairness or bias  
- epistemic vs aleatoric uncertainty separation  
- regulatory compliance  

CDI measures **internal behavioral deviation**, not outcomes.

---

## 8. Interpretation constraints

A high CDI value indicates:

> The model exhibited increased internal instability during the window `T`.

It does **not** imply:

- the model was wrong  
- the model should have been disabled  
- a specific failure cause  

Interpretation requires human judgment and contextual data.

---

## 9. Operational scope

### Supported use cases

- post-mortem analysis  
- audit preparation  
- deployment comparison  
- policy threshold justification  

### Unsupported use cases

- real-time gating  
- automated approval systems  
- safety guarantees  
- model selection  

---

## 10. Computational considerations

- **Level 1 CDI**: single-pass inference, low overhead  
- **Level 2 CDI**: multi-pass perturbation analysis, offline only  

CDI makes **no guarantees** about latency suitability in serving paths.

---

## 11. Relationship to existing literature

CDI draws from established techniques:

- uncertainty proxies  
- calibration theory  
- local sensitivity analysis  
- statistical drift detection  

It does **not** claim theoretical novelty.

The contribution is **systematization for auditability**, not new math.

---

## 12. Summary

- CDI is a composite instability index  
- CDI aggregates known signals  
- CDI operates without per-sample labels  
- CDI is descriptive, not prescriptive  
- CDI supports evidence generation, not decisions  

This document defines scope, not endorsement.

---

## Design principle

> **Transparency over novelty**  
> **Auditability over automation**  
> **Evidence over opinion**

---
