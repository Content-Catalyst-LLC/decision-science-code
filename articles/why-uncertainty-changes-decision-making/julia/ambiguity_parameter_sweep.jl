# ambiguity_parameter_sweep.jl

expected_utility = Dict(
    "Expand" => 0.62,
    "Hedge" => 0.66,
    "PreserveOption" => 0.60,
    "AdaptivePathway" => 0.70
)

ambiguity = Dict(
    "Expand" => 0.42,
    "Hedge" => 0.22,
    "PreserveOption" => 0.08,
    "AdaptivePathway" => 0.15
)

for lambda in 0.0:0.5:3.0
    scores = Dict(k => expected_utility[k] - lambda * ambiguity[k] for k in keys(expected_utility))
    best = collect(keys(scores))[argmax(collect(values(scores)))]
    println("lambda=", lambda, " best=", best, " score=", round(scores[best], digits=4))
end
