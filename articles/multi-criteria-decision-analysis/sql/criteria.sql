-- criteria.sql

INSERT INTO criteria (criterion_id, criterion_name, direction, description)
VALUES
('C1', 'cost', 'cost', 'Total cost or resource burden.'),
('C2', 'implementation_feasibility', 'benefit', 'Practical ability to implement the alternative.'),
('C3', 'equity', 'benefit', 'Distributional fairness and access.'),
('C4', 'resilience', 'benefit', 'Ability to perform under disruption and change.'),
('C5', 'environmental_benefit', 'benefit', 'Environmental improvement or avoided harm.'),
('C6', 'long_term_value', 'benefit', 'Value over extended time horizons.'),
('C7', 'legitimacy', 'benefit', 'Trust, institutional fit, and stakeholder acceptance.');
