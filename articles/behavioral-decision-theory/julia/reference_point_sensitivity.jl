# reference_point_sensitivity.jl

function prospect_value(x; alpha=0.88, beta=0.88, loss_aversion=2.0)
    x >= 0 ? x^alpha : -loss_aversion * ((-x)^beta)
end

for reference in [-100.0, 0.0, 100.0]
    println("reference=", reference, " score=", round(prospect_value(120.0 - reference), digits=6))
end
