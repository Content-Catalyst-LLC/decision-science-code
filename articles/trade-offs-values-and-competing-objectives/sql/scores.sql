-- scores.sql

INSERT INTO scores (alternative_id, objective_id, score, evidence_quality)
VALUES
('A1', 'O1', 0.90, 'medium'),
('A1', 'O2', 0.38, 'medium'),
('A1', 'O3', 0.42, 'medium'),
('A2', 'O1', 0.74, 'high'),
('A2', 'O2', 0.72, 'high'),
('A2', 'O3', 0.76, 'high'),
('A3', 'O2', 0.91, 'medium'),
('A4', 'O3', 0.93, 'high'),
('A6', 'O4', 0.91, 'medium'),
('A6', 'O6', 0.90, 'medium');
