# cascade_risk_model.jl

function cascade_risk_score(exposure, dependency_centrality, buffer_weakness, common_mode_risk, monitoring_quality, response_capacity)
    return 0.22 * exposure + 0.22 * dependency_centrality + 0.20 * buffer_weakness + 0.18 * common_mode_risk - 0.09 * monitoring_quality - 0.09 * response_capacity
end

println("Cascade risk score = ", round(cascade_risk_score(0.82, 0.88, 0.76, 0.79, 0.42, 0.40), digits=6))
