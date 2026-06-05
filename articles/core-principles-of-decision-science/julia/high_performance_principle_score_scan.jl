# high_performance_principle_score_scan.jl

alternatives = Dict(
    "Fast Expansion" => [0.55, 0.42, 0.40, 0.36, 0.44, 0.38, 0.44, 0.52, 0.30],
    "Balanced Adaptation" => [0.81, 0.78, 0.79, 0.71, 0.74, 0.74, 0.76, 0.78, 0.74],
    "Resilient Strategy" => [0.76, 0.83, 0.82, 0.76, 0.88, 0.91, 0.80, 0.80, 0.78],
    "Adaptive Learning Strategy" => [0.88, 0.87, 0.85, 0.84, 0.86, 0.86, 0.93, 0.84, 0.88],
    "Evidence-First Pilot" => [0.92, 0.90, 0.91, 0.88, 0.80, 0.78, 0.89, 0.94, 0.95]
)

weights = [0.12, 0.14, 0.12, 0.10, 0.11, 0.14, 0.12, 0.08, 0.07]

for (name, values) in alternatives
    score = sum(values .* weights)
    println(name, " composite score = ", round(score, digits=4))
end
