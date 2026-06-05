#!/usr/bin/env python3
"""Value at Risk and Conditional Value at Risk helpers."""

from __future__ import annotations

from statistics import mean


def quantile(values: list[float], probability: float) -> float:
    sorted_values = sorted(values)
    index = int(probability * (len(sorted_values) - 1))
    return sorted_values[index]


def cvar(values: list[float], probability: float) -> float:
    var_value = quantile(values, probability)
    tail = [value for value in values if value <= var_value]
    return mean(tail)


if __name__ == "__main__":
    sample = [0.04, 0.02, -0.03, 0.08, -0.12, 0.01, -0.20, 0.06]
    print(round(quantile(sample, 0.05), 6))
    print(round(cvar(sample, 0.05), 6))
