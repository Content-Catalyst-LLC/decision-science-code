# What Is Decision Science?

This companion directory supports the article **"What Is Decision Science?"**

The workflows model decision science as structured judgment under uncertainty, complexity, and competing objectives. The examples emphasize alternatives, criteria, evidence, assumptions, scenarios, expected value, expected utility, regret, robustness, sensitivity analysis, multi-criteria decision analysis, and accountable decision records.

## Directory Structure

```text
articles/what-is-decision-science/
├── python/
├── r/
├── julia/
├── sql/
├── rust/
├── go/
├── cpp/
├── fortran/
├── c/
├── docs/
├── data/
├── outputs/
└── notebooks/
```

## Modeling Principles

1. Define the decision before modeling options.
2. Distinguish outcome quality from decision-process quality.
3. Make alternatives explicit.
4. Represent uncertainty honestly.
5. Surface values and trade-offs.
6. Use sensitivity analysis to test assumption dependence.
7. Prefer robustness over fragile optimization under deep uncertainty.
8. Document decision records for accountability and learning.
9. Treat computational models as supports for judgment, not replacements for responsibility.

## Quick Start

From this article directory:

```bash
python3 python/run_all_decision_science_workflows.py
Rscript r/run_all_decision_science_workflows.R
```

Outputs are written to:

```text
outputs/tables/
outputs/figures/
outputs/decision_records/
```
