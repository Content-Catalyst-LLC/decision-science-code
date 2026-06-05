#!/usr/bin/env python3
"""Small risk-aversion sensitivity check."""

from __future__ import annotations

import math


def crra_utility(x: float, rho: float, offset: float = 151.0) -> float:
    z = x + offset
    if abs(rho - 1.0) < 1e-9:
        return math.log(z)
    return (z ** (1.0 - rho) - 1.0) / (1.0 - rho)


def expected_utility(outcomes: list[float], probabilities: list[float], rho: float) -> float:
    return sum(p * crra_utility(x, rho) for x, p in zip(outcomes, probabilities))


if __name__ == "__main__":
    for rho in [0.25, 0.75, 1.0, 1.5, 2.25]:
        print(rho, round(expected_utility([180, 40], [0.6, 0.4], rho), 6))
