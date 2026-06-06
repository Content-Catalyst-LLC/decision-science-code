#!/usr/bin/env python3
"""Evidence-quality review helpers."""

from __future__ import annotations


def evidence_review_flag(evidence_quality: str, decision_stakes: str) -> str:
    if evidence_quality == "low" and decision_stakes == "high":
        return "review"
    return "acceptable"


if __name__ == "__main__":
    print(evidence_review_flag("low", "high"))
    print(evidence_review_flag("high", "high"))
