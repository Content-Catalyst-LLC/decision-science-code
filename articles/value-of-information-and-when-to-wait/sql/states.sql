-- states.sql

INSERT INTO states (state_id, state_name, prior_probability, description)
VALUES
('S1', 'stable_growth', 0.35, 'Favorable conditions with stable growth and manageable disruption.'),
('S2', 'adverse_conditions', 0.25, 'Conditions worsen through cost pressure, risk, or operational stress.'),
('S3', 'disruptive_shift', 0.20, 'Rapid change makes flexible or adaptive strategies more valuable.'),
('S4', 'delayed_window', 0.20, 'Waiting causes opportunity loss and narrows the action window.');
