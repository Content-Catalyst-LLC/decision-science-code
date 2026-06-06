-- evidence_signals.sql

INSERT INTO evidence_signals (signal_id, domain, signal_type, reliability, diagnostic_strength, description)
VALUES
('S1', 'Public Policy', 'early warning indicator', 0.68, 0.52, 'partial signal from monitored public system'),
('S2', 'Healthcare', 'test result', 0.90, 0.78, 'high-quality clinical signal'),
('S3', 'Financial Risk', 'market anomaly', 0.62, 0.45, 'ambiguous risk signal under volatility'),
('S4', 'Infrastructure', 'asset condition signal', 0.74, 0.60, 'maintenance and condition-monitoring evidence'),
('S5', 'AI Governance', 'model drift signal', 0.70, 0.58, 'performance drift and subgroup error evidence');
