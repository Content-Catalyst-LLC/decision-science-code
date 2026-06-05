# forecast_value_frontier.jl

function forecast_value(loss_without_forecast, loss_with_forecast, forecast_cost)
    return loss_without_forecast - loss_with_forecast - forecast_cost
end

println("forecast value proxy = ", round(forecast_value(25.0, 14.0, 3.5), digits=6))
