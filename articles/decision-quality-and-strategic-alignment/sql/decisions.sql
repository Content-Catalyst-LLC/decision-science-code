-- decisions.sql

INSERT INTO decisions (
    decision_id,
    decision_name,
    objective_clarity,
    alternative_quality,
    information_strength,
    tradeoff_transparency,
    uncertainty_treatment,
    implementation_readiness,
    strategic_fit,
    capability_fit,
    value_fit
)
VALUES
('D1', 'Fast Growth Allocation', 0.58, 0.49, 0.55, 0.42, 0.45, 0.72, 0.46, 0.52, 0.44),
('D2', 'Balanced Strategic Investment', 0.81, 0.77, 0.79, 0.80, 0.76, 0.78, 0.84, 0.81, 0.82),
('D3', 'Risk-Controlled Expansion', 0.74, 0.72, 0.76, 0.83, 0.86, 0.75, 0.79, 0.77, 0.76),
('D4', 'Mission-Aligned Capability Build', 0.89, 0.84, 0.73, 0.78, 0.74, 0.82, 0.91, 0.88, 0.93),
('D5', 'Efficiency Consolidation', 0.67, 0.61, 0.69, 0.58, 0.52, 0.88, 0.62, 0.66, 0.59),
('D6', 'Adaptive Learning Portfolio', 0.86, 0.88, 0.82, 0.86, 0.89, 0.77, 0.88, 0.90, 0.87);
