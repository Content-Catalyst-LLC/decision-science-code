#!/usr/bin/env python3
"""Decision-threshold calibration helper."""

from __future__ import annotations


def should_act(probability: float, threshold: float) -> bool:
    return probability >= threshold


if __name__ == "__main__":
    print(should_act(0.72, 0.65))
    print(should_act(0.58, 0.65))
