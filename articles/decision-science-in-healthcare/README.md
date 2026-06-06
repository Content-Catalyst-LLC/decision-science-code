# Decision Science in Healthcare

This companion directory supports the article **"Decision Science in Healthcare."**

The workflows operationalize healthcare decision science as a reproducible decision-science problem involving clinical uncertainty, treatment strategy comparison, diagnostic probability, cost-effectiveness, shared decision-making, patient preference, equity review, hospital capacity, queue pressure, safety risk, surge response, AI decision support, and decision-record scaffolding.

## Core Claim

Healthcare decision science is not simply about choosing the statistically best option in the abstract. It is about making choices that remain clinically credible, operationally workable, ethically justified, patient-centered, and institutionally sustainable under real conditions of uncertainty.

## Modeling Principles

1. Treat healthcare decisions as probabilistic, ethical, patient-centered, and operational.
2. Make clinical evidence, uncertainty, patient values, and resource constraints explicit.
3. Separate diagnostic probability from certainty and update beliefs as evidence changes.
4. Evaluate treatment options across benefit, harm, patient preference, equity, and feasibility.
5. Analyze cost-effectiveness while preserving ethical and distributional review.
6. Model capacity, queues, staffing, discharges, safety risk, and surge response over time.
7. Include systems thinking, feedback loops, delays, and operational bottlenecks.
8. Treat AI and clinical decision support as governed components of the decision system.
9. Use monitoring, trigger points, escalation rules, and revision pathways.
10. Preserve assumptions, alternatives, patient values, equity concerns, safety risks, and revision triggers in decision records.

## Quick Start

From this article directory:

```bash
python3 python/run_all_healthcare_workflows.py
Rscript r/run_all_healthcare_workflows.R
```

Outputs are written to:

```text
outputs/tables/
outputs/figures/
outputs/decision_records/
```
