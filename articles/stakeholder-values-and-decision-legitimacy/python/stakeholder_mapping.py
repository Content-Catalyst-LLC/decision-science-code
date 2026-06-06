#!/usr/bin/env python3
"""Stakeholder mapping helper."""

from __future__ import annotations


def affectedness_priority(affectedness: float, vulnerability: float, influence: float) -> float:
    return 0.45 * affectedness + 0.35 * vulnerability + 0.20 * (1.0 - influence)


if __name__ == "__main__":
    print(round(affectedness_priority(0.9, 0.8, 0.2), 6))
