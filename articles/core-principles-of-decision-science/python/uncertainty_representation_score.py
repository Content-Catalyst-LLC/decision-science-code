#!/usr/bin/env python3
"""Uncertainty representation scoring."""

from __future__ import annotations


def uncertainty_score(probabilities: bool, ranges: bool, scenarios: bool, assumptions: bool, sensitivity: bool) -> float:
    return sum([probabilities, ranges, scenarios, assumptions, sensitivity]) / 5.0


if __name__ == "__main__":
    print(uncertainty_score(True, True, True, True, False))
