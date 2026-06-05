# high_performance_record_quality_scan.jl

records = Dict(
    "DR-001" => [0.82,0.74,0.78,0.72,0.70,0.76,0.68,0.80,0.66,0.62,0.78],
    "DR-002" => [0.88,0.84,0.82,0.80,0.86,0.78,0.72,0.84,0.82,0.80,0.86],
    "DR-003" => [0.76,0.70,0.86,0.74,0.72,0.82,0.64,0.78,0.68,0.70,0.74],
    "DR-004" => [0.62,0.50,0.58,0.46,0.40,0.52,0.30,0.56,0.34,0.32,0.48],
    "DR-005" => [0.91,0.88,0.80,0.89,0.92,0.86,0.84,0.88,0.90,0.92,0.90]
)

weights = [0.10,0.09,0.11,0.11,0.12,0.10,0.09,0.10,0.09,0.09,0.10]

for (id, scores) in records
    quality = sum(scores .* weights)
    minimum_component = minimum(scores)
    accountable = 0.70 * quality + 0.30 * minimum_component
    println(id, " accountable judgment score = ", round(accountable, digits=4))
end
