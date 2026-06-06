-- scenarios.sql

INSERT INTO scenarios (scenario_id, scenario_name, description)
VALUES
('S1', 'baseline', 'Ordinary patient conditions where assumptions broadly hold.'),
('S2', 'high_risk_patient', 'Patient context where adverse-event risk and comorbidity are more salient.'),
('S3', 'resource_constraint', 'Clinical setting with limited staff capacity, cost pressure, or availability constraints.'),
('S4', 'preference_conflict', 'Patient values differ from average clinical recommendation.'),
('S5', 'followup_uncertainty', 'Future where monitoring continuity and follow-up reliability are uncertain.');
