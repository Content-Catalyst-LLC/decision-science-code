#!/usr/bin/env python3
"""Capability and governance fit helper."""

from __future__ import annotations


def strategic_fit_score(capability_fit: float, governance_feasibility: float, adaptability: float) -> float:
    return 0.40 * capability_fit + 0.32 * governance_feasibility + 0.28 * adaptability


def requires_fit_review(capability_fit: float, governance_feasibility: float, threshold: float = 0.55) -> bool:
    return capability_fit < threshold or governance_feasibility < threshold


if __name__ == "__main__":
    print(round(strategic_fit_score(0.72, 0.70, 0.84), 6))
    print(requires_fit_review(0.44, 0.46))
