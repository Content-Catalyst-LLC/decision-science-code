# high_performance_bayesian_update.jl

function bayesian_update(prior, sensitivity, false_positive_rate)
    numerator = sensitivity * prior
    denominator = numerator + false_positive_rate * (1.0 - prior)
    return numerator / denominator
end

cases = [
    ("Diagnostic Case", 0.10, 0.86, 0.12),
    ("Model Drift Case", 0.18, 0.78, 0.16),
    ("Policy Pilot Case", 0.35, 0.70, 0.22),
    ("Cybersecurity Case", 0.08, 0.82, 0.10),
    ("Infrastructure Case", 0.22, 0.74, 0.18)
]

for (name, prior, sensitivity, false_positive_rate) in cases
    posterior = bayesian_update(prior, sensitivity, false_positive_rate)
    println(name, " posterior = ", round(posterior, digits=6))
end
