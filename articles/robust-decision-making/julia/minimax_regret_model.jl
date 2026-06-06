function max_regret(values, scenario_bests)
    return maximum(scenario_bests .- values)
end
println("Maximum regret = ", round(max_regret([0.73, 0.77, 0.79, 0.81], [0.92, 0.77, 0.83, 0.81]), digits=6))
