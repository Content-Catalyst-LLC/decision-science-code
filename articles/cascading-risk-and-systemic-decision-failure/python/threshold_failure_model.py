#!/usr/bin/env python3
"""Threshold failure helper."""

from __future__ import annotations


def threshold_failure(stress: float, neighbor_failure_load: float, buffer: float, threshold: float) -> bool:
    effective_stress = stress + neighbor_failure_load + max(0.0, 0.40 - buffer)
    return effective_stress >= threshold


if __name__ == "__main__":
    print(threshold_failure(0.52, 0.18, 0.31, 0.66))
