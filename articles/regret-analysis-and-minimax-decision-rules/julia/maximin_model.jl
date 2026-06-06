# maximin_model.jl

function maximin_value(values)
    return minimum(values)
end

println("Maximin value = ", round(maximin_value([0.73, 0.81, 0.79, 0.87, 0.76, 0.77]), digits=6))
