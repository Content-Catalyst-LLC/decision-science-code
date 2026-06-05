-- strategies.sql

INSERT INTO strategies (strategy_name, mean_return, volatility, shock_probability, shock_size, recovery_credit, description)
VALUES
('Conservative Strategy', 0.035, 0.025, 0.010, -0.045, 0.010, 'Low volatility and limited shock exposure'),
('Balanced Strategy', 0.065, 0.070, 0.025, -0.100, 0.015, 'Higher average return with moderate downside exposure'),
('High-Risk Strategy', 0.105, 0.165, 0.055, -0.260, 0.000, 'High mean return paired with severe tail exposure'),
('Adaptive Strategy', 0.075, 0.090, 0.030, -0.140, 0.030, 'Moderate upside with adaptive recovery capacity'),
('Resilient Strategy', 0.060, 0.050, 0.015, -0.070, 0.045, 'Moderate return with stronger recovery and downside protection');
