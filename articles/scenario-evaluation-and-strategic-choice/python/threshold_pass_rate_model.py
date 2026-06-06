#!/usr/bin/env python3
"""Threshold pass rate helper."""

from __future__ import annotations


def threshold_pass_rate(values: list[float], threshold: float) -> float:
    if not values:
        raise ValueError("At least one value is required.")
    return sum(1 for value in values if value >= threshold) / len(values)


if __name__ == "__main__":
    print(round(threshold_pass_rate([0.78, 0.76, 0.82, 0.80], 0.70), 6))
