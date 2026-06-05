# trigger_threshold_simulation.jl

signals = [
    ("model_drift", 0.34, 0.0, 0.30),
    ("cost_escalation", 0.12, 0.0, 0.15),
    ("adverse_event_rate", 0.05, 0.0, 0.04),
    ("market_growth", 0.04, 0.06, 0.16)
]

for (name, value, lower, upper) in signals
    active = value < lower || value > upper
    println(name, " review trigger active = ", active)
end
