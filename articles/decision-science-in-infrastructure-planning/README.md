# Decision Science in Infrastructure Planning

This companion directory supports the article **"Decision Science in Infrastructure Planning."**

The workflows operationalize infrastructure planning as a reproducible decision-science problem involving long-lived assets, scenario uncertainty, lifecycle cost, resilience, service continuity, public value, equity, environmental performance, adaptive pathways, governance review, and decision-record scaffolding.

## Core Claim

Infrastructure planning is not only an engineering, financing, or construction problem. It is structured public judgment under uncertainty because infrastructure decisions commit societies to physical pathways that can last for decades or centuries.

## Modeling Principles

1. Treat infrastructure projects as long-lived public decisions, not isolated capital expenditures.
2. Define the service need before naming a project.
3. Compare maintenance, retrofit, expansion, demand management, nature-based, modular, and adaptive options.
4. Evaluate lifecycle value, not only upfront capital cost.
5. Test alternatives across demand, climate, funding, technology, disruption, and governance scenarios.
6. Include equity, access, affordability, exposure, displacement, and public legitimacy.
7. Evaluate resilience through service continuity, criticality, redundancy, recovery, and adaptation.
8. Use adaptive pathways with monitoring indicators and trigger points.
9. Treat data, AI, models, and digital twins as decision-support tools requiring governance.
10. Preserve assumptions, alternatives, trade-offs, equity concerns, risks, and revision triggers in decision records.

## Quick Start

From this article directory:

```bash
python3 python/run_all_infrastructure_workflows.py
Rscript r/run_all_infrastructure_workflows.R
```

Outputs are written to:

```text
outputs/tables/
outputs/figures/
outputs/decision_records/
```
