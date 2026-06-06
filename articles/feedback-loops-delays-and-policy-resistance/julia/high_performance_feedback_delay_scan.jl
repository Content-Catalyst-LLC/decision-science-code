# high_performance_feedback_delay_scan.jl

function feedback_adjusted_score(dynamic_score, average_performance, worst_case, threshold_pass_rate)
    return 0.35 * dynamic_score + 0.25 * average_performance + 0.20 * worst_case + 0.20 * threshold_pass_rate
end

println("Feedback-adjusted score = ", round(feedback_adjusted_score(0.42, 0.79, 0.76, 1.0), digits=6))
