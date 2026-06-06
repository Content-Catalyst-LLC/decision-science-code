#!/usr/bin/env python3
"""Cost-effectiveness helper."""

from __future__ import annotations


def icer(cost_1: float, cost_0: float, outcome_1: float, outcome_0: float) -> float:
    delta_outcome = outcome_1 - outcome_0
    if delta_outcome == 0:
        raise ValueError("Incremental outcome is zero; ICER is undefined.")
    return (cost_1 - cost_0) / delta_outcome


if __name__ == "__main__":
    print(round(icer(cost_1=12000, cost_0=8000, outcome_1=3.4, outcome_0=3.0), 6))
