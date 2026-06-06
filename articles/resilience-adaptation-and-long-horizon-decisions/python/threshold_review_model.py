#!/usr/bin/env python3
"""Threshold review helper."""

from __future__ import annotations


def threshold_breach_rate(values: list[float], failure_threshold: float) -> float:
    if not values:
        raise ValueError("At least one value is required.")
    return sum(1 for value in values if value <= failure_threshold) / len(values)


if __name__ == "__main__":
    print(round(threshold_breach_rate([100, 92, 80, 64, 75], 65), 6))
