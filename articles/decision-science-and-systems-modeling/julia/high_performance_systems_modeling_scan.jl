# high_performance_systems_modeling_scan.jl

function systems_decision_score(dynamic_score, average_performance, worst_case, threshold_pass_rate)
    return 0.35 * dynamic_score + 0.25 * average_performance + 0.20 * worst_case + 0.20 * threshold_pass_rate
end

println("Systems decision score = ", round(systems_decision_score(0.78, 0.82, 0.79, 1.0), digits=6))
