#!/usr/bin/env python3
"""Minimax regret diagnostics."""

from __future__ import annotations


def minimax_regret(payoff_matrix: dict[str, list[float]]) -> tuple[str, dict[str, float]]:
    n = len(next(iter(payoff_matrix.values())))
    best_by_state = [max(payoff_matrix[name][i] for name in payoff_matrix) for i in range(n)]
    max_regret = {}
    for name, payoffs in payoff_matrix.items():
        regrets = [best_by_state[i] - payoffs[i] for i in range(n)]
        max_regret[name] = max(regrets)
    return min(max_regret, key=max_regret.get), max_regret


if __name__ == "__main__":
    matrix = {
        "Optimize": [145, 92, 30, -95, -40],
        "Balanced": [112, 84, 58, 12, 30],
        "Robust": [78, 72, 65, 48, 55],
        "Adaptive": [98, 80, 62, 38, 68],
        "Staged Pilot": [82, 70, 60, 42, 74],
    }
    selected, regrets = minimax_regret(matrix)
    print("Maximum regret:", regrets)
    print("Selected:", selected)
