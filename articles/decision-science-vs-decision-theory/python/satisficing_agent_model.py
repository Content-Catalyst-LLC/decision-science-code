#!/usr/bin/env python3
"""Satisficing agent scaffold for bounded rationality."""

from __future__ import annotations


def satisficing_choice(candidates: list[tuple[str, float]], threshold: float) -> str:
    for name, value in candidates:
        if value >= threshold:
            return name
    return candidates[-1][0]


if __name__ == "__main__":
    search_order = [
        ("Staged Pilot", 52),
        ("Balanced", 48),
        ("Robust", 57),
        ("Optimize", 62),
    ]
    print(satisficing_choice(search_order, threshold=55))
