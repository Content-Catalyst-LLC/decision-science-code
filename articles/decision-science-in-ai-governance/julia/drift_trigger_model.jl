# drift_trigger_model.jl

function drift_indicator(current_metric, baseline_metric)
    return abs(current_metric - baseline_metric)
end

println("Drift indicator = ", round(drift_indicator(0.77, 0.86), digits=6))
