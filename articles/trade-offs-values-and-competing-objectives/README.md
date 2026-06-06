# Trade-Offs, Values, and Competing Objectives

This companion directory supports the article **"Trade-Offs, Values, and Competing Objectives."**

The workflows operationalize trade-off analysis as a reproducible decision-science problem involving competing objectives, value weights, dominated-option review, rank stability, scenario regret, robustness, stakeholder value profiles, review queues, and decision-record scaffolding.

## Core Claim

Trade-offs are not secondary complications in decision science. They are often the central structure of the decision itself. Better decisions do not eliminate trade-offs; they make trade-offs explicit, examine the values behind them, test how conclusions change under different assumptions, and document what is being sacrificed, protected, deferred, or prioritized.

## Modeling Principles

1. Make competing objectives explicit.
2. Treat weights as value judgments, not neutral parameters.
3. Identify dominated options before accepting sacrifice.
4. Distinguish real trade-offs from false trade-offs caused by narrow framing.
5. Use thresholds when some values should not be fully compensatory.
6. Evaluate distributional consequences across stakeholders.
7. Test rank stability under changing priorities.
8. Compare regret across value scenarios.
9. Treat robustness as important under uncertainty.
10. Preserve decision records for what was traded, why, by whom, and with what review triggers.

## Quick Start

From this article directory:

```bash
python3 python/run_all_tradeoff_workflows.py
Rscript r/run_all_tradeoff_workflows.R
```

Outputs are written to:

```text
outputs/tables/
outputs/figures/
outputs/decision_records/
```
