# Risk Analysis and Probabilistic Reasoning

This companion directory supports the article **"Risk Analysis and Probabilistic Reasoning."**

The workflows operationalize risk analysis as a reproducible decision-science practice. They include expected-loss calculation, volatility measurement, tail-risk diagnostics, value-at-risk and conditional-value-at-risk estimates, threshold-breach analysis, probability-quality auditing, scenario stress testing, Bayesian risk updating, and decision-record scaffolding.

## Core Claim

Risk analysis connects uncertainty to consequence. Probabilistic reasoning provides the formal language for representing likelihood, updating beliefs, and comparing uncertain outcomes. A useful risk analysis does not merely calculate averages. It examines downside exposure, tail behavior, uncertainty quality, scenario stress, model assumptions, and review triggers.

## Modeling Principles

1. Define the decision and risk context before calculating risk.
2. Separate hazards, exposure, vulnerability, consequence, and response capacity.
3. Represent uncertainty explicitly and document probability quality.
4. Use expected loss as a baseline, not as the whole analysis.
5. Compare volatility, threshold breaches, tail loss, and stress exposure.
6. Use Bayesian updating when risk estimates should change with evidence.
7. Treat model outputs as assumptions-dependent decision support.
8. Communicate uncertainty without false precision.
9. Preserve risk assumptions and review triggers in decision records.
10. Treat computational models as supports for judgment, not replacements for responsibility.

## Quick Start

From this article directory:

```bash
python3 python/run_all_risk_analysis_workflows.py
Rscript r/run_all_risk_analysis_workflows.R
```

Outputs are written to:

```text
outputs/tables/
outputs/figures/
outputs/decision_records/
```
