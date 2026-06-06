#!/usr/bin/env python3
"""Sustainability value score helper."""

from __future__ import annotations


def sustainability_value_score(
    emissions_reduction: float,
    social_equity: float,
    cost_burden: float,
    resilience_score: float,
    implementation_feasibility: float,
    threshold_protection: float,
) -> float:
    return (
        0.22 * emissions_reduction
        + 0.20 * social_equity
        - 0.12 * cost_burden
        + 0.18 * resilience_score
        + 0.12 * implementation_feasibility
        + 0.16 * threshold_protection
    )


if __name__ == "__main__":
    print(round(sustainability_value_score(0.61, 0.74, 0.49, 0.82, 0.66, 0.82), 6))
