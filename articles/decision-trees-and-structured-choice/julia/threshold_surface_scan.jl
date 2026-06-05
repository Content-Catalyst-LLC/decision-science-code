# threshold_surface_scan.jl

function threshold_probability(success_payoff, failure_payoff, target, cost, credit)
    denom = success_payoff - failure_payoff
    if abs(denom) < 1e-9
        return NaN
    end
    return (target + cost - credit - failure_payoff) / denom
end

println("Immediate threshold:", round(threshold_probability(125.0, -35.0, 60.0, 0.0, 0.0), digits=4))
println("Staged threshold:", round(threshold_probability(145.0, -20.0, 60.0, 12.0, 18.0), digits=4))
