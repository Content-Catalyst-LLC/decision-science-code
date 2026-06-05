#!/usr/bin/env python3
"""Dissent preservation audit."""

from __future__ import annotations


def dissent_score(dissent_present: bool, evidence_recorded: bool, response_recorded: bool, unresolved_flag: bool) -> float:
    values = [dissent_present, evidence_recorded, response_recorded, unresolved_flag]
    return sum(1 for value in values if value) / len(values)


if __name__ == "__main__":
    print(round(dissent_score(True, True, True, False), 4))
