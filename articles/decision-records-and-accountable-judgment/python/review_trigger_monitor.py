#!/usr/bin/env python3
"""Review trigger monitor."""

from __future__ import annotations


def trigger_active(value: float, lower: float, upper: float) -> bool:
    return value < lower or value > upper


if __name__ == "__main__":
    print(trigger_active(0.34, 0.0, 0.30))
    print(trigger_active(0.12, 0.0, 0.15))
