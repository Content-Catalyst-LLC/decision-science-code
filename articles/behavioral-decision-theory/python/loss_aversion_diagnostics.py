#!/usr/bin/env python3
"""Loss aversion diagnostics."""

from __future__ import annotations


def loss_aversion_flag(loss_aversion: float, threshold: float = 2.5) -> str:
    return "review" if loss_aversion >= threshold else "acceptable"


if __name__ == "__main__":
    for value in [1.6, 2.2, 2.7]:
        print(value, loss_aversion_flag(value))
