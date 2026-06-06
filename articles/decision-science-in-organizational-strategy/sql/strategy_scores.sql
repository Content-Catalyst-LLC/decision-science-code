-- strategy_scores.sql

INSERT INTO strategy_scores (strategy_id, low_growth, base_case, high_growth, disruption, adaptability, capability_fit, governance_feasibility, reversibility)
VALUES
('S1',72,84,91,48,0.42,0.86,0.78,0.58),
('S2',68,82,89,66,0.84,0.72,0.70,0.82),
('S3',40,88,118,32,0.48,0.44,0.46,0.30),
('S4',62,79,92,76,0.90,0.70,0.66,0.64),
('S5',64,81,96,70,0.74,0.68,0.72,0.70),
('S6',70,78,86,82,0.82,0.76,0.80,0.74);
