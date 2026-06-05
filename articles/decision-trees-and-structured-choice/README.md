# Decision Trees and Structured Choice

This companion directory supports the article **"Decision Trees and Structured Choice."**

The workflows operationalize decision-tree analysis as a practical tool for structuring sequential choices under uncertainty. They include expected-value rollback, expected-utility-ready branch logic, value-of-information examples, probability threshold analysis, regret diagnostics, review-trigger generation, and decision-record scaffolding.

## Core Claim

Decision trees make structured choice visible. They show what can be chosen, what remains uncertain, what happens next, which outcomes may occur, and how those outcomes are valued. Their value is not only computational; they also make assumptions, sequence, uncertainty, contingent options, and review logic explicit.

## Modeling Principles

1. Define the decision before drawing branches.
2. Separate decision nodes from chance nodes.
3. Represent sequence and contingency explicitly.
4. Document probability sources and probability quality.
5. Treat terminal values as value assumptions, not mere technical inputs.
6. Use rollback analysis to evaluate downstream consequences.
7. Test probability and value thresholds.
8. Compare expected value with regret, downside exposure, and robustness when relevant.
9. Define review triggers for assumptions that could fail.
10. Preserve the tree structure, assumptions, and rationale in a decision record.

## Quick Start

From this article directory:

```bash
python3 python/run_all_decision_tree_workflows.py
Rscript r/run_all_decision_tree_workflows.R
```

Outputs are written to:

```text
outputs/tables/
outputs/figures/
outputs/decision_records/
```
