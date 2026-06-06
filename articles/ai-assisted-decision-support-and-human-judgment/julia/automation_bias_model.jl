# automation_bias_model.jl

function automation_bias(actual_reliance, justified_reliance)
    return actual_reliance - justified_reliance
end

println("Automation bias = ", round(automation_bias(0.78, 0.56), digits=6))
