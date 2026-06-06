# probability_weighting_frontier.jl

function weighted_probability(p, gamma)
    return (p^gamma) / ((p^gamma + (1 - p)^gamma)^(1 / gamma))
end

for p in [0.05, 0.10, 0.50, 0.90]
    println("p=", p, " weighted=", round(weighted_probability(p, 0.72), digits=6))
end
