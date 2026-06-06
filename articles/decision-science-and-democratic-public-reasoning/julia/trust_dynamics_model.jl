# trust_dynamics_model.jl

function next_trust(current_trust, performance, transparency, responsiveness, fairness, uncertainty_stress, harm)
    trust = current_trust + 0.08 * performance + 0.06 * transparency + 0.08 * responsiveness + 0.08 * fairness - 0.06 * uncertainty_stress - 0.10 * harm
    return max(0.0, min(1.0, trust))
end

println("Next trust = ", round(next_trust(0.62, 0.70, 0.78, 0.74, 0.72, 0.36, 0.30), digits=6))
