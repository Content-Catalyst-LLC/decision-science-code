#!/usr/bin/env python3
"""Adaptive revision helper."""

from __future__ import annotations


def should_revise(system_state: float, resilience_capacity: float, stress_threshold: float, resilience_threshold: float) -> bool:
    return system_state >= stress_threshold or resilience_capacity <= resilience_threshold


if __name__ == "__main__":
    print(should_revise(72.0, 24.0, 80.0, 25.0))
