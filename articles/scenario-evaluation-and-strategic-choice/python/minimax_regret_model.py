#!/usr/bin/env python3
"""Minimax regret helper for scenario evaluation."""

from __future__ import annotations


def maximum_regret(strategy_values: list[float], scenario_best_values: list[float]) -> float:
    if len(strategy_values) != len(scenario_best_values):
        raise ValueError("Strategy and best-scenario lists must have the same length.")
    regrets = [best - value for value, best in zip(strategy_values, scenario_best_values)]
    return max(regrets)


if __name__ == "__main__":
    print(round(maximum_regret([0.76, 0.71, 0.63], [0.92, 0.76, 0.82]), 6))
