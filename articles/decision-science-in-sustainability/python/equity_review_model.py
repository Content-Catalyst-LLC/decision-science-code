#!/usr/bin/env python3
"""Environmental justice and equity review helper."""

from __future__ import annotations


def requires_equity_review(social_equity: float, public_trust: float, threshold: float = 0.50, trust_threshold: float = 45.0) -> bool:
    return social_equity < threshold or public_trust < trust_threshold


if __name__ == "__main__":
    print(requires_equity_review(0.46, 58.0))
