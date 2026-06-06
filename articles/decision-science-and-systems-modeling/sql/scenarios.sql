-- scenarios.sql

INSERT INTO scenarios (scenario_id, scenario_name, description)
VALUES
('C1', 'baseline', 'Stable reference future with manageable dynamics.'),
('C2', 'delayed_feedback', 'Future where consequences appear late and early indicators mislead.'),
('C3', 'resource_constraint', 'Future with capacity or resource constraints.'),
('C4', 'shock_event', 'Future with external disruption or sudden system stress.'),
('C5', 'adaptive_resistance', 'Future where actors respond strategically to the intervention.');
