-- scenarios.sql

INSERT INTO scenarios (scenario_id, scenario_name, description)
VALUES
('C1', 'stable_conditions', 'Baseline future with stable system behavior and manageable disruption.'),
('C2', 'delayed_feedback', 'Future where delayed consequences dominate early performance signals.'),
('C3', 'coordination_stress', 'Future where implementation depends on cross-system coordination.'),
('C4', 'shock_event', 'Future with external disruption or sudden system stress.'),
('C5', 'adaptive_resistance', 'Future where actors respond strategically to the intervention.');
