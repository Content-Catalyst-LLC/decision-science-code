# prospect_value_sensitivity.jl

function prospect_value(x, lambda)
    x >= 0 ? x^0.88 : -lambda * ((-x)^0.88)
end

for lambda in [1.5, 2.0, 2.5]
    println("loss_aversion=", lambda, " loss_value=", round(prospect_value(-100.0, lambda), digits=6))
end
