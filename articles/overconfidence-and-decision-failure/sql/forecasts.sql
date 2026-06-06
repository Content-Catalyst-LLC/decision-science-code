-- forecasts.sql

INSERT INTO forecasts (forecast_id, domain, forecast_probability, confidence, outcome, evidence_quality)
VALUES
('F1', 'Public Policy', 0.62, 0.78, 1, 'medium'),
('F2', 'Healthcare', 0.82, 0.90, 1, 'high'),
('F3', 'Financial Risk', 0.44, 0.72, 0, 'medium'),
('F4', 'Infrastructure', 0.56, 0.76, 1, 'medium'),
('F5', 'AI Governance', 0.69, 0.88, 0, 'low');
