#!/usr/bin/env python3
"""Implementation readiness helper."""

from __future__ import annotations


def readiness_flag(score: float, threshold: float = 0.65) -> str:
    if score < threshold:
        return "review"
    return "acceptable"


if __name__ == "__main__":
    print(readiness_flag(0.60))
    print(readiness_flag(0.80))
