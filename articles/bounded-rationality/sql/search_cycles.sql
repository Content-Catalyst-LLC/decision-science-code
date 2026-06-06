-- search_cycles.sql

INSERT INTO search_cycles (cycle, domain, aspiration, search_cost_per_option, n_options, time_limit)
VALUES
(1, 'Public Policy', 0.68, 0.020, 8, 30),
(2, 'Healthcare', 0.72, 0.015, 10, 20),
(3, 'Financial Risk', 0.70, 0.018, 12, 15),
(4, 'Infrastructure', 0.74, 0.025, 9, 60),
(5, 'AI Governance', 0.71, 0.022, 11, 25);
