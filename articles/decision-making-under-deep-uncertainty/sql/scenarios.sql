-- scenarios.sql

INSERT INTO scenarios (scenario_id, scenario_name, description)
VALUES
('C1', 'stable_growth', 'Baseline favorable future with stable growth and manageable disruption.'),
('C2', 'fiscal_stress', 'Budget pressure, funding volatility, and resource constraints.'),
('C3', 'climate_disruption', 'Environmental stress, physical risk, and disruption.'),
('C4', 'technology_shift', 'Rapid technology, model, or platform change.'),
('C5', 'governance_breakdown', 'Institutional capacity, legitimacy, or coordination stress.'),
('C6', 'social_contestation', 'Public resistance, stakeholder conflict, or legitimacy challenge.');
