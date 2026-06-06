#!/usr/bin/env python3
"""Gain-loss frame model helper."""

from __future__ import annotations


def frame_reversal(gain_choice: str, loss_choice: str) -> bool:
    return gain_choice != loss_choice


if __name__ == "__main__":
    print(frame_reversal("sure option", "risky option"))
