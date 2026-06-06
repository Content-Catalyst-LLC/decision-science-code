# high_performance_future_decision_scan.jl

function future_decision_score(ai, governance, uncertainty, legitimacy, reproducibility, systems, ethics, adaptive, burden, failure)
    return 0.12 * ai + 0.14 * governance + 0.14 * uncertainty + 0.12 * legitimacy + 0.12 * reproducibility + 0.12 * systems + 0.14 * ethics + 0.14 * adaptive - 0.04 * burden - 0.12 * failure
end

println("Future decision score = ", round(future_decision_score(0.86, 0.90, 0.88, 0.84, 0.88, 0.86, 0.90, 0.88, 0.80, 0.24), digits=6))
