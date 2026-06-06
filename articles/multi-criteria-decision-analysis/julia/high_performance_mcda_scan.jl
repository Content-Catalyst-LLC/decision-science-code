# high_performance_mcda_scan.jl

function weighted_score(scores, weights)
    if abs(sum(weights) - 1.0) > 1e-9
        error("Weights must sum to 1.")
    end
    return sum(scores .* weights)
end

scores = [0.8, 0.6, 0.9]
weights = [0.3, 0.3, 0.4]
println("Weighted score = ", round(weighted_score(scores, weights), digits=6))
