-- review_triggers.sql

INSERT INTO review_triggers (trigger_id, trigger_name, trigger_value, description)
VALUES
('T1', 'uncertainty_trigger', 0.62, 'Model uncertainty above this level requires review.'),
('T2', 'oversight_trigger', 0.58, 'Human oversight below this level requires review.'),
('T3', 'automation_bias_trigger', 0.62, 'Automation-bias risk above this level requires review.'),
('T4', 'contestability_trigger', 0.56, 'Contestability below this level requires review.'),
('T5', 'fairness_risk_trigger', 0.60, 'Fairness risk above this level requires review.'),
('T6', 'accountability_trigger', 0.58, 'Accountability below this level requires review.');
