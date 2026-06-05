#!/usr/bin/env python3
"""Expected value and expected utility helper functions."""

from __future__ import annotations

import math


def expected_value(outcomes: list[float], probabilities: list[float]) -> float:
    if len(outcomes) != len(probabilities):
        raise ValueError("outcomes and probabilities must have the same length")
    if not math.isclose(sum(probabilities), 1.0, abs_tol=1e-8):
        raise ValueError("probabilities must sum to 1")
    return sum(value * probability for value, probability in zip(outcomes, probabilities))


def exponential_utility(value: float, risk_aversion: float = 0.018) -> float:
    return 1.0 - math.exp(-risk_aversion * value)


def expected_utility(outcomes: list[float], probabilities: list[float], risk_aversion: float = 0.018) -> float:
    return expected_value([exponential_utility(value, risk_aversion) for value in outcomes], probabilities)


if __name__ == "__main__":
    outcomes = [100, 40, -25]
    probabilities = [0.45, 0.35, 0.20]
    print("Expected value:", round(expected_value(outcomes, probabilities), 4))
    print("Expected utility:", round(expected_utility(outcomes, probabilities), 6))
