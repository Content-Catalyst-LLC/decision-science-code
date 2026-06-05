#!/usr/bin/env python3
"""Expected utility model inspired by Bernoulli-style subjective value."""

from __future__ import annotations

import math


def utility(value: float, risk_aversion: float = 0.016) -> float:
    return 1.0 - math.exp(-risk_aversion * value)


def expected_utility(payoffs: list[float], probabilities: list[float]) -> float:
    return sum(utility(x) * p for x, p in zip(payoffs, probabilities))


if __name__ == "__main__":
    probabilities = [0.42, 0.28, 0.18, 0.12]
    print(expected_utility([92, 68, 18, 42], probabilities))
