# high_performance_sensitivity_scan.jl

function score(base, demand_sensitivity, cost_sensitivity, disruption_sensitivity, resilience_buffer, adaptation_capacity, demand, cost, disruption)
    return base + demand_sensitivity * demand - cost_sensitivity * cost - disruption_sensitivity * disruption +
           resilience_buffer * max(0.0, disruption) + adaptation_capacity * abs(demand)
end

strategies = [
    ("Efficiency Strategy", 78.0, 10.0, 16.0, 18.0, 4.0, 3.0),
    ("Balanced Strategy", 75.0, 8.0, 10.0, 11.0, 9.0, 7.0),
    ("Resilience Strategy", 70.0, 5.5, 8.0, 7.0, 16.0, 5.0),
    ("Adaptive Strategy", 73.0, 7.0, 9.0, 9.0, 12.0, 12.0)
]

for s in strategies
    name, base, ds, cs, dis, rb, ac = s
    println(name, " baseline score = ", round(score(base, ds, cs, dis, rb, ac, 0.5, 0.3, 0.2), digits=4))
end
