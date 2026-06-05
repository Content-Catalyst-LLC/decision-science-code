#!/usr/bin/env python3
"""Regret analysis and minimax decision rule."""

from __future__ import annotations


def regret_matrix(payoff_matrix: dict[str, dict[str, float]]) -> dict[str, dict[str, float]]:
    scenarios = list(next(iter(payoff_matrix.values())).keys())
    output: dict[str, dict[str, float]] = {}

    for alternative, payoffs in payoff_matrix.items():
        output[alternative] = {}
        for scenario in scenarios:
            best = max(payoff_matrix[alt][scenario] for alt in payoff_matrix)
            output[alternative][scenario] = best - payoffs[scenario]

    return output


def minimax_regret(payoff_matrix: dict[str, dict[str, float]]) -> tuple[str, dict[str, float]]:
    regrets = regret_matrix(payoff_matrix)
    max_regrets = {
        alternative: max(values.values())
        for alternative, values in regrets.items()
    }
    selected = min(max_regrets, key=max_regrets.get)
    return selected, max_regrets


if __name__ == "__main__":
    matrix = {
        "Optimize": {"baseline": 120, "adverse": 20, "shock": -80},
        "Hedge": {"baseline": 88, "adverse": 62, "shock": 15},
        "Preserve option": {"baseline": 64, "adverse": 55, "shock": 38},
    }
    selected_strategy, regrets = minimax_regret(matrix)
    print("Maximum regrets:", regrets)
    print("Selected by minimax regret:", selected_strategy)
