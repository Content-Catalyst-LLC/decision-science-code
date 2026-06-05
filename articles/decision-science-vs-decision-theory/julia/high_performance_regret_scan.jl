# high_performance_regret_scan.jl

strategies = ["Optimize", "Balanced", "Robust", "Adaptive", "StagedPilot"]
payoff = [
    145.0 92.0 30.0 -95.0 -40.0;
    112.0 84.0 58.0 12.0 30.0;
    78.0 72.0 65.0 48.0 55.0;
    98.0 80.0 62.0 38.0 68.0;
    82.0 70.0 60.0 42.0 74.0
]

best = vec(maximum(payoff, dims=1))
for (i, strategy) in enumerate(strategies)
    regrets = best .- payoff[i, :]
    println(strategy, " max regret = ", maximum(regrets))
end
