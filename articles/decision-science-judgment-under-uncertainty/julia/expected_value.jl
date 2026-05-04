# Decision Science: Expected Value in Julia
# Educational example only.

alternatives = Dict(
    "Incremental Program Upgrade" => [(0.65, 72.0), (0.35, 38.0)],
    "Targeted Resilience Investment" => [(0.55, 84.0), (0.45, 52.0)],
    "Large-Scale Transformation" => [(0.45, 96.0), (0.55, 30.0)]
)

function expected_value(outcomes)
    return sum(probability * value for (probability, value) in outcomes)
end

for (alternative, outcomes) in alternatives
    println(alternative, ": ", expected_value(outcomes))
end
