-- scenarios.sql

INSERT INTO scenarios (scenario_id, scenario_name, weight, description)
VALUES
('C1', 'stable_growth', 0.18, 'Baseline favorable future with stable growth and manageable disruption.'),
('C2', 'fiscal_stress', 0.16, 'Budget pressure, funding volatility, and resource constraints.'),
('C3', 'climate_disruption', 0.18, 'Environmental stress, physical risk, and disruption.'),
('C4', 'technology_shift', 0.17, 'Rapid technology, model, or platform change.'),
('C5', 'governance_stress', 0.15, 'Institutional capacity, legitimacy, or coordination stress.'),
('C6', 'social_contestation', 0.16, 'Public resistance, stakeholder conflict, or legitimacy challenge.');
