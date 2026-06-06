# stock_flow_model.jl

function stock_update(stock, inflow, outflow)
    return stock + inflow - outflow
end

println("Next stock = ", round(stock_update(100.0, 12.0, 8.5), digits=6))
