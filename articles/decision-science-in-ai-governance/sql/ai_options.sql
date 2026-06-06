-- ai_options.sql

INSERT INTO ai_options (option_id, option_name, description)
VALUES
('O1', 'Reject Use Case', 'Rejects deployment and avoids AI-specific harms but forgoes operational value.'),
('O2', 'Pilot With Strong Controls', 'Limited pilot with strong safeguards, validation, monitoring, and review authority.'),
('O3', 'Limited Internal Deployment', 'Internal deployment with moderate safeguards and operational value.'),
('O4', 'High-Stakes Deployment', 'High-value high-stakes deployment with weak controls and unacceptable stress performance.'),
('O5', 'Vendor Tool With Audit Rights', 'Vendor system with some governance rights but unresolved stress and drift concerns.'),
('O6', 'Adaptive Governance Rollout', 'Staged rollout with monitoring thresholds, escalation controls, and adaptive safeguards.');
