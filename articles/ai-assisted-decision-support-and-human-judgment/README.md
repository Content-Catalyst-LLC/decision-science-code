# AI-Assisted Decision Support and Human Judgment

This companion directory supports the article **"AI-Assisted Decision Support and Human Judgment."**

The workflows operationalize AI-assisted decision support as a reproducible decision-science problem involving model confidence, uncertainty, human oversight, automation-bias risk, contestability, fairness review, accountability, monitoring, decision records, and review-trigger scaffolding.

## Core Claim

AI should support decision quality, not replace accountable judgment. Responsible AI-assisted decision support requires clear use cases, risk classification, evidence standards, human oversight, uncertainty communication, model validation, stakeholder review, contestability, monitoring, decision records, and governance authority.

## Modeling Principles

1. Define the decision before selecting the AI tool.
2. Distinguish AI evidence support, analytic support, recommendation, triage, monitoring, and automation.
3. Match governance strength to use-case risk, consequence severity, reversibility, uncertainty, and contestability.
4. Treat human oversight as a designed role with authority, time, training, evidence access, and override power.
5. Make model uncertainty, missing data, distribution shift, calibration limits, and context mismatch visible.
6. Monitor automation bias, overreliance, override patterns, and reviewer behavior.
7. Evaluate fairness, subgroup performance, exclusion risk, appeal pathways, and distributional effects.
8. Preserve records of model version, data, output, human review, final decision, and rationale.
9. Define review triggers for uncertainty, weak oversight, automation bias, fairness risk, accountability weakness, and contestability gaps.
10. Maintain corrective authority to revise, restrict, suspend, retrain, replace, or retire AI-supported decision systems.

## Quick Start

From this article directory:

```bash
python3 python/run_all_ai_decision_support_workflows.py
Rscript r/run_all_ai_decision_support_workflows.R
```

Outputs are written to:

```text
outputs/tables/
outputs/figures/
outputs/decision_records/
```
