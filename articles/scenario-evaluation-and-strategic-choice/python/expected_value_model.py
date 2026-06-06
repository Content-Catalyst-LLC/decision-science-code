#!/usr/bin/env python3
"""Expected value helper for scenario evaluation."""

from __future__ import annotations


def expected_value(values: list[float], probabilities: list[float]) -> float:
    if len(values) != len(probabilities):
        raise ValueError("Values and probabilities must have the same length.")
    return sum(value * probability for value, probability in zip(values, probabilities))


if __name__ == "__main__":
    print(round(expected_value([0.78, 0.76, 0.82], [0.30, 0.40, 0.30]), 6))
