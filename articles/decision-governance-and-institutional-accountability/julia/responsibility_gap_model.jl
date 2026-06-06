# responsibility_gap_model.jl

function responsibility_gap(decision_influence, accountability)
    return max(0.0, decision_influence - accountability)
end

println("Responsibility gap = ", round(responsibility_gap(0.62, 0.34), digits=6))
