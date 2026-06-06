#!/usr/bin/env python3
"""Buffer depletion helper."""

from __future__ import annotations


def buffer_next(current_buffer: float, stress: float, replenishment: float = 0.015, depletion_rate: float = 0.08) -> float:
    return max(0.0, current_buffer - depletion_rate * stress + replenishment)


if __name__ == "__main__":
    print(round(buffer_next(0.58, 0.45), 6))
