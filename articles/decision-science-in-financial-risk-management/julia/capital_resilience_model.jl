# capital_resilience_model.jl

function capital_next(current_capital, period_return_pct, floor)
    return max(floor, current_capital * (1.0 + period_return_pct / 100.0))
end

println("Capital next = ", round(capital_next(100.0, -8.5, 20.0), digits=6))
