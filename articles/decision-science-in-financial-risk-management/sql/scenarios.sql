-- scenarios.sql

INSERT INTO scenarios (scenario_id, scenario_name, probability, description)
VALUES
('S1', 'normal', 0.55, 'Ordinary market conditions with moderate losses.'),
('S2', 'recession', 0.20, 'Macroeconomic slowdown with credit and earnings pressure.'),
('S3', 'liquidity_shock', 0.15, 'Funding closure and market-depth stress.'),
('S4', 'systemic_stress', 0.10, 'Broad system stress with correlation convergence and capital pressure.');
