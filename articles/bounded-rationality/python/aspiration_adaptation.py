#!/usr/bin/env python3
"""Adaptive aspiration helper."""

from __future__ import annotations


def update_aspiration(current: float, feedback: float, learning_rate: float = 0.12) -> float:
    return max(0.35, min(0.95, current + learning_rate * (feedback - current)))


if __name__ == "__main__":
    aspiration = 0.70
    for feedback in [0.74, 0.68, 0.76]:
        aspiration = update_aspiration(aspiration, feedback)
        print(round(aspiration, 6))
