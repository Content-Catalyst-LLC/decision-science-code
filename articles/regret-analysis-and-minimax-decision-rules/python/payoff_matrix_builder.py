#!/usr/bin/env python3
"""Payoff matrix helper."""

from __future__ import annotations


def validate_payoff_matrix(rows: list[dict[str, float]], scenarios: list[str]) -> bool:
    return all(all(scenario in row for scenario in scenarios) for row in rows)


if __name__ == "__main__":
    rows = [{"a": 0.1, "b": 0.2}, {"a": 0.3, "b": 0.4}]
    print(validate_payoff_matrix(rows, ["a", "b"]))
