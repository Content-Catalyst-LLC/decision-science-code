#!/usr/bin/env python3
"""Delayed response helper."""

from __future__ import annotations


def delayed_value(history: list[float], delay: int) -> float:
    if not history:
        raise ValueError("History must contain at least one value.")
    index = max(0, len(history) - delay)
    return history[index]


if __name__ == "__main__":
    print(round(delayed_value([8.0, 8.6, 9.1, 9.5, 9.7], 4), 6))
