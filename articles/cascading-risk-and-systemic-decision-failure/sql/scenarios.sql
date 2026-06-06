-- scenarios.sql

INSERT INTO scenarios (scenario_id, scenario_name, description)
VALUES
('S1', 'baseline', 'Ordinary operating conditions with no major disruption.'),
('S2', 'local_disruption', 'Failure begins in one node or component.'),
('S3', 'common_mode_shock', 'Shared stress affects multiple components simultaneously.'),
('S4', 'demand_surge', 'External demand or load increases sharply across the system.'),
('S5', 'delayed_response', 'Early warning is missed and escalation occurs late.');
