-- scenarios.sql

INSERT INTO scenarios (scenario_id, scenario_name, description)
VALUES
('S1', 'baseline', 'Reference case with manageable system behavior.'),
('S2', 'delayed_feedback', 'Future where lagged consequences dominate early signals.'),
('S3', 'resistance_escalation', 'Future where system counter-response intensifies.'),
('S4', 'capacity_constraint', 'Future where implementation capacity limits policy effect.'),
('S5', 'adaptive_revision', 'Future where monitoring and revision improve performance.');
