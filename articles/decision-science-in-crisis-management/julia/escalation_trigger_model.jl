function escalation_required(risk, uncertainty, public_trust, resource_pressure, cascading_impact)
    return risk >= 0.72 || uncertainty >= 0.62 || public_trust <= 0.46 || resource_pressure >= 0.70 || cascading_impact >= 0.64
end

println("Escalation required = ", escalation_required(0.68, 0.64, 0.55, 0.61, 0.58))
