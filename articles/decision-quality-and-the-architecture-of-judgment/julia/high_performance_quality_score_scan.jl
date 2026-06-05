# high_performance_quality_score_scan.jl

alternatives = Dict(
    "Fast Commitment" => [0.55,0.50,0.48,0.35,0.42,0.30,0.38,0.34,0.28],
    "Evidence-Guided Choice" => [0.84,0.80,0.88,0.78,0.80,0.74,0.72,0.80,0.76],
    "Robust Adaptive Pathway" => [0.88,0.86,0.82,0.91,0.86,0.84,0.90,0.86,0.90],
    "Consensus Shortcut" => [0.46,0.44,0.52,0.40,0.38,0.28,0.36,0.42,0.34],
    "Staged Learning Decision" => [0.92,0.90,0.94,0.90,0.88,0.86,0.82,0.94,0.96]
)

weights = [0.11,0.10,0.12,0.13,0.11,0.10,0.11,0.11,0.11]

for (name, scores) in alternatives
    score = sum(scores .* weights)
    println(name, " decision-quality score = ", round(score, digits=4))
end
