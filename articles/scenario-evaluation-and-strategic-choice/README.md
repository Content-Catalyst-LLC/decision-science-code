# Scenario Evaluation and Strategic Choice

This companion directory supports the article **"Scenario Evaluation and Strategic Choice."**

The workflows operationalize scenario evaluation as a reproducible decision-science problem involving plausible futures, strategy performance, expected value, worst-case performance, regret, scenario dispersion, threshold pass rates, vulnerability review, adaptive triggers, and decision-record scaffolding.

## Core Claim

Scenario evaluation improves strategic choice when uncertainty cannot be reduced responsibly to one forecast. Instead of asking only which future is most likely, decision-makers compare how strategies perform across plausible futures, identify where each strategy fails, and define how the strategy should adapt as evidence changes.

## Modeling Principles

1. Define the decision before building the scenario set.
2. Use scenarios as decision instruments, not only narratives.
3. Compare strategies across multiple plausible futures.
4. Evaluate expected value, worst-case performance, regret, dispersion, and threshold pass rate.
5. Treat unacceptable threshold failure as different from ordinary performance variation.
6. Identify vulnerability conditions and fragile assumptions.
7. Include stakeholder values, trade-offs, and legitimacy constraints.
8. Define monitoring indicators and adaptive triggers.
9. Preserve scenario assumptions and evaluation rules in a decision record.
10. Treat strategic choice as a selected posture, pathway, or decision architecture under uncertainty.

## Quick Start

From this article directory:

```bash
python3 python/run_all_scenario_choice_workflows.py
Rscript r/run_all_scenario_choice_workflows.R
```

Outputs are written to:

```text
outputs/tables/
outputs/figures/
outputs/decision_records/
```
