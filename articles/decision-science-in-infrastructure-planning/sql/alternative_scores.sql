-- alternative_scores.sql

INSERT INTO alternative_scores (alternative_id, baseline, climate_stress, demand_growth, funding_constraint, disruption, lifecycle_cost, equity_score, resilience_score, environmental_score, implementation_feasibility, adaptability)
VALUES
('A1',62,44,50,78,46,0.38,0.52,0.46,0.50,0.82,0.40),
('A2',72,68,66,72,70,0.56,0.66,0.72,0.64,0.74,0.62),
('A3',78,58,88,48,54,0.88,0.48,0.58,0.42,0.48,0.36),
('A4',76,76,82,70,78,0.66,0.74,0.84,0.76,0.66,0.90),
('A5',70,82,62,76,80,0.58,0.82,0.88,0.92,0.70,0.78),
('A6',74,72,80,74,76,0.62,0.78,0.80,0.78,0.68,0.84);
