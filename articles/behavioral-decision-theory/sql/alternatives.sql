-- alternatives.sql

INSERT INTO alternatives (alternative_id, domain, option_name, reference_point, description)
VALUES
('A1', 'Public Policy', 'Status Quo', 0, 'current policy baseline'),
('A2', 'Healthcare', 'Cautious Alternative', 0, 'lower-risk clinical option'),
('A3', 'Financial Risk', 'High-Upside Alternative', 100, 'high-upside option with downside exposure'),
('A4', 'Infrastructure', 'Loss-Avoidance Alternative', -100, 'option framed around avoiding deterioration'),
('A5', 'AI Governance', 'Balanced Alternative', 0, 'moderate-governance deployment option');
