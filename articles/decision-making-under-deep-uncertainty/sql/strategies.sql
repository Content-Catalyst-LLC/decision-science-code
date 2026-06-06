-- strategies.sql

INSERT INTO strategies (strategy_id, strategy_name, base_return, volatility, adaptability, resilience, description)
VALUES
('S1', 'Aggressive Commitment', 1.90, 4.40, 0.30, 0.20, 'High commitment strategy with high upside and substantial downside exposure.'),
('S2', 'Balanced Adaptive Strategy', 1.40, 2.70, 1.20, 0.80, 'Moderate strategy designed to adapt under shifting conditions.'),
('S3', 'Defensive Resilience Strategy', 1.00, 1.90, 0.90, 1.20, 'Lower upside strategy emphasizing downside protection.'),
('S4', 'Staged Optionality Strategy', 1.30, 2.40, 1.40, 1.00, 'Sequenced strategy preserving options and triggers.'),
('S5', 'Modular No-Regrets Strategy', 1.15, 2.10, 1.10, 1.10, 'Modular strategy with broad acceptable performance.'),
('S6', 'Learning Portfolio Strategy', 1.25, 2.30, 1.50, 1.00, 'Portfolio approach emphasizing learning and revision.');
