# treatment_value_model.jl

function treatment_value_score(expected_benefit, adverse_event_risk, cost_burden, patient_preference_fit, equity_score, implementation_feasibility)
    return 0.30 * expected_benefit - 0.18 * adverse_event_risk - 0.14 * cost_burden + 0.18 * patient_preference_fit + 0.10 * equity_score + 0.10 * implementation_feasibility
end

println("Treatment value score = ", round(treatment_value_score(0.72, 0.12, 0.54, 0.88, 0.76, 0.70), digits=6))
