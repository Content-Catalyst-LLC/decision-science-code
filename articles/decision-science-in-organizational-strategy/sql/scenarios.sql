-- scenarios.sql

INSERT INTO scenarios (scenario_id, scenario_name, probability, description)
VALUES
('C1', 'low_growth', 0.25, 'Weak demand and slower market expansion.'),
('C2', 'base_case', 0.35, 'Ordinary conditions where assumptions broadly hold.'),
('C3', 'high_growth', 0.20, 'Upside environment where demand and adoption accelerate.'),
('C4', 'disruption', 0.20, 'Competitive, technological, regulatory, or operating disruption.');
