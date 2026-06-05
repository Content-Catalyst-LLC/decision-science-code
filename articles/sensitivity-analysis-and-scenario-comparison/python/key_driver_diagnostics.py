#!/usr/bin/env python3
"""Key-driver diagnostic helper."""

from __future__ import annotations


def driver_flag(score_range: float, winner_count: int) -> str:
    if winner_count > 1 or score_range > 25:
        return "high"
    if score_range > 12:
        return "medium"
    return "stable"


if __name__ == "__main__":
    print(driver_flag(30.5, 2))
    print(driver_flag(8.0, 1))
