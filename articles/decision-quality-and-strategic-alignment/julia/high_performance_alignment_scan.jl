# high_performance_alignment_scan.jl

function weighted_score(scores, weights)
    if abs(sum(weights) - 1.0) > 1e-9
        error("Weights must sum to 1.")
    end
    return sum(scores .* weights)
end

scores = [0.86, 0.88, 0.82, 0.86, 0.89, 0.77]
weights = [0.16, 0.15, 0.17, 0.18, 0.18, 0.16]
println("Decision quality score = ", round(weighted_score(scores, weights), digits=6))
