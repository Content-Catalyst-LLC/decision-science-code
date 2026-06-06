#!/usr/bin/env python3
"""Decision-rule comparison helper."""

from __future__ import annotations


def combined_robustness_score(maximin_value: float, maximum_regret: float, pass_rate: float, expected_value: float, performance_range: float) -> float:
    return (
        0.25 * maximin_value
        + 0.25 * (1 - maximum_regret)
        + 0.25 * pass_rate
        + 0.15 * expected_value
        + 0.10 * (1 - performance_range)
    )


if __name__ == "__main__":
    print(round(combined_robustness_score(0.73, 0.19, 1.0, 0.79, 0.15), 6))
