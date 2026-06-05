#!/usr/bin/env python3
"""Robustness threshold analysis."""

from __future__ import annotations


def robustness_share(values: list[float], threshold: float) -> float:
    return sum(1 for value in values if value >= threshold) / len(values)


if __name__ == "__main__":
    print(robustness_share([0.82, 0.76, 0.91, 0.68, 0.88], 0.75))
