#!/usr/bin/env python3
"""Timing review helper."""

from __future__ import annotations


def should_review(lock_in_risk: float, option_value: float, lock_in_threshold: float = 0.72, option_threshold: float = 0.35) -> bool:
    return lock_in_risk >= lock_in_threshold or option_value <= option_threshold


if __name__ == "__main__":
    print(should_review(0.73, 0.42))
