#!/usr/bin/env python3
"""Adaptive review trigger helper."""

from __future__ import annotations


def review_required(
    governance: float,
    uncertainty: float,
    ethics: float,
    adaptive_capacity: float,
    failure_risk: float,
    governance_trigger: float = 0.58,
    uncertainty_trigger: float = 0.58,
    ethics_trigger: float = 0.58,
    adaptive_trigger: float = 0.58,
    failure_risk_trigger: float = 0.62,
) -> bool:
    return (
        governance <= governance_trigger
        or uncertainty <= uncertainty_trigger
        or ethics <= ethics_trigger
        or adaptive_capacity <= adaptive_trigger
        or failure_risk >= failure_risk_trigger
    )


if __name__ == "__main__":
    print(review_required(0.54, 0.62, 0.50, 0.54, 0.56))
