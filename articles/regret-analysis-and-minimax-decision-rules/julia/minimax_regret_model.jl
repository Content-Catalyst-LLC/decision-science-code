# minimax_regret_model.jl

function max_regret(values, scenario_bests)
    return maximum(scenario_bests .- values)
end

values = [0.73, 0.81, 0.79, 0.87, 0.76, 0.77]
bests = [0.92, 0.81, 0.84, 0.88, 0.82, 0.83]
println("Maximum regret = ", round(max_regret(values, bests), digits=6))
