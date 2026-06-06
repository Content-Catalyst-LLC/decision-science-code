#!/usr/bin/env python3
def message_priority(risk: float, uncertainty: float, actionability: float, time_sensitivity: float) -> float:
    return 0.34 * risk + 0.22 * uncertainty + 0.24 * actionability + 0.20 * time_sensitivity

def trust_update(current_trust: float, clarity: float, consistency: float, responsiveness: float, rumor_pressure: float) -> float:
    return max(0.0, min(1.0, current_trust + 0.06 * clarity + 0.05 * consistency + 0.05 * responsiveness - 0.08 * rumor_pressure))

if __name__ == "__main__":
    print(round(message_priority(0.78, 0.62, 0.82, 0.88), 6))
    print(round(trust_update(0.58, 0.80, 0.76, 0.72, 0.34), 6))
