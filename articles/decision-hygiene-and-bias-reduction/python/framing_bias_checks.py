#!/usr/bin/env python3
"""Framing bias helper functions."""

from __future__ import annotations


def framing_sensitivity(frame_a_score: float, frame_b_score: float) -> float:
    return abs(frame_a_score - frame_b_score)


if __name__ == "__main__":
    print(round(framing_sensitivity(0.62, 0.48), 6))
