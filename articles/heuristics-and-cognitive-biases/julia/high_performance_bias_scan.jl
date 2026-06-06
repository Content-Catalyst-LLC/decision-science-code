# high_performance_bias_scan.jl

function clamp01(x)
    return min(max(x, 0.01), 0.99)
end

function anchored_estimate(anchor, evidence, weight)
    return clamp01(weight * anchor + (1 - weight) * evidence)
end

function brier_score(probability, outcome)
    return (probability - outcome)^2
end

println("Anchored estimate = ", round(anchored_estimate(0.80, 0.42, 0.45), digits=6))
println("Brier score = ", round(brier_score(0.72, 1.0), digits=6))
