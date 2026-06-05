# decision_architecture_frontier.jl

profiles = Dict(
    "Fast Commitment" => (0.42, 0.28),
    "Evidence-Guided Choice" => (0.78, 0.76),
    "Robust Adaptive Pathway" => (0.84, 0.90),
    "Staged Learning Decision" => (0.86, 0.96)
)

for (name, pair) in profiles
    safeguards, learning = pair
    score = 0.45 * safeguards + 0.55 * learning
    println(name, " review-readiness score = ", round(score, digits=4))
end
