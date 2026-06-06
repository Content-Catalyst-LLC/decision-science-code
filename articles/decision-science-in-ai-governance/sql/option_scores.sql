-- option_scores.sql

INSERT INTO option_scores (option_id, baseline_value, safety_stress, equity_stress, security_stress, drift_stress, evidence_quality, oversight_strength, equity_score, transparency_score, security_readiness, implementation_feasibility)
VALUES
('O1',35,80,78,82,84,0.90,0.88,0.86,0.82,0.90,0.92),
('O2',68,70,74,72,76,0.72,0.84,0.78,0.76,0.74,0.70),
('O3',74,62,60,64,58,0.66,0.68,0.64,0.66,0.68,0.76),
('O4',84,42,38,46,40,0.48,0.46,0.42,0.44,0.48,0.56),
('O5',70,58,56,60,54,0.62,0.62,0.58,0.60,0.64,0.68),
('O6',78,76,80,78,82,0.76,0.82,0.80,0.78,0.82,0.72);
