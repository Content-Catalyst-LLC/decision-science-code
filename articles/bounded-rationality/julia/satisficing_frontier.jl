# satisficing_frontier.jl

values = [0.58, 0.71, 0.82, 0.77, 0.91]

for aspiration in [0.60, 0.70, 0.80, 0.90]
    selected = findfirst(x -> x >= aspiration, values)
    if selected === nothing
        selected = argmax(values)
    end
    println("aspiration=", aspiration, " selected=", selected, " value=", values[selected])
end
