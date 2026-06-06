#!/usr/bin/env python3
"""Search-cost diagnostic helper."""

from __future__ import annotations


def net_value(utility: float, search_order: int, search_cost_per_option: float) -> float:
    return utility - search_order * search_cost_per_option


def continue_search(expected_improvement: float, marginal_search_cost: float) -> bool:
    return expected_improvement > marginal_search_cost


if __name__ == "__main__":
    print(round(net_value(0.82, 3, 0.04), 6))
    print(continue_search(0.05, 0.03))
