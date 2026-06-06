#!/usr/bin/env python3
"""Adaptive pathway score helper."""

from __future__ import annotations


def pathway_score(initial_performance: float, flexibility: float, monitoring_quality: float, trigger_clarity: float, switching_cost: float, fallback_strength: float) -> float:
    return (
        0.20 * initial_performance
        + 0.18 * flexibility
        + 0.16 * monitoring_quality
        + 0.16 * trigger_clarity
        - 0.12 * switching_cost
        + 0.18 * fallback_strength
    )


if __name__ == "__main__":
    print(round(pathway_score(0.76, 0.88, 0.82, 0.80, 0.38, 0.84), 6))
