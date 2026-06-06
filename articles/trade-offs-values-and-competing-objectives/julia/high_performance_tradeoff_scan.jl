# high_performance_tradeoff_scan.jl

function weighted_score(scores, weights)
    if abs(sum(weights) - 1.0) > 1e-9
        error("Weights must sum to 1.")
    end
    return sum(scores .* weights)
end

scores = [0.90, 0.38, 0.42, 0.54, 0.48, 0.70]
weights = [0.18, 0.18, 0.20, 0.18, 0.14, 0.12]
println("Weighted score = ", round(weighted_score(scores, weights), digits=6))
