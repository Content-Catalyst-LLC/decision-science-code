# resource_pressure_model.jl

function resource_next(resource_stock, extraction, regeneration)
    return max(0.0, resource_stock - extraction + regeneration)
end

function pressure_next(resource_pressure, policy_response, governance_delay, random_component)
    return max(5.0, resource_pressure + random_component - 0.050 * policy_response + 0.030 * governance_delay)
end

println("Resource next = ", round(resource_next(100.0, 28.0, 13.2), digits=6))
println("Pressure next = ", round(pressure_next(28.0, 8.0, 5.0, 0.60), digits=6))
