#!/usr/bin/env python3
"""Minimax regret under uncertainty."""

from __future__ import annotations


def minimax_regret(payoff_matrix: dict[str, list[float]]) -> tuple[str, dict[str, float]]:
    n = len(next(iter(payoff_matrix.values())))
    best_by_state = [max(payoff_matrix[name][i] for name in payoff_matrix) for i in range(n)]
    max_regret = {}
    for name, values in payoff_matrix.items():
        regrets = [best_by_state[i] - values[i] for i in range(n)]
        max_regret[name] = max(regrets)
    return min(max_regret, key=max_regret.get), max_regret


if __name__ == "__main__":
    matrix = {
        "Expand": [120, 45, -95, -130, 20],
        "Hedge": [92, 68, 18, -20, 55],
        "Preserve Option": [72, 62, 42, 18, 70],
        "Adaptive Pathway": [95, 72, 34, 10, 78],
    }
    selected, regrets = minimax_regret(matrix)
    print(regrets)
    print("Selected:", selected)
