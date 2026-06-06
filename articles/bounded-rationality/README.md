# Bounded Rationality

This companion directory supports the article **"Bounded Rationality."**

The workflows operationalize bounded rationality as structured decision-making under limits of information, attention, time, search cost, organizational capacity, and uncertainty. They include bounded-search simulations, satisficing versus optimization comparisons, aspiration-level adaptation, stopping-rule diagnostics, opportunity-loss estimates, organizational constraint models, review queues, and decision-record scaffolding.

## Core Claim

Bounded rationality does not mean irrationality. It means that real decision-makers reason under constraints. Decision science improves judgment by designing search, thresholds, tools, routines, records, and feedback systems that fit finite human and institutional capacity.

## Modeling Principles

1. Define the decision before searching for alternatives.
2. Treat alternatives as discovered or constructed, not automatically complete.
3. Make aspiration thresholds explicit.
4. Account for search cost and the marginal value of additional evidence.
5. Compare optimization benchmarks with satisficing behavior.
6. Evaluate search order, stopping rules, opportunity loss, and net value.
7. Model cognitive, informational, temporal, and institutional constraints.
8. Treat decision tools as supports for bounded judgment, not replacements for responsibility.
9. Use adaptive aspiration levels when feedback changes what counts as good enough.
10. Preserve decision records for assumptions, thresholds, search rules, selected options, rejected options, and review triggers.

## Quick Start

From this article directory:

```bash
python3 python/run_all_bounded_rationality_workflows.py
Rscript r/run_all_bounded_rationality_workflows.R
```

Outputs are written to:

```text
outputs/tables/
outputs/figures/
outputs/decision_records/
```
