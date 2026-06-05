# adaptive_pathway_frontier.jl

struct Pathway
    name::String
    reversibility::Float64
    learning::Float64
    robustness::Float64
end

pathways = [
    Pathway("Expand", 0.22, 0.30, 0.35),
    Pathway("Hedge", 0.56, 0.55, 0.62),
    Pathway("PreserveOption", 0.90, 0.86, 0.78),
    Pathway("AdaptivePathway", 0.84, 0.92, 0.72)
]

for p in pathways
    score = 0.35 * p.reversibility + 0.35 * p.learning + 0.30 * p.robustness
    println(p.name, " adaptive score = ", round(score, digits=3))
end
