# Decision-Making Under Deep Uncertainty

This companion directory supports the article **"Decision-Making Under Deep Uncertainty."**

The workflows operationalize deep uncertainty as a reproducible decision-science problem involving ambiguous futures, contested model assumptions, scenario-weight profiles, regret, robustness, vulnerability analysis, adaptive pathways, structural uncertainty simulation, review triggers, and decision-record scaffolding.

## Core Claim

Decision-making under deep uncertainty is necessary when future conditions are unknown, probabilities cannot be reliably estimated, models of system behavior are contested, and values or thresholds may be disputed. Under these conditions, decision-makers should not pretend uncertainty has been solved. They should explore many plausible futures, identify strategy vulnerabilities, compare robustness and regret, preserve flexibility, and document assumptions, trade-offs, thresholds, and revision triggers.

## Modeling Principles

1. Distinguish risk, ordinary uncertainty, and deep uncertainty.
2. Treat models as exploratory tools rather than final forecasts.
3. Compare strategies across many plausible futures.
4. Evaluate robustness, regret, threshold compliance, and vulnerability sets.
5. Test ambiguity profiles when scenario weights or value priorities are contested.
6. Identify failure conditions instead of focusing only on averages.
7. Preserve adaptive capacity through staged commitments and triggers.
8. Connect adaptation to governance, authority, monitoring, and review.
9. Document assumptions, scenarios, thresholds, trade-offs, dissent, and selected actions.
10. Use decision records to support learning before hindsight rewrites the decision.

## Quick Start

From this article directory:

```bash
python3 python/run_all_deep_uncertainty_workflows.py
Rscript r/run_all_deep_uncertainty_workflows.R
```

Outputs are written to:

```text
outputs/tables/
outputs/figures/
outputs/decision_records/
```
