# Decision Science vs. Decision Theory

This companion directory supports the article **"Decision Science vs. Decision Theory."**

The workflows compare formal decision-theoretic criteria with applied decision-science diagnostics. They show how expected utility, Bayesian updating, loss functions, regret, and formal rational choice can be extended with bounded rationality, satisficing, robustness, scenario comparison, institutional stress testing, evidence quality, legitimacy, and accountable decision records.

## Core Distinction

- **Decision theory** clarifies rational choice under formal assumptions: actions, states, outcomes, probabilities, utilities, loss functions, and coherent preferences.
- **Decision science** embeds those formal tools inside real decision environments: incomplete evidence, cognitive limits, organizational incentives, contested values, implementation constraints, and deep uncertainty.

## Modeling Principles

1. Use expected utility when probabilities and utilities are defensible.
2. Use Bayesian updating when evidence changes beliefs.
3. Use loss functions when decisions depend on asymmetric error costs.
4. Use regret and robustness when futures are uncertain or contested.
5. Use satisficing models when bounded rationality and search constraints matter.
6. Evaluate implementation capacity, evidence quality, and legitimacy alongside formal payoff.
7. Treat computational models as supports for judgment, not replacements for responsibility.
8. Preserve decision records so formal assumptions and applied judgments remain reviewable.

## Quick Start

From this article directory:

```bash
python3 python/run_all_decision_theory_science_workflows.py
Rscript r/run_all_decision_theory_science_workflows.R
```

Outputs are written to:

```text
outputs/tables/
outputs/figures/
outputs/decision_records/
```
