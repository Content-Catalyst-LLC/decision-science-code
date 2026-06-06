-- scenarios.sql

INSERT INTO scenarios (scenario_id, scenario_name, description)
VALUES
('S1', 'stable_future', 'Future with manageable stress and stable institutional conditions.'),
('S2', 'climate_stress', 'Future with increased climate exposure and chronic stress.'),
('S3', 'funding_constraint', 'Future with fiscal or resource constraints.'),
('S4', 'institutional_drift', 'Future with governance turnover, weakened memory, or policy drift.'),
('S5', 'shock_event', 'Future with acute disruption or cascading stress.');
