-- stopping_rules.sql

INSERT INTO stopping_rules (rule_id, rule_name, description, primary_risk)
VALUES
('SR1', 'first_acceptable', 'Stop when first option meets aspiration threshold', 'search-order bias'),
('SR2', 'deadline', 'Stop when deadline arrives', 'inadequate evidence'),
('SR3', 'marginal_value', 'Stop when expected improvement is lower than search cost', 'misestimated value of information'),
('SR4', 'min_option_set', 'Stop after reviewing a minimum number of alternatives', 'missed unconventional alternatives'),
('SR5', 'confidence_threshold', 'Stop when confidence threshold is reached', 'overconfidence');
