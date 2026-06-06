#!/usr/bin/env python3
"""Threshold compliance helper."""

from __future__ import annotations


def threshold_pass_rate(values: list[float], threshold: float) -> float:
    if not values:
        raise ValueError("At least one value is required.")
    return sum(1 for value in values if value >= threshold) / len(values)


if __name__ == "__main__":
    print(round(threshold_pass_rate([0.72, 0.66, 0.81], 0.70), 6))
