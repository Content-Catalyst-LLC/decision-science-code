# robustness_frontier_core_principles.jl

frontier = Dict(
    "Fast Expansion" => (0.38, 0.44),
    "Balanced Adaptation" => (0.74, 0.76),
    "Resilient Strategy" => (0.91, 0.80),
    "Adaptive Learning Strategy" => (0.86, 0.93),
    "Evidence-First Pilot" => (0.78, 0.89)
)

for (name, pair) in frontier
    robustness, adaptability = pair
    score = 0.5 * robustness + 0.5 * adaptability
    println(name, " robust-adaptive score = ", round(score, digits=4))
end
