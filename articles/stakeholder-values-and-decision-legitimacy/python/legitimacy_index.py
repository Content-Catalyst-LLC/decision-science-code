#!/usr/bin/env python3
"""Decision legitimacy index helper."""

from __future__ import annotations


def legitimacy_index(aggregate_score: float, procedural_score: float, pass_rate: float, min_score: float, max_burden: float) -> float:
    return 0.40 * aggregate_score + 0.24 * procedural_score + 0.18 * pass_rate + 0.10 * min_score - 0.08 * max_burden


if __name__ == "__main__":
    print(round(legitimacy_index(0.82, 0.89, 1.0, 0.76, 0.26), 6))
