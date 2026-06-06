# high_performance_framing_scan.jl

function prospect_value(x; alpha=0.88, beta=0.88, loss_aversion=2.0)
    if x >= 0
        return x^alpha
    else
        return -loss_aversion * ((-x)^beta)
    end
end

function prospect_score(high, p_high, low, reference)
    return p_high * prospect_value(high - reference) + (1 - p_high) * prospect_value(low - reference)
end

println("Sure gain score = ", round(prospect_score(120.0, 1.0, 0.0, 0.0), digits=6))
println("Risky gain score = ", round(prospect_score(240.0, 0.60, 0.0, 0.0), digits=6))
