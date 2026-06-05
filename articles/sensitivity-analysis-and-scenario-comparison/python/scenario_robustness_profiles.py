#!/usr/bin/env python3
"""Scenario robustness profile helper."""

from __future__ import annotations


def robustness_score(average: float, minimum: float, worst: float, max_regret: float, volatility: float) -> float:
    return 0.35 * average + 0.30 * minimum + 0.20 * worst - 0.10 * max_regret - 0.05 * volatility


if __name__ == "__main__":
    print(round(robustness_score(75.0, 62.0, 49.0, 14.0, 8.5), 6))
