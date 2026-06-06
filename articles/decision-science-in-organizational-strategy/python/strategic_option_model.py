#!/usr/bin/env python3
"""Strategic option value helper."""

from __future__ import annotations


def expected_value(values: dict[str, float], probabilities: dict[str, float]) -> float:
    return sum(values[name] * probabilities[name] for name in values)


def downside_robustness(values: dict[str, float]) -> float:
    return min(values.values())


if __name__ == "__main__":
    values = {"low_growth": 68.0, "base_case": 82.0, "high_growth": 89.0, "disruption": 66.0}
    probabilities = {"low_growth": 0.25, "base_case": 0.35, "high_growth": 0.20, "disruption": 0.20}
    print(round(expected_value(values, probabilities), 6))
    print(round(downside_robustness(values), 6))
