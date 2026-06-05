#!/usr/bin/env python3
"""Posterior expected utility helper."""

from __future__ import annotations


def posterior_expected_utility(posterior: float, utility_true: float, utility_false: float) -> float:
    return posterior * utility_true + (1.0 - posterior) * utility_false


if __name__ == "__main__":
    posterior = 0.443299
    print(round(posterior_expected_utility(posterior, 90, -25), 6))
