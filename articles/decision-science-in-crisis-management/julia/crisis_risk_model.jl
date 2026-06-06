function crisis_risk(likelihood, severity, exposure, vulnerability, criticality)
    return likelihood * severity * exposure * vulnerability * criticality
end

println("Crisis risk = ", round(crisis_risk(0.72, 0.86, 0.68, 0.62, 0.90), digits=6))
