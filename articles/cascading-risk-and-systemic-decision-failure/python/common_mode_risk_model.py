#!/usr/bin/env python3
"""Common-mode risk helper."""

from __future__ import annotations


def common_mode_review(common_mode_risk: float, threshold: float = 0.70) -> bool:
    return common_mode_risk >= threshold


if __name__ == "__main__":
    print(common_mode_review(0.74))
