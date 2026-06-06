-- system_scores.sql

INSERT INTO system_scores (system_id, exposure, dependency_centrality, buffer_weakness, common_mode_risk, monitoring_quality, response_capacity)
VALUES
('C1',0.82,0.88,0.76,0.79,0.42,0.40),
('C2',0.46,0.38,0.28,0.34,0.78,0.80),
('C3',0.78,0.72,0.83,0.74,0.38,0.35),
('C4',0.42,0.44,0.24,0.30,0.82,0.84),
('C5',0.69,0.76,0.66,0.62,0.46,0.44),
('C6',0.50,0.48,0.36,0.40,0.86,0.82);
