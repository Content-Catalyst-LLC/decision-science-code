-- thresholds.sql

INSERT INTO thresholds (domain, decision_context, probability_threshold, false_positive_cost, false_negative_cost, review_owner)
VALUES
('Public Policy', 'scale or revise intervention', 0.62, 18, 55, 'policy review group'),
('Healthcare', 'treat or monitor patient risk', 0.55, 24, 80, 'clinical review lead'),
('Financial Risk', 'escalate risk controls', 0.35, 12, 70, 'risk committee'),
('Infrastructure', 'prioritize investment or inspection', 0.50, 28, 65, 'infrastructure planning lead'),
('AI Governance', 'audit or retrain model', 0.45, 15, 85, 'model governance lead');
