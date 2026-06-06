-- scenarios.sql

INSERT INTO scenarios (scenario_id, scenario_name, probability, description)
VALUES
('S1', 'baseline_value', 0.35, 'Expected operating value under ordinary use conditions.'),
('S2', 'safety_stress', 0.20, 'Safety or reliability stress scenario.'),
('S3', 'equity_stress', 0.15, 'Distributional fairness or subgroup performance stress scenario.'),
('S4', 'security_stress', 0.15, 'Security, misuse, prompt injection, or data exposure stress scenario.'),
('S5', 'drift_stress', 0.15, 'Model drift, concept drift, scope creep, or vendor update stress scenario.');
