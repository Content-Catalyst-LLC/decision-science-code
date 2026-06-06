-- review_triggers.sql

INSERT INTO review_triggers (trigger_id, trigger_name, trigger_value, description)
VALUES
('T1', 'accountability_trigger', 0.56, 'Accountability below this level requires review.'),
('T2', 'traceability_trigger', 0.58, 'Evidence traceability below this level requires review.'),
('T3', 'review_trigger', 0.58, 'Review strength below this level requires review.'),
('T4', 'responsibility_gap_trigger', 0.28, 'Influence exceeding accountability by this amount requires review.'),
('T5', 'risk_trigger', 0.68, 'Risk exposure above this level requires review.'),
('T6', 'process_burden_trigger', 0.75, 'Process burden above this level requires governance redesign.');
