-- scores.sql

INSERT INTO scores (alternative_id, criterion_id, raw_score, normalized_score, evidence_quality)
VALUES
('A1', 'C1', 68, 0.725, 'medium'),
('A1', 'C2', 0.86, 0.849, 'medium'),
('A1', 'C3', 0.36, 0.000, 'medium'),
('A2', 'C1', 82, 0.451, 'high'),
('A2', 'C3', 0.72, 0.621, 'high'),
('A3', 'C3', 0.94, 1.000, 'medium'),
('A4', 'C4', 0.95, 1.000, 'high'),
('A6', 'C6', 0.89, 0.977, 'medium');
