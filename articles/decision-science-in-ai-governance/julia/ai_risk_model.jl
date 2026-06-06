# ai_risk_model.jl

function composite_ai_risk(safety, equity, bias, privacy, opacity, security)
    return 0.20 * safety + 0.18 * equity + 0.16 * bias + 0.16 * privacy + 0.14 * opacity + 0.16 * security
end

println("Composite AI risk = ", round(composite_ai_risk(0.52, 0.48, 0.50, 0.42, 0.55, 0.46), digits=6))
