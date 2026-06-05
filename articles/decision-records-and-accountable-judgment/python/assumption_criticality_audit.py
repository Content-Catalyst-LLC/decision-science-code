#!/usr/bin/env python3
"""Assumption criticality audit."""

from __future__ import annotations


def assumption_risk(confidence: float, criticality: float) -> float:
    return criticality * (1.0 - confidence)


def monitoring_gap(confidence: float, criticality: float, monitored: bool) -> bool:
    return criticality >= 0.75 and confidence < 0.75 and not monitored


if __name__ == "__main__":
    print(round(assumption_risk(0.42, 0.90), 4))
    print(monitoring_gap(0.42, 0.90, False))
