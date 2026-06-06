# Decision Hygiene and Bias Reduction

This companion directory supports the article **"Decision Hygiene and Bias Reduction."**

The workflows operationalize decision hygiene as a reproducible decision-science problem involving bias diagnostics, noise audits, calibration, evidence-quality review, framing checks, independent estimates, structured dissent, model validation, review queues, and decision-record scaffolding.

## Core Claim

Decision hygiene reduces predictable distortion before decisions are finalized. Better decisions do not come from telling people to be less biased. They come from designing cleaner judgment conditions: independent estimates, explicit criteria, base-rate checks, structured dissent, calibrated confidence, evidence review, decision records, and post-decision learning.

## Modeling Principles

1. Treat bias reduction as process design, not individual willpower.
2. Separate systematic bias from unwanted noise.
3. Preserve independent estimates before anchoring or social influence.
4. Use evidence inventories, base rates, reference classes, and disconfirming evidence.
5. Test alternative frames before the decision hardens.
6. Score confidence and forecasts against outcomes.
7. Use structured dissent, premortems, and red teams.
8. Audit models and AI outputs for false precision, drift, calibration, and subgroup performance.
9. Preserve decision records before hindsight rewrites the decision.
10. Scale hygiene to stakes, uncertainty, reversibility, and harm potential.

## Quick Start

From this article directory:

```bash
python3 python/run_all_decision_hygiene_workflows.py
Rscript r/run_all_decision_hygiene_workflows.R
```

Outputs are written to:

```text
outputs/tables/
outputs/figures/
outputs/decision_records/
```
