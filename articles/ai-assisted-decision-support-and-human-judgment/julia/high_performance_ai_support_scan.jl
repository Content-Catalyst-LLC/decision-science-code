# high_performance_ai_support_scan.jl

function decision_support_score(model_performance, uncertainty_visibility, oversight, contestability, fairness, accountability, monitoring, automation_bias, burden)
    return 0.16 * model_performance + 0.14 * uncertainty_visibility + 0.16 * oversight + 0.14 * contestability + 0.14 * fairness + 0.14 * accountability + 0.10 * monitoring - 0.10 * automation_bias - 0.04 * burden
end

println("Decision-support score = ", round(decision_support_score(0.82, 0.86, 0.88, 0.86, 0.84, 0.90, 0.90, 0.28, 0.68), digits=6))
