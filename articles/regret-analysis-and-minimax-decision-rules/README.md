# Regret Analysis and Minimax Decision Rules

This companion directory supports the article **"Regret Analysis and Minimax Decision Rules."**

The workflows operationalize regret analysis as a reproducible decision-science problem involving payoff matrices, regret matrices, opportunity loss, maximin choice, minimax regret, threshold compliance, vulnerability analysis, decision-rule comparison, and decision-record scaffolding.

## Core Claim

Regret analysis compares each action with the action that would have been best after uncertainty resolves. Minimax decision rules help decision-makers choose when probabilities are unreliable, outcomes are uncertain, and the cost of being wrong matters as much as the possibility of being right.

## Modeling Principles

1. Build an explicit action-by-scenario payoff matrix.
2. Distinguish absolute performance from relative opportunity loss.
3. Calculate regret by comparing each action with the best action in each scenario.
4. Use maximin to protect the worst absolute payoff.
5. Use minimax regret to protect against the worst missed opportunity.
6. Compare expected value, maximin, minimax regret, and threshold rules.
7. Pair regret with absolute performance thresholds.
8. Test sensitivity to scenario design, action sets, and value assumptions.
9. Preserve decision records before hindsight rewrites the reasoning.
10. Treat regret analysis as decision support, not an automatic answer.

## Quick Start

From this article directory:

```bash
python3 python/run_all_regret_minimax_workflows.py
Rscript r/run_all_regret_minimax_workflows.R
```

Outputs are written to:

```text
outputs/tables/
outputs/figures/
outputs/decision_records/
```
