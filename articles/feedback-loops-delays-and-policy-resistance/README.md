# Feedback Loops, Delays, and Policy Resistance

This companion directory supports the article **"Feedback Loops, Delays, and Policy Resistance."**

The workflows operationalize feedback-aware policy design as a reproducible decision-science problem involving reinforcing feedback, balancing feedback, delayed response, stock-and-flow logic, resistance intensity, scenario performance, threshold review, monitoring triggers, and decision-record scaffolding.

## Core Claim

Well-intended decisions often fail because they enter systems that respond. Feedback loops can amplify or counteract interventions. Delays can cause false confidence, premature abandonment, and overcorrection. Policy resistance can weaken or reverse the intended effect when system structure, incentives, and adaptive behavior are ignored.

## Modeling Principles

1. Define the policy problem and target outcome.
2. Identify recurring patterns rather than isolated events.
3. Map stocks, flows, reinforcing loops, balancing loops, and delays.
4. Treat policy resistance as system response, not only implementation failure.
5. Compare policies across delayed feedback, resistance escalation, capacity constraint, and adaptive revision scenarios.
6. Track accumulated stocks, not only visible flows.
7. Monitor both direct outcomes and counter-responses.
8. Use thresholds to trigger review before resistance becomes failure.
9. Preserve decision records before hindsight rewrites the rationale.
10. Treat feedback-aware policy design as a learning process, not a one-time act of control.

## Quick Start

From this article directory:

```bash
python3 python/run_all_feedback_delay_workflows.py
Rscript r/run_all_feedback_delay_workflows.R
```

Outputs are written to:

```text
outputs/tables/
outputs/figures/
outputs/decision_records/
```
