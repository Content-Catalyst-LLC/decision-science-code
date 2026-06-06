-- confidence_estimates.sql

INSERT INTO confidence_estimates (case_id, domain, confidence, accuracy_proxy, confidence_source)
VALUES
(1, 'Public Policy', 0.78, 0.86, 'expert judgment'),
(2, 'Healthcare', 0.90, 0.97, 'clinical review'),
(3, 'Financial Risk', 0.72, 0.81, 'forecast model'),
(4, 'Infrastructure', 0.76, 0.69, 'project team'),
(5, 'AI Governance', 0.88, 0.52, 'automated score');
