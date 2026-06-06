# policy_value_model.jl

function policy_value_score(efficiency, equity, resilience, feasibility, legitimacy, implementation_capacity)
    return 0.18 * efficiency + 0.22 * equity + 0.18 * resilience + 0.14 * feasibility + 0.14 * legitimacy + 0.14 * implementation_capacity
end

println("Policy value score = ", round(policy_value_score(0.72, 0.84, 0.70, 0.76, 0.80, 0.86), digits=6))
