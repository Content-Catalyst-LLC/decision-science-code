#!/usr/bin/env python3
"""Framing sensitivity helper."""

from __future__ import annotations


def frame_sensitivity_index(gain_score: float, loss_score: float) -> float:
    return abs(gain_score - loss_score)


def frame_reversal(gain_choice: str, loss_choice: str) -> bool:
    return gain_choice != loss_choice


if __name__ == "__main__":
    print(round(frame_sensitivity_index(50.0, -80.0), 6))
    print(frame_reversal("safe", "risky"))
