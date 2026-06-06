#!/usr/bin/env python3
def crisis_risk(likelihood: float, severity: float, exposure: float, vulnerability: float, criticality: float) -> float:
    return likelihood * severity * exposure * vulnerability * criticality

if __name__ == "__main__":
    print(round(crisis_risk(0.72, 0.86, 0.68, 0.62, 0.90), 6))
