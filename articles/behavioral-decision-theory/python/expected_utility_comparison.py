#!/usr/bin/env python3
"""Expected value and expected utility helpers."""

from __future__ import annotations

import math


def utility(x: float) -> float:
    return math.copysign(math.sqrt(abs(x)), x)


def expected_value(outcomes: list[float], probabilities: list[float]) -> float:
    if len(outcomes) != len(probabilities):
        raise ValueError("Outcomes and probabilities must have the same length.")
    return sum(x * p for x, p in zip(outcomes, probabilities))


def expected_utility(outcomes: list[float], probabilities: list[float]) -> float:
    if len(outcomes) != len(probabilities):
        raise ValueError("Outcomes and probabilities must have the same length.")
    return sum(utility(x) * p for x, p in zip(outcomes, probabilities))


if __name__ == "__main__":
    print(round(expected_value([120, -40], [0.60, 0.40]), 6))
    print(round(expected_utility([120, -40], [0.60, 0.40]), 6))
