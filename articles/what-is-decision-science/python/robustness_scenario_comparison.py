#!/usr/bin/env python3
"""Robustness diagnostics across scenarios."""

from __future__ import annotations


def robustness_share(payoffs: list[float], threshold: float) -> float:
    if not payoffs:
        raise ValueError("payoffs cannot be empty")
    return sum(1 for payoff in payoffs if payoff >= threshold) / len(payoffs)


def main() -> None:
    alternatives = {
        "Optimize": [120, 20, -80, 40],
        "Hedge": [88, 62, 15, 55],
        "Preserve option": [64, 55, 38, 58],
    }

    for alternative, payoffs in alternatives.items():
        print(alternative, round(robustness_share(payoffs, threshold=35), 3))


if __name__ == "__main__":
    main()
