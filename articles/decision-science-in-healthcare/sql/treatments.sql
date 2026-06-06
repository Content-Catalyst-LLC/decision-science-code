-- treatments.sql

INSERT INTO treatments (treatment_id, treatment_name, description)
VALUES
('T1', 'Standard Therapy', 'Common baseline treatment with moderate preference fit and strong feasibility.'),
('T2', 'Aggressive Therapy', 'High expected benefit but higher adverse-event risk, cost, and implementation constraints.'),
('T3', 'Conservative Management', 'Lower-risk lower-cost management pathway with lower expected benefit.'),
('T4', 'Shared-Decision Pathway', 'Preference-sensitive pathway with strong patient alignment.'),
('T5', 'Equity-Sensitive Care Pathway', 'Care pathway designed to improve access, equity, and follow-up reliability.'),
('T6', 'Monitoring-First Strategy', 'Staged monitoring strategy that preserves flexibility and lowers immediate risk.');
