#!/usr/bin/env python3
"""Portfolio loss helper for financial risk decision science."""

from __future__ import annotations


def expected_loss(losses: dict[str, float], probabilities: dict[str, float]) -> float:
    return sum(losses[name] * probabilities[name] for name in losses)


def worst_case_loss(losses: dict[str, float]) -> float:
    return min(losses.values())


if __name__ == "__main__":
    losses = {"normal": -1.2, "recession": -4.8, "liquidity_shock": -3.6, "systemic_stress": -6.2}
    probs = {"normal": 0.55, "recession": 0.20, "liquidity_shock": 0.15, "systemic_stress": 0.10}
    print(round(expected_loss(losses, probs), 6))
    print(round(worst_case_loss(losses), 6))
