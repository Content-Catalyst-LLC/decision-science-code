-- hypotheses.sql

INSERT INTO hypotheses (hypothesis_id, case_name, hypothesis_name, description)
VALUES
(1, 'Diagnostic Case', 'condition present', 'A clinical-style condition is present'),
(2, 'Model Drift Case', 'model drift present', 'A deployed model has drifted enough to require action'),
(3, 'Policy Pilot Case', 'policy effect present', 'A pilot program has a positive implementation effect'),
(4, 'Cybersecurity Case', 'intrusion present', 'A security alert reflects a real intrusion'),
(5, 'Infrastructure Case', 'asset failure risk elevated', 'Inspection anomaly indicates elevated asset risk');
