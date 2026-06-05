# robust_strategy_frontier.jl

strategies = Dict(
    "Optimize" => [145.0, 92.0, 30.0, -95.0, -40.0],
    "Balanced" => [112.0, 84.0, 58.0, 12.0, 30.0],
    "Robust" => [78.0, 72.0, 65.0, 48.0, 55.0],
    "Adaptive" => [98.0, 80.0, 62.0, 38.0, 68.0],
    "StagedPilot" => [82.0, 70.0, 60.0, 42.0, 74.0]
)

threshold = 45.0
for (name, values) in strategies
    robust = count(v -> v >= threshold, values) / length(values)
    println(name, " robustness = ", round(robust, digits=3))
end
