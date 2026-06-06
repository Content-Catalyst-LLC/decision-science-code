-- design_scores.sql

INSERT INTO design_scores (design_id, model_performance, uncertainty_visibility, human_oversight, contestability, fairness_review, accountability, monitoring_strength, automation_bias_risk, process_burden)
VALUES
('S1',0.00,0.42,0.88,0.62,0.54,0.62,0.44,0.18,0.30),
('S2',0.66,0.72,0.84,0.72,0.66,0.72,0.62,0.26,0.42),
('S3',0.78,0.66,0.72,0.66,0.70,0.70,0.70,0.46,0.54),
('S4',0.80,0.70,0.68,0.82,0.78,0.80,0.78,0.42,0.62),
('S5',0.84,0.48,0.36,0.40,0.46,0.44,0.70,0.72,0.48),
('S6',0.82,0.86,0.88,0.86,0.84,0.90,0.90,0.28,0.68);
