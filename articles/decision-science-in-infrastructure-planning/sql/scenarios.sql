-- scenarios.sql

INSERT INTO scenarios (scenario_id, scenario_name, probability, description)
VALUES
('S1', 'baseline', 0.30, 'Ordinary conditions where assumptions broadly hold.'),
('S2', 'climate_stress', 0.20, 'Climate stress involving heat, flooding, storms, drought, wildfire, or service disruption.'),
('S3', 'demand_growth', 0.20, 'Higher service demand due to population, economic, or land-use change.'),
('S4', 'funding_constraint', 0.15, 'Reduced fiscal flexibility or capital availability.'),
('S5', 'disruption', 0.15, 'Technology, supply-chain, governance, cyber, or operational disruption.');
