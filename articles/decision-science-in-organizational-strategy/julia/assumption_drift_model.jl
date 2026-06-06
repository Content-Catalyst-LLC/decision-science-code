# assumption_drift_model.jl

function drift_next(current_drift, signal_pressure, adaptability, governance_support)
    return max(0.0, min(1.0, current_drift + signal_pressure - 0.025 * adaptability - 0.015 * governance_support))
end

println("Assumption drift next = ", round(drift_next(0.20, 0.08, 0.42, 0.78), digits=6))
