# robust_paradigm_frontier.jl

strategies = Dict(
    "Aggressive" => [128.0, 50.0, -90.0, -20.0],
    "Balanced" => [92.0, 68.0, 18.0, 42.0],
    "Defensive" => [62.0, 58.0, 44.0, 54.0],
    "Adaptive" => [88.0, 70.0, 36.0, 72.0]
)

threshold = 40.0
for (name, values) in strategies
    robust = count(v -> v >= threshold, values) / length(values)
    println(name, " robustness = ", round(robust, digits=3))
end
