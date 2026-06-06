# resilience_stock_model.jl

function resilience_update(current, recovery, investment, degradation, shock)
    return max(0.0, current + recovery + investment - degradation - shock)
end

println("Next resilience stock = ", round(resilience_update(35.0, 3.0, 2.0, 1.0, 1.6), digits=6))
