#!/usr/bin/env python3
"""Bounded rationality and satisficing example."""

from __future__ import annotations


def satisficing_choice(candidates: list[tuple[str, float]], threshold: float) -> str:
    for name, value in candidates:
        if value >= threshold:
            return name
    return candidates[-1][0]


if __name__ == "__main__":
    candidates = [("Aggressive", -90), ("Balanced", 18), ("Adaptive", 36), ("Defensive", 44)]
    print(satisficing_choice(candidates, threshold=40))
