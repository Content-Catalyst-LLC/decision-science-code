-- treatment_scores.sql

INSERT INTO treatment_scores (treatment_id, expected_benefit, adverse_event_risk, cost_burden, patient_preference_fit, equity_score, implementation_feasibility)
VALUES
('T1',0.68,0.14,0.48,0.61,0.64,0.78),
('T2',0.79,0.26,0.82,0.55,0.50,0.52),
('T3',0.52,0.08,0.31,0.72,0.58,0.82),
('T4',0.72,0.12,0.54,0.88,0.76,0.70),
('T5',0.70,0.13,0.58,0.80,0.86,0.66),
('T6',0.60,0.09,0.40,0.76,0.68,0.74);
