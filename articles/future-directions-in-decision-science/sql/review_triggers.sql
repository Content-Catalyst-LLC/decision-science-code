-- review_triggers.sql

INSERT INTO review_triggers (trigger_id, trigger_name, trigger_value, description)
VALUES
('T1', 'governance_trigger', 0.58, 'Governance maturity below this level requires review.'),
('T2', 'uncertainty_trigger', 0.58, 'Uncertainty capability below this level requires review.'),
('T3', 'ethics_trigger', 0.58, 'Ethical accountability below this level requires review.'),
('T4', 'adaptive_trigger', 0.58, 'Adaptive capacity below this level requires review.'),
('T5', 'failure_risk_trigger', 0.62, 'Failure risk above this level requires review.'),
('T6', 'legitimacy_trigger', 0.58, 'Stakeholder legitimacy below this level requires review.');
