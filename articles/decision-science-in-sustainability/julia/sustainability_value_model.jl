# sustainability_value_model.jl

function sustainability_value_score(emissions_reduction, social_equity, cost_burden, resilience_score, implementation_feasibility, threshold_protection)
    return 0.22 * emissions_reduction + 0.20 * social_equity - 0.12 * cost_burden + 0.18 * resilience_score + 0.12 * implementation_feasibility + 0.16 * threshold_protection
end

println("Sustainability value score = ", round(sustainability_value_score(0.61, 0.74, 0.49, 0.82, 0.66, 0.82), digits=6))
