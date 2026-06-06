#!/usr/bin/env python3
"""Procedural legitimacy helper."""

from __future__ import annotations


def procedural_score(values: dict[str, float], weights: dict[str, float]) -> float:
    return sum(values[key] * weights[key] for key in weights)


if __name__ == "__main__":
    values = {"voice": 0.92, "transparency": 0.90, "explanation": 0.88, "contestability": 0.86, "review": 0.90}
    weights = {"voice": 0.24, "transparency": 0.20, "explanation": 0.20, "contestability": 0.18, "review": 0.18}
    print(round(procedural_score(values, weights), 6))
