#!/usr/bin/env python3
"""AI decision-support oversight trigger helper."""

from __future__ import annotations


def review_required(
    model_uncertainty: float,
    human_oversight: float,
    automation_bias: float,
    contestability: float,
    fairness_risk: float,
    accountability: float,
    uncertainty_trigger: float = 0.62,
    oversight_trigger: float = 0.58,
    automation_bias_trigger: float = 0.62,
    contestability_trigger: float = 0.56,
    fairness_risk_trigger: float = 0.60,
    accountability_trigger: float = 0.58,
) -> bool:
    return (
        model_uncertainty >= uncertainty_trigger
        or human_oversight <= oversight_trigger
        or automation_bias >= automation_bias_trigger
        or contestability <= contestability_trigger
        or fairness_risk >= fairness_risk_trigger
        or accountability <= accountability_trigger
    )


if __name__ == "__main__":
    print(review_required(0.44, 0.72, 0.46, 0.66, 0.42, 0.70))
