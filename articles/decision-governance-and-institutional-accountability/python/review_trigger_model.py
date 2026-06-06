#!/usr/bin/env python3
"""Decision governance review trigger helper."""

from __future__ import annotations


def review_required(
    accountability: float,
    evidence_traceability: float,
    review_strength: float,
    responsibility_gap: float,
    risk_exposure: float,
    accountability_trigger: float = 0.56,
    traceability_trigger: float = 0.58,
    review_trigger: float = 0.58,
    responsibility_gap_trigger: float = 0.28,
    risk_trigger: float = 0.68,
) -> bool:
    return (
        accountability <= accountability_trigger
        or evidence_traceability <= traceability_trigger
        or review_strength <= review_trigger
        or responsibility_gap >= responsibility_gap_trigger
        or risk_exposure >= risk_trigger
    )


if __name__ == "__main__":
    print(review_required(0.54, 0.62, 0.61, 0.20, 0.48))
