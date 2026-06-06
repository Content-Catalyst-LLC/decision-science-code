#!/usr/bin/env python3
"""Expected value helper."""

from __future__ import annotations


def expected_value(values: list[float], probabilities: list[float]) -> float:
    if len(values) != len(probabilities):
        raise ValueError("Values and probabilities must have the same length.")
    if abs(sum(probabilities) - 1.0) > 1e-9:
        raise ValueError("Probabilities must sum to 1.")
    return sum(value * probability for value, probability in zip(values, probabilities))


if __name__ == "__main__":
    print(round(expected_value([82, 28, 40, 76], [0.35, 0.25, 0.20, 0.20]), 6))
