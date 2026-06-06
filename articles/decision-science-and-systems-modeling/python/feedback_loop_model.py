#!/usr/bin/env python3
"""Feedback loop helper."""

from __future__ import annotations


def feedback_update(state: float, reinforcing: float, balancing: float, disturbance: float = 0.0) -> float:
    return state + reinforcing - balancing + disturbance


if __name__ == "__main__":
    print(round(feedback_update(55.0, 3.85, 2.10, -0.4), 6))
