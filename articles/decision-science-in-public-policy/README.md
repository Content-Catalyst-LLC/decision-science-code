# Decision Science in Public Policy

This companion directory supports the article **"Decision Science in Public Policy."**

The workflows operationalize public policy decision science as a reproducible decision-science problem involving policy package comparison, multi-objective analysis, evidence and uncertainty, equity review, legitimacy, implementation capacity, scenario robustness, policy uptake, public trust, implementation drift, adaptive review, and decision-record scaffolding.

## Core Claim

Public policy decision science is not only about choosing among technical options. It is about building defensible architectures of collective judgment in settings where evidence is incomplete, goals conflict, power is unevenly distributed, values are contested, and implementation occurs through real institutions rather than abstract models alone.

## Modeling Principles

1. Treat public policy as collective judgment under uncertainty.
2. Make policy objectives and value conflicts explicit.
3. Separate evidence from judgment and empirical claims from normative choices.
4. Evaluate efficiency, equity, resilience, feasibility, legitimacy, and implementation capacity together.
5. Test policies across plausible futures and implementation stress.
6. Include behavioral response, administrative burden, and public trust.
7. Analyze feedback loops, delays, interdependence, and policy resistance.
8. Connect policy design to implementation architecture and institutional capacity.
9. Use monitoring, trigger points, and adaptive review for long-horizon policy.
10. Preserve assumptions, alternatives, trade-offs, dissent, stakeholder concerns, and revision triggers in decision records.

## Quick Start

From this article directory:

```bash
python3 python/run_all_public_policy_workflows.py
Rscript r/run_all_public_policy_workflows.R
```

Outputs are written to:

```text
outputs/tables/
outputs/figures/
outputs/decision_records/
```
