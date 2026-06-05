#!/usr/bin/env python3
"""Systems consequence scan."""

from __future__ import annotations


def systems_risk(feedback_strength: float, delay: float, spillover: float, lock_in: float) -> float:
    return 0.30 * feedback_strength + 0.25 * delay + 0.25 * spillover + 0.20 * lock_in


if __name__ == "__main__":
    print(round(systems_risk(0.70, 0.60, 0.50, 0.80), 4))
