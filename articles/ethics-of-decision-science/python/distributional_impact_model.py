#!/usr/bin/env python3
def group_net_benefit(benefit, cost, risk):
    return benefit - cost - risk

def distributional_gap(values):
    return max(values) - min(values)

if __name__ == "__main__":
    values = [group_net_benefit(86, 24, 18), group_net_benefit(48, 44, 58), group_net_benefit(52, 34, 48)]
    print(values)
    print(distributional_gap(values))
