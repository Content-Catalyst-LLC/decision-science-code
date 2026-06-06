#!/usr/bin/env python3
"""Model reliance helper for AI-assisted decision support."""

from __future__ import annotations


def justified_model_reliance(evidence_quality: float, calibration: float, decision_risk: float, uncertainty: float) -> float:
    reliance = 0.35 * evidence_quality + 0.35 * calibration - 0.16 * decision_risk - 0.14 * uncertainty
    return max(0.0, min(1.0, reliance))


if __name__ == "__main__":
    print(round(justified_model_reliance(0.82, 0.78, 0.54, 0.36), 6))
