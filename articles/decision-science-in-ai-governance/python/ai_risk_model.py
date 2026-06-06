#!/usr/bin/env python3
"""AI risk decomposition helper."""

from __future__ import annotations


def composite_ai_risk(
    safety: float,
    equity: float,
    bias: float,
    privacy: float,
    opacity: float,
    security: float,
) -> float:
    return (
        0.20 * safety
        + 0.18 * equity
        + 0.16 * bias
        + 0.16 * privacy
        + 0.14 * opacity
        + 0.16 * security
    )


if __name__ == "__main__":
    print(round(composite_ai_risk(0.52, 0.48, 0.50, 0.42, 0.55, 0.46), 6))
