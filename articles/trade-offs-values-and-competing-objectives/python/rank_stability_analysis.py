#!/usr/bin/env python3
"""Rank stability helper."""

from __future__ import annotations

from statistics import mean, stdev


def rank_stability(ranks: list[int]) -> dict[str, float]:
    if not ranks:
        raise ValueError("At least one rank is required.")
    return {
        "average_rank": mean(ranks),
        "best_rank_rate": sum(1 for rank in ranks if rank == 1) / len(ranks),
        "top_two_rate": sum(1 for rank in ranks if rank <= 2) / len(ranks),
        "rank_volatility": stdev(ranks) if len(ranks) > 1 else 0.0,
    }


if __name__ == "__main__":
    result = rank_stability([1, 1, 2, 3, 1, 2])
    print({key: round(value, 6) for key, value in result.items()})
