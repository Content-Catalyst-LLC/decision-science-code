#!/usr/bin/env python3
"""Adaptive response helper."""

from __future__ import annotations


def update_adaptive_response(response: float, target: float, current_state: float, learning_rate: float = 0.06) -> float:
    return max(0.0, response + learning_rate * (target - current_state))


if __name__ == "__main__":
    print(round(update_adaptive_response(14.0, 58.0, 52.0), 6))
