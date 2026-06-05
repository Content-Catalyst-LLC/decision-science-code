# high_performance_tree_rollback.jl

strategies = Dict(
    "Immediate Action" => (125.0, -35.0, 0.58, 0.0, 0.0),
    "Staged Learning" => (145.0, -20.0, 0.54, 12.0, 18.0),
    "Delay Without Learning" => (95.0, 20.0, 0.62, 5.0, 5.0),
    "Conservative Baseline" => (70.0, 55.0, 0.88, 0.0, 3.0)
)

function expected_value(success_payoff, failure_payoff, p, cost, credit)
    return success_payoff * p + failure_payoff * (1.0 - p) - cost + credit
end

for (name, values) in strategies
    success_payoff, failure_payoff, p, cost, credit = values
    println(name, " EV = ", round(expected_value(success_payoff, failure_payoff, p, cost, credit), digits=4))
end
