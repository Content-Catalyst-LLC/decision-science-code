# robust_uncertainty_scenario_scan.jl

strategies = Dict(
    "Expand" => [120.0, 45.0, -95.0, -130.0, 20.0],
    "Hedge" => [92.0, 68.0, 18.0, -20.0, 55.0],
    "PreserveOption" => [72.0, 62.0, 42.0, 18.0, 70.0],
    "AdaptivePathway" => [95.0, 72.0, 34.0, 10.0, 78.0]
)

threshold = 40.0

for (name, values) in strategies
    robust = count(v -> v >= threshold, values) / length(values)
    println(name, " robustness = ", round(robust, digits=3))
end
