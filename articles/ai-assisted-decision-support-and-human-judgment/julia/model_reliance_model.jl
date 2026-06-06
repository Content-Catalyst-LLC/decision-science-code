# model_reliance_model.jl

function justified_model_reliance(evidence_quality, calibration, decision_risk, uncertainty)
    return max(0.0, min(1.0, 0.35 * evidence_quality + 0.35 * calibration - 0.16 * decision_risk - 0.14 * uncertainty))
end

println("Justified model reliance = ", round(justified_model_reliance(0.82, 0.78, 0.54, 0.36), digits=6))
