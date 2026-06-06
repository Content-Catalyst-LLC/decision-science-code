-- review_triggers.sql

INSERT INTO review_triggers (trigger_id, trigger_name, trigger_value, description)
VALUES
('T1', 'trust_trigger', 0.50, 'Public trust below this level requires review.'),
('T2', 'legitimacy_trigger', 0.56, 'Legitimacy below this level requires review.'),
('T3', 'contestability_trigger', 0.56, 'Contestability below this level requires review.'),
('T4', 'equity_trigger', 0.56, 'Equity review below this level requires review.'),
('T5', 'harm_trigger', 0.62, 'Public harm signal above this level requires review.'),
('T6', 'participation_trigger', 0.55, 'Participation quality below this level requires review.');
