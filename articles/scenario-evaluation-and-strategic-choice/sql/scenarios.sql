-- scenarios.sql

INSERT INTO scenarios (scenario_id, scenario_name, probability, description)
VALUES
('S1', 'high_growth', 0.22, 'Future with strong demand growth and favorable investment conditions.'),
('S2', 'slow_growth', 0.24, 'Future with weak demand growth and moderate constraint.'),
('S3', 'disruption', 0.20, 'Future with shock disruption volatility or operational stress.'),
('S4', 'policy_shift', 0.18, 'Future with regulatory policy or governance change.'),
('S5', 'resource_constraint', 0.16, 'Future with financing capacity labor or material constraint.');
