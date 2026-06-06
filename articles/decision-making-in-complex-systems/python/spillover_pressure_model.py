#!/usr/bin/env python3
"""Spillover pressure helper."""

from __future__ import annotations


def update_spillover_pressure(pressure: float, system_state: float, adaptive_response: float) -> float:
    return max(0.0, pressure + 0.05 * system_state - 0.03 * adaptive_response)


if __name__ == "__main__":
    print(round(update_spillover_pressure(7.0, 52.0, 14.0), 6))
