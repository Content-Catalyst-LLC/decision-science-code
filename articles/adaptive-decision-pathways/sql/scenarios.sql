-- scenarios.sql

INSERT INTO scenarios (scenario_id, scenario_name, description)
VALUES
('S1', 'baseline', 'Ordinary conditions where initial assumptions broadly hold.'),
('S2', 'accelerating_risk', 'Future where risk increases faster than expected.'),
('S3', 'cost_pressure', 'Future where costs rise and fiscal constraints tighten.'),
('S4', 'technology_shift', 'Future where new technology or standards change the option set.'),
('S5', 'stakeholder_conflict', 'Future where legitimacy, values, and distributional concerns intensify.');
