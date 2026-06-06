# Value of Information and When to Wait

This companion directory supports the article **"Value of Information and When to Wait."**

The workflows operationalize value-of-information reasoning as a reproducible decision-science problem involving expected value under current information, expected value of perfect information, expected value of sample information, decision-change probability, information costs, delay costs, net value of waiting, staged action, and decision-record scaffolding.

## Core Claim

Information has decision value only when it can change action, improve expected outcomes, reduce regret, prevent threshold failure, clarify timing, or support accountable revision. More information is not automatically better. Decision-makers must compare the expected benefit of learning with the full cost of evidence gathering and delay.

## Modeling Principles

1. Define the decision before requesting information.
2. Identify the current best action under existing evidence.
3. Ask what evidence could change the action, timing, scale, or safeguards.
4. Estimate the expected value of perfect information as an upper bound.
5. Estimate the expected value of imperfect sample information for practical evidence.
6. Subtract direct information cost and delay cost.
7. Include opportunity loss, risk exposure, option loss, and legitimacy cost.
8. Use staged action when learning and action can proceed together.
9. Define stopping rules so analysis does not become delay.
10. Preserve decision records before hindsight rewrites the rationale.

## Quick Start

From this article directory:

```bash
python3 python/run_all_value_of_information_workflows.py
Rscript r/run_all_value_of_information_workflows.R
```

Outputs are written to:

```text
outputs/tables/
outputs/figures/
outputs/decision_records/
```
