-- quality_dimensions.sql

INSERT INTO quality_dimensions (dimension_id, dimension_name, weight, description)
VALUES
('Q1', 'objective_clarity', 0.16, 'Clarity of decision objectives.'),
('Q2', 'alternative_quality', 0.15, 'Quality and variety of alternatives considered.'),
('Q3', 'information_strength', 0.17, 'Strength and relevance of available evidence.'),
('Q4', 'tradeoff_transparency', 0.18, 'Visibility of competing objectives and sacrifices.'),
('Q5', 'uncertainty_treatment', 0.18, 'Quality of assumptions, risks, scenarios, and unknowns.'),
('Q6', 'implementation_readiness', 0.16, 'Ability to execute the selected action.');
