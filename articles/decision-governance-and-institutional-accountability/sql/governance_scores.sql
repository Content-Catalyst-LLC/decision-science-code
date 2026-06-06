-- governance_scores.sql

INSERT INTO governance_scores (design_id, decision_quality, legitimacy, accountability, implementation_reliability, evidence_traceability, review_strength, monitoring_strength, corrective_capacity, risk_exposure, process_burden)
VALUES
('G1',0.52,0.46,0.40,0.58,0.44,0.36,0.38,0.34,0.72,0.20),
('G2',0.66,0.62,0.58,0.62,0.60,0.62,0.54,0.50,0.58,0.46),
('G3',0.78,0.74,0.76,0.74,0.78,0.76,0.72,0.72,0.40,0.56),
('G4',0.82,0.78,0.82,0.70,0.82,0.90,0.70,0.78,0.36,0.66),
('G5',0.76,0.76,0.86,0.78,0.88,0.80,0.82,0.82,0.34,0.62),
('G6',0.86,0.84,0.90,0.84,0.86,0.88,0.90,0.92,0.30,0.68);
