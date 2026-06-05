# high_performance_scenario_scan.jl
# High-performance scenario scan scaffold for decision science.

struct Scenario
    name::String
    probability::Float64
    multiplier::Float64
    disruption::Float64
end

struct Alternative
    name::String
    benefit::Float64
    cost::Float64
    resilience::Float64
end

function payoff(a::Alternative, s::Scenario)
    return a.benefit * s.multiplier - a.cost - s.disruption * (1.0 - a.resilience) * 50.0
end

scenarios = [
    Scenario("baseline", 0.4, 1.0, 0.1),
    Scenario("adverse", 0.35, 0.8, 0.4),
    Scenario("shock", 0.25, 0.6, 0.8),
]

alternatives = [
    Alternative("optimize", 120.0, 45.0, 0.35),
    Alternative("robust", 88.0, 40.0, 0.85),
    Alternative("staged", 75.0, 30.0, 0.65),
]

for a in alternatives
    ev = sum(s.probability * payoff(a, s) for s in scenarios)
    println(a.name, " expected value = ", round(ev, digits=3))
end
