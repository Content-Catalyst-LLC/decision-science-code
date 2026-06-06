# regret_model.jl

function maximum_regret(strategy_values, scenario_best_values)
    regrets = scenario_best_values .- strategy_values
    return maximum(regrets)
end

println("Maximum regret = ", round(maximum_regret([0.76, 0.71, 0.63], [0.92, 0.76, 0.82]), digits=6))
