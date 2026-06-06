-- scenarios.sql

INSERT INTO scenarios (scenario_id, scenario_name, description)
VALUES
('S1', 'stable_future', 'Future where existing assumptions remain broadly stable.'),
('S2', 'technology_shift', 'Future where new technology or standards change the value of current commitments.'),
('S3', 'policy_change', 'Future where regulation, governance, or public policy changes.'),
('S4', 'demand_shock', 'Future where demand changes sharply or system stress rises.'),
('S5', 'late_switch_required', 'Future where the current path becomes unacceptable and transition is required.');
