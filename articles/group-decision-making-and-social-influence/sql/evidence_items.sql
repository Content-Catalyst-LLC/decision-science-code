-- evidence_items.sql

INSERT INTO evidence_items (evidence_id, group_id, evidence_type, shared_status, quality, description)
VALUES
('E1', 1, 'base rate', 'shared', 'high', 'reference-class evidence available to all members'),
('E2', 1, 'implementation signal', 'unique', 'medium', 'operational concern known by one role'),
('E3', 1, 'stakeholder impact', 'unique', 'medium', 'distributional concern held by stakeholder representative'),
('E4', 1, 'forecast', 'shared', 'medium', 'forecast used in group discussion'),
('E5', 1, 'warning signal', 'unique', 'low', 'early indicator requiring review');
