#!/usr/bin/env python3
"""Variance and tail metric helpers."""

from __future__ import annotations

from statistics import mean, pstdev


def downside_frequency(values: list[float], threshold: float) -> float:
    return sum(1 for value in values if value <= threshold) / len(values)


if __name__ == "__main__":
    values = [0.04, 0.02, -0.03, 0.08, -0.12, 0.01]
    print(round(mean(values), 6))
    print(round(pstdev(values), 6))
    print(round(downside_frequency(values, -0.05), 6))
