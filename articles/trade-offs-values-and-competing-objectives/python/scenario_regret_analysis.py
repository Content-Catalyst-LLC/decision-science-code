#!/usr/bin/env python3
"""Scenario regret helper."""

from __future__ import annotations


def regret(score: float, best_score: float) -> float:
    return best_score - score


if __name__ == "__main__":
    print(round(regret(0.72, 0.91), 6))
