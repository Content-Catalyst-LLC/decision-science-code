-- process_scores.sql

INSERT INTO process_scores (process_id, evidence_quality, transparency, participation, procedural_fairness, contestability, equity_review, accountability, uncertainty_communication, process_burden, public_trust_risk)
VALUES
('P1',0.78,0.44,0.22,0.42,0.36,0.48,0.46,0.52,0.24,0.68),
('P2',0.62,0.68,0.58,0.58,0.64,0.56,0.60,0.58,0.46,0.54),
('P3',0.70,0.70,0.68,0.66,0.68,0.72,0.66,0.66,0.56,0.46),
('P4',0.78,0.82,0.82,0.84,0.78,0.76,0.74,0.78,0.72,0.34),
('P5',0.64,0.76,0.86,0.78,0.72,0.78,0.72,0.62,0.64,0.38),
('P6',0.84,0.88,0.88,0.88,0.86,0.86,0.88,0.86,0.76,0.28);
