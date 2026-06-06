#!/usr/bin/env python3
"""Structured dissent helper."""

from __future__ import annotations


def dissent_required(decision_stakes: str, evidence_quality: str, uncertainty: float) -> str:
    if decision_stakes == "high" or evidence_quality == "low" or uncertainty > 0.20:
        return "required"
    return "optional"


if __name__ == "__main__":
    print(dissent_required("high", "medium", 0.10))
    print(dissent_required("low", "high", 0.05))
