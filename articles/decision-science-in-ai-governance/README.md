# Decision Science in AI Governance

This companion directory supports the article **"Decision Science in AI Governance."**

The workflows operationalize AI governance as a reproducible decision-science problem involving use-case classification, risk tiering, evidence thresholds, human oversight, fairness and distributional impact, transparency, vendor risk, drift monitoring, incident escalation, adaptive safeguards, and decision-record scaffolding.

## Core Claim

AI governance is not only a compliance problem, a technical risk problem, an ethics problem, or a policy problem. It is a decision-science problem: how should institutions decide which AI systems to build, buy, deploy, restrict, monitor, audit, scale, or reject when impacts are uncertain, incentives are uneven, evidence is incomplete, and harms may emerge after deployment?

## Modeling Principles

1. Treat AI governance as a decision system, not only a policy document.
2. Evaluate AI use cases in context rather than evaluating the model alone.
3. Classify risk by stakes, reversibility, affected population, autonomy, opacity, scale, and institutional capacity.
4. Match evidence thresholds to risk level and decision consequence.
5. Design human oversight with authority, information, time, expertise, independence, and accountability.
6. Evaluate distributional impact, subgroup performance, fairness trade-offs, and contestability.
7. Govern vendors, model updates, data terms, audit rights, and exit options.
8. Monitor drift, incidents, misuse, complaints, equity performance, and security events after deployment.
9. Use adaptive safeguards when monitoring indicators cross thresholds.
10. Preserve assumptions, alternatives, evidence, risk classification, approvals, safeguards, dissent, and revision triggers in decision records.

## Quick Start

From this article directory:

```bash
python3 python/run_all_ai_governance_workflows.py
Rscript r/run_all_ai_governance_workflows.R
```

Outputs are written to:

```text
outputs/tables/
outputs/figures/
outputs/decision_records/
```
