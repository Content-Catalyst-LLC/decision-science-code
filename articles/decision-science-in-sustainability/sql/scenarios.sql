-- scenarios.sql

INSERT INTO scenarios (scenario_id, scenario_name, description)
VALUES
('C1', 'baseline', 'Ordinary conditions where sustainability assumptions broadly hold.'),
('C2', 'climate_stress', 'Future where climate pressure accelerates and resilience becomes critical.'),
('C3', 'cost_pressure', 'Future where costs rise and affordability constraints intensify.'),
('C4', 'technology_shift', 'Future where new technologies or standards change the option set.'),
('C5', 'equity_conflict', 'Future where distributional conflict and legitimacy concerns intensify.');
