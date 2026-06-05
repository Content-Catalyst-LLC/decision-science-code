#!/usr/bin/env python3
"""Minimax regret historical paradigm example."""

from __future__ import annotations


def minimax_regret(payoff_matrix: dict[str, list[float]]) -> tuple[str, dict[str, float]]:
    scenario_count = len(next(iter(payoff_matrix.values())))
    best_by_scenario = [max(payoff_matrix[name][i] for name in payoff_matrix) for i in range(scenario_count)]
    max_regrets = {}
    for name, payoffs in payoff_matrix.items():
        max_regrets[name] = max(best_by_scenario[i] - payoffs[i] for i in range(scenario_count))
    return min(max_regrets, key=max_regrets.get), max_regrets


if __name__ == "__main__":
    matrix = {
        "Aggressive": [128, 50, -90, -20],
        "Balanced": [92, 68, 18, 42],
        "Defensive": [62, 58, 44, 54],
        "Adaptive": [88, 70, 36, 72],
    }
    print(minimax_regret(matrix))
