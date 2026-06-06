# adaptive_pathway_model.jl

function adaptive_growth(base_return, regime_shift, shock, adaptability, resilience)
    return base_return + regime_shift + shock + 0.8 * adaptability + 0.6 * resilience
end

println("Adaptive growth = ", round(adaptive_growth(1.25, -1.0, 0.4, 1.5, 1.0), digits=6))
