# high_performance_prospect_scan.jl

function prospect_value(x; alpha=0.88, beta=0.88, loss_aversion=2.0)
    x >= 0 ? x^alpha : -loss_aversion * ((-x)^beta)
end

function weighted_probability(p; gamma=0.72)
    return (p^gamma) / ((p^gamma + (1 - p)^gamma)^(1 / gamma))
end

println("Gain value = ", round(prospect_value(100.0), digits=6))
println("Loss value = ", round(prospect_value(-100.0), digits=6))
println("Weighted probability = ", round(weighted_probability(0.10), digits=6))
