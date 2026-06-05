# regret_surface_diagnostics.jl
# Regret diagnostics scaffold.

strategies = ["optimize", "hedge", "preserve"]
matrix = [
    120.0 20.0 -80.0;
    90.0 60.0 10.0;
    65.0 58.0 40.0
]

best_by_scenario = vec(maximum(matrix, dims=1))
regret = similar(matrix)

for i in axes(matrix, 1), j in axes(matrix, 2)
    regret[i, j] = best_by_scenario[j] - matrix[i, j]
end

for (i, strategy) in enumerate(strategies)
    println(strategy, " max regret = ", maximum(regret[i, :]))
end
