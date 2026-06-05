# Why Uncertainty Changes Decision-Making

This companion directory supports the article **"Why Uncertainty Changes Decision-Making."**

The workflows model decision-making under risk, uncertainty, ambiguity, model uncertainty, and deep uncertainty. They compare expected value, expected utility, ambiguity-adjusted value, minimax regret, robustness thresholds, option value, adaptive pathways, monitoring triggers, and decision records.

## Core Claim

Uncertainty changes decision-making because it changes the decision criterion. Under stable risk, expected utility may be appropriate. Under ambiguity and deep uncertainty, professional decision work must also evaluate regret, robustness, reversibility, option value, learning capacity, institutional capacity, and accountability.

## Modeling Principles

1. Distinguish risk, uncertainty, ambiguity, and deep uncertainty.
2. Use expected value only when probabilities and outcomes are credible.
3. Use ambiguity diagnostics when the probability structure is poorly understood.
4. Use regret and robustness when forecasts are fragile.
5. Preserve reversibility when uncertainty is high and learning is possible.
6. Compare value of information with the cost of delay.
7. Use adaptive pathways when staged decisions and monitoring are feasible.
8. Document decision records for accountability and learning.
9. Treat computational models as supports for judgment, not substitutes for responsibility.

## Quick Start

From this article directory:

```bash
python3 python/run_all_uncertainty_workflows.py
Rscript r/run_all_uncertainty_workflows.R
```

Outputs are written to:

```text
outputs/tables/
outputs/figures/
outputs/decision_records/
```
