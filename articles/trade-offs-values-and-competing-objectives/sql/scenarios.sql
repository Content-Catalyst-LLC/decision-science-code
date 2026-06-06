-- scenarios.sql

INSERT INTO scenario_weights (scenario_name, objective_id, weight)
VALUES
('efficiency', 'O1', 0.36),
('efficiency', 'O2', 0.10),
('efficiency', 'O3', 0.14),
('efficiency', 'O4', 0.16),
('efficiency', 'O5', 0.12),
('efficiency', 'O6', 0.12),
('equity', 'O1', 0.10),
('equity', 'O2', 0.36),
('equity', 'O3', 0.14),
('equity', 'O4', 0.14),
('equity', 'O5', 0.16),
('equity', 'O6', 0.10);
