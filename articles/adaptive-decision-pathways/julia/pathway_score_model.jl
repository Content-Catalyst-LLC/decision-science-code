# pathway_score_model.jl

function pathway_score(initial_performance, flexibility, monitoring_quality, trigger_clarity, switching_cost, fallback_strength)
    return 0.20 * initial_performance + 0.18 * flexibility + 0.16 * monitoring_quality + 0.16 * trigger_clarity - 0.12 * switching_cost + 0.18 * fallback_strength
end

println("Pathway score = ", round(pathway_score(0.76, 0.88, 0.82, 0.80, 0.38, 0.84), digits=6))
