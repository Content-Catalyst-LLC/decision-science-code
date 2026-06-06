#!/usr/bin/env python3
"""AI reliance helper for future decision science."""

from __future__ import annotations


def ai_reliance_weight(
    model_validity: float,
    calibration: float,
    human_oversight: float,
    decision_risk: float,
    model_uncertainty: float,
) -> float:
    weight = (
        0.28 * model_validity
        + 0.24 * calibration
        + 0.22 * human_oversight
        - 0.14 * decision_risk
        - 0.12 * model_uncertainty
    )
    return max(0.0, min(1.0, weight))


if __name__ == "__main__":
    print(round(ai_reliance_weight(0.82, 0.78, 0.86, 0.54, 0.36), 6))
