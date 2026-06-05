# assumption_risk_frontier.jl

assumptions = [
    ("A1", 0.62, 0.86),
    ("A3", 0.68, 0.78),
    ("A7", 0.42, 0.90),
    ("A8", 0.38, 0.84),
    ("A9", 0.72, 0.88)
]

for (id, confidence, criticality) in assumptions
    risk = criticality * (1.0 - confidence)
    println(id, " assumption risk = ", round(risk, digits=4))
end
