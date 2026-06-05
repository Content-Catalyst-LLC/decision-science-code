-- alternatives.sql
-- Example inserts for alternatives.

INSERT INTO alternatives (alternative_name, strategy_type, implementation_capacity, evidence_quality, legitimacy)
VALUES
('Optimize', 'formal expected-utility strategy', 0.55, 0.68, 0.48),
('Balanced', 'mixed strategy', 0.72, 0.78, 0.66),
('Robust', 'robust decision-science strategy', 0.82, 0.84, 0.76),
('Adaptive', 'adaptive pathway strategy', 0.74, 0.80, 0.82),
('Staged Pilot', 'bounded and staged learning strategy', 0.88, 0.92, 0.86);
