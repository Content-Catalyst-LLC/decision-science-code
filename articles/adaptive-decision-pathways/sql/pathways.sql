-- pathways.sql

INSERT INTO pathways (pathway_id, pathway_name, description)
VALUES
('A1', 'Fixed Commitment Path', 'Strong baseline performance but weak flexibility, triggers, and fallback capacity.'),
('A2', 'Wait-and-See Path', 'Preserves flexibility but delays early action and has weak trigger clarity.'),
('A3', 'Low-Regret Initial Action', 'Takes useful early action while preserving future alternatives.'),
('A4', 'Modular Adaptive Path', 'Combines initial action with modularity, monitoring, and strong fallback capacity.'),
('A5', 'Trigger-Based Escalation Path', 'Uses clear thresholds to escalate before adaptation space closes.'),
('A6', 'Portfolio Pathway', 'Maintains a portfolio of pathways and switches based on evidence.');
