# robustness_frontier_analysis.jl
# Robustness frontier scaffold.

payoffs = Dict(
    "optimize" => [120.0, 20.0, -80.0],
    "hedge" => [90.0, 60.0, 10.0],
    "preserve" => [65.0, 58.0, 40.0]
)

threshold = 35.0

for (name, values) in payoffs
    robustness = count(v -> v >= threshold, values) / length(values)
    println(name, " robustness = ", round(robustness, digits=3))
end
