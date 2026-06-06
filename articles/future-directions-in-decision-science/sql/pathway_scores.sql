-- pathway_scores.sql

INSERT INTO pathway_scores (pathway_id, ai_readiness, governance_maturity, uncertainty_capability, participatory_legitimacy, reproducibility, systems_modeling, ethical_accountability, adaptive_capacity, process_burden, failure_risk)
VALUES
('F1',0.20,0.46,0.58,0.32,0.48,0.42,0.44,0.40,0.32,0.62),
('F2',0.78,0.54,0.62,0.40,0.62,0.56,0.50,0.54,0.54,0.56),
('F3',0.82,0.86,0.74,0.62,0.78,0.68,0.82,0.74,0.66,0.34),
('F4',0.66,0.78,0.90,0.66,0.74,0.84,0.76,0.90,0.72,0.30),
('F5',0.52,0.76,0.72,0.88,0.68,0.62,0.84,0.76,0.76,0.36),
('F6',0.86,0.90,0.88,0.84,0.88,0.86,0.90,0.88,0.80,0.24);
