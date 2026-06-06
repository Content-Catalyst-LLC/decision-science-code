#!/usr/bin/env python3
"""Stopping-rule helper for bounded rationality."""

from __future__ import annotations


def stopping_rule_label(
    satisfies_aspiration: bool,
    deadline_reached: bool,
    expected_improvement: float,
    marginal_search_cost: float,
) -> str:
    if satisfies_aspiration:
        return "first_acceptable"
    if deadline_reached:
        return "deadline"
    if expected_improvement <= marginal_search_cost:
        return "marginal_value"
    return "continue_search"


if __name__ == "__main__":
    print(stopping_rule_label(False, False, 0.02, 0.03))
