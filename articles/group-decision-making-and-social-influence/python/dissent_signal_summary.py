#!/usr/bin/env python3
"""Dissent signal helper."""

from __future__ import annotations

from statistics import mean


def dissent_ratio(estimates: list[float], threshold: float = 0.12) -> float:
    if not estimates:
        raise ValueError("At least one estimate is required.")
    group_estimate = mean(estimates)
    return sum(1 for estimate in estimates if abs(estimate - group_estimate) > threshold) / len(estimates)


if __name__ == "__main__":
    print(round(dissent_ratio([0.66, 0.55, 0.68, 0.50, 0.63, 0.59, 0.70]), 6))
