# Decision Science and Systems Modeling

This companion directory supports the article **"Decision Science and Systems Modeling."**

The workflows operationalize systems modeling as a reproducible decision-science problem involving dynamic system response, stock-and-flow logic, feedback loops, delayed effects, resilience capacity, scenario performance, sensitivity, threshold risk, robust intervention paths, and decision-record scaffolding.

## Core Claim

Decision science and systems modeling work together when decisions are treated as interventions inside dynamic systems. Systems modeling helps make structure, assumptions, delays, feedback, accumulations, thresholds, and policy sensitivity explicit before choices become costly, irreversible, or politically difficult to revise.

## Modeling Principles

1. Define the decision before building the model.
2. Document the system boundary and what is excluded.
3. Represent choices as interventions in stocks, flows, rules, signals, incentives, or structure.
4. Make feedback loops, delays, thresholds, and accumulations explicit.
5. Compare strategies across scenarios rather than relying on one expected case.
6. Test sensitivity to uncertain parameters and structural assumptions.
7. Track worst-case performance and threshold failures.
8. Treat model outputs as structured hypotheses, not certainty.
9. Connect model outputs to monitoring and revision triggers.
10. Preserve model assumptions and decision rationale in decision records.

## Quick Start

From this article directory:

```bash
python3 python/run_all_systems_modeling_workflows.py
Rscript r/run_all_systems_modeling_workflows.R
```

Outputs are written to:

```text
outputs/tables/
outputs/figures/
outputs/decision_records/
```
