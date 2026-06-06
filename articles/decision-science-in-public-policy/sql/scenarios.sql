-- scenarios.sql

INSERT INTO scenarios (scenario_id, scenario_name, description)
VALUES
('S1', 'baseline', 'Ordinary conditions where policy assumptions broadly hold.'),
('S2', 'fiscal_constraint', 'Future where budgets tighten and implementation costs matter more.'),
('S3', 'public_trust_decline', 'Future where legitimacy and public cooperation weaken.'),
('S4', 'demand_surge', 'Future where demand for public services rises sharply.'),
('S5', 'implementation_stress', 'Future where administrative capacity is strained.');
