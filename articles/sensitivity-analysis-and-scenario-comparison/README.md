# Sensitivity Analysis and Scenario Comparison

This companion directory supports the article **"Sensitivity Analysis and Scenario Comparison."**

The workflows operationalize sensitivity analysis and scenario comparison as professional decision-science practices. They include one-way sensitivity, multi-way sensitivity, threshold testing, scenario comparison, robustness scoring, regret analysis, probabilistic sensitivity, key-driver diagnostics, synthetic decision records, and multi-language scaffolds.

## Core Claim

Sensitivity analysis and scenario comparison reveal how decisions change when assumptions, parameters, risks, evidence, and external conditions shift. Their purpose is not to produce more analysis for its own sake. Their purpose is to expose assumption dependence, fragile recommendations, key drivers, thresholds, ranking reversals, regret exposure, and robustness across plausible futures.

## Modeling Principles

1. Define the decision and baseline model before varying assumptions.
2. Identify uncertain, contested, high-impact, and controllable inputs.
3. Document plausible ranges and evidence quality.
4. Test one-way sensitivity for interpretability.
5. Test multi-way and probabilistic sensitivity for interaction effects.
6. Identify thresholds where preferences reverse.
7. Compare strategies across coherent scenarios.
8. Evaluate robustness, regret, downside breach, and ranking stability.
9. Translate key drivers into review triggers and monitoring indicators.
10. Treat computational models as supports for judgment, not replacements for responsibility.

## Quick Start

From this article directory:

```bash
python3 python/run_all_sensitivity_workflows.py
Rscript r/run_all_sensitivity_workflows.R
```

Outputs are written to:

```text
outputs/tables/
outputs/figures/
outputs/decision_records/
```
