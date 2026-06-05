# bayesian_update_frontier.jl

function bayesian_update(prior, sensitivity, false_positive_rate)
    evidence_probability = sensitivity * prior + false_positive_rate * (1.0 - prior)
    return (sensitivity * prior) / evidence_probability
end

println("model drift posterior = ", round(bayesian_update(0.10, 0.82, 0.12), digits=6))
println("cost escalation posterior = ", round(bayesian_update(0.15, 0.76, 0.18), digits=6))
