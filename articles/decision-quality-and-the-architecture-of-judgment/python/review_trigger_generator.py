#!/usr/bin/env python3
"""Review trigger generator."""

from __future__ import annotations


def review_trigger(outcome: float, quality: float, uncertainty_quality: float, accountability: float) -> bool:
    return outcome < 60 or quality < 0.65 or uncertainty_quality < 0.55 or accountability < 0.55


if __name__ == "__main__":
    print(review_trigger(58, 0.82, 0.91, 0.86))
    print(review_trigger(82, 0.84, 0.90, 0.92))
