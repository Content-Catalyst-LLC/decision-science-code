#!/usr/bin/env python3
"""Robustness helper for strategic options."""

from __future__ import annotations


def robust_strategy_score(expected_value: float, downside_robustness: float, adaptability: float, reversibility: float) -> float:
    return (
        0.36 * expected_value / 100.0
        + 0.30 * downside_robustness / 100.0
        + 0.20 * adaptability
        + 0.14 * reversibility
    )


if __name__ == "__main__":
    print(round(robust_strategy_score(76.7, 66.0, 0.84, 0.82), 6))
