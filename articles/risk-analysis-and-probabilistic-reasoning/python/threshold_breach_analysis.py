#!/usr/bin/env python3
"""Threshold breach analysis."""

from __future__ import annotations


def breach_probability(values: list[float], threshold: float) -> float:
    if not values:
        return 0.0
    return sum(1 for value in values if value <= threshold) / len(values)


if __name__ == "__main__":
    print(round(breach_probability([0.05, -0.02, -0.11, 0.03, -0.14], -0.10), 6))
