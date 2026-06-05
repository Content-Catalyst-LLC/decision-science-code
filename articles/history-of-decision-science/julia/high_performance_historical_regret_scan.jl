# high_performance_historical_regret_scan.jl

strategies = ["Aggressive", "Balanced", "Defensive", "Adaptive"]
payoff = [
    128.0 50.0 -90.0 -20.0;
    92.0 68.0 18.0 42.0;
    62.0 58.0 44.0 54.0;
    88.0 70.0 36.0 72.0
]

best = vec(maximum(payoff, dims=1))
for (i, strategy) in enumerate(strategies)
    regrets = best .- payoff[i, :]
    println(strategy, " max regret = ", maximum(regrets))
end
