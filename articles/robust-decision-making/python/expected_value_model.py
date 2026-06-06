#!/usr/bin/env python3
from __future__ import annotations

def expected_value(values: list[float], weights: list[float]) -> float:
    if len(values) != len(weights):
        raise ValueError("Values and weights must have the same length.")
    if abs(sum(weights) - 1.0) > 1e-9:
        raise ValueError("Weights must sum to 1.")
    return sum(value * weight for value, weight in zip(values, weights))

if __name__ == "__main__":
    print(round(expected_value([0.9, 0.4, 0.2], [0.3, 0.3, 0.4]), 6))
