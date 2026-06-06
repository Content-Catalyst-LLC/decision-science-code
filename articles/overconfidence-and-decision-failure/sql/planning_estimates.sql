-- planning_estimates.sql

INSERT INTO planning_estimates (case_id, domain, estimated_duration, actual_duration, estimated_cost, actual_cost)
VALUES
(1, 'Public Policy', 120, 154, 850000, 1050000),
(2, 'Healthcare', 90, 96, 500000, 540000),
(3, 'Financial Risk', 45, 58, 250000, 315000),
(4, 'Infrastructure', 365, 520, 5000000, 7200000),
(5, 'AI Governance', 180, 250, 1200000, 1680000);
