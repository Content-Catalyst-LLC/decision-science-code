#!/usr/bin/env python3
"""Ecological threshold review helper."""

from __future__ import annotations


def threshold_breach(resource_stock: float, threshold: float = 35.0) -> bool:
    return resource_stock < threshold


def strategy_requires_review(social_equity: float, resilience_score: float, threshold_protection: float, cost_burden: float) -> bool:
    return social_equity < 0.50 or resilience_score < 0.50 or threshold_protection < 0.55 or cost_burden > 0.70


if __name__ == "__main__":
    print(threshold_breach(34.0))
    print(strategy_requires_review(0.46, 0.51, 0.48, 0.34))
