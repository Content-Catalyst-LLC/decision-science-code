#!/usr/bin/env python3
"""Trade-off review queue helper."""

from __future__ import annotations


def review_flag(dominated_by_any: bool, best_rank_rate: float, rank_volatility: float, max_regret: float) -> str:
    if dominated_by_any or best_rank_rate < 0.25 or rank_volatility > 1.25 or max_regret > 0.20:
        return "review"
    return "acceptable"


if __name__ == "__main__":
    print(review_flag(False, 0.2, 0.8, 0.1))
    print(review_flag(False, 0.7, 0.5, 0.1))
