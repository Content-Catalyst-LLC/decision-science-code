# threshold_frontier.jl

function threshold_equal_utility(a_intercept, a_slope, b_intercept, b_slope)
    denom = a_slope - b_slope
    if abs(denom) < 1e-9
        return NaN
    end
    return (b_intercept - a_intercept) / denom
end

println("Demand threshold = ", round(threshold_equal_utility(70.0, 5.5, 73.0, 7.0), digits=4))
