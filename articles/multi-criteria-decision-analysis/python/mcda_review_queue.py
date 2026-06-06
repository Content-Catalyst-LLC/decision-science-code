#!/usr/bin/env python3
"""MCDA review queue helper."""

from __future__ import annotations


def review_flag(best_rank_rate: float, rank_volatility: float, score_gap_from_leader: float) -> str:
    if best_rank_rate < 0.25 or rank_volatility > 1.25 or score_gap_from_leader < 0.03:
        return "review"
    return "acceptable"


if __name__ == "__main__":
    print(review_flag(0.20, 0.8, 0.05))
    print(review_flag(0.60, 0.5, 0.08))
