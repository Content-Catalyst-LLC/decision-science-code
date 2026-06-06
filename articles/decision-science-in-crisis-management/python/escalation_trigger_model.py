#!/usr/bin/env python3
def escalation_required(risk: float, uncertainty: float, public_trust: float, resource_pressure: float, cascading_impact: float) -> bool:
    return risk >= 0.72 or uncertainty >= 0.62 or public_trust <= 0.46 or resource_pressure >= 0.70 or cascading_impact >= 0.64

if __name__ == "__main__":
    print(escalation_required(0.68, 0.64, 0.55, 0.61, 0.58))
