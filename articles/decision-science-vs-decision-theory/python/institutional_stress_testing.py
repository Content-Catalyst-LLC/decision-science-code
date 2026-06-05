#!/usr/bin/env python3
"""Institutional stress testing scaffold."""

from __future__ import annotations


def stress_adjusted_score(payoff: float, implementation_capacity: float, legitimacy: float, friction: float) -> float:
    return payoff - friction * (1.0 - implementation_capacity) * 50.0 - friction * (1.0 - legitimacy) * 35.0


if __name__ == "__main__":
    print(stress_adjusted_score(80, implementation_capacity=0.70, legitimacy=0.60, friction=0.50))
