#!/usr/bin/env python3
"""Reference-class forecasting helper."""

from __future__ import annotations


def adjusted_forecast(base_rate: float, evidence_adjustment: float) -> float:
    return max(0.01, min(0.99, base_rate + evidence_adjustment))


if __name__ == "__main__":
    print(round(adjusted_forecast(0.46, 0.12), 6))
