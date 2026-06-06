# high_performance_legitimacy_scan.jl

function weighted_score(values, weights)
    return sum(values .* weights)
end

values = [0.68, 0.80, 0.84, 0.82, 0.86, 0.90]
weights = [0.12, 0.18, 0.28, 0.14, 0.16, 0.12]
println("Stakeholder score = ", round(weighted_score(values, weights), digits=6))
