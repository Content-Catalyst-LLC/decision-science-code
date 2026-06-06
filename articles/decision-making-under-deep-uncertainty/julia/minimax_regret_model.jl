# minimax_regret_model.jl

function max_regret(values, scenario_bests)
    return maximum(scenario_bests .- values)
end

values = [0.72, 0.80, 0.78, 0.87, 0.75, 0.77]
bests = [0.91, 0.80, 0.84, 0.88, 0.81, 0.83]
println("Maximum regret = ", round(max_regret(values, bests), digits=6))
