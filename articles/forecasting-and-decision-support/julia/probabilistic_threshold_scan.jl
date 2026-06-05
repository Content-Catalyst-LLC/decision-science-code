# probabilistic_threshold_scan.jl

function threshold_from_costs(false_positive_cost, false_negative_cost)
    return false_positive_cost / (false_positive_cost + false_negative_cost)
end

for costs in [(15.0, 85.0), (24.0, 80.0), (12.0, 70.0)]
    fp, fn = costs
    println("threshold = ", round(threshold_from_costs(fp, fn), digits=6))
end
