#!/usr/bin/env python3
"""Adaptive pathway trigger scaffold."""

from __future__ import annotations


def trigger_active(model_shift: float, loss_frequency: float, implementation_capacity: float) -> bool:
    return model_shift >= 0.65 or loss_frequency >= 0.25 or implementation_capacity <= 0.50


if __name__ == "__main__":
    print(trigger_active(model_shift=0.70, loss_frequency=0.10, implementation_capacity=0.72))
    print(trigger_active(model_shift=0.30, loss_frequency=0.10, implementation_capacity=0.72))
