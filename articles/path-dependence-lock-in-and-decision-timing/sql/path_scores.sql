-- path_scores.sql

INSERT INTO path_scores (path_id, initial_value, future_flexibility, switching_cost, lock_in_risk, reversibility, timing_sensitivity)
VALUES
('P1',0.78,0.32,0.74,0.81,0.26,0.69),
('P2',0.62,0.84,0.30,0.34,0.80,0.72),
('P3',0.74,0.82,0.42,0.38,0.78,0.48),
('P4',0.66,0.28,0.68,0.76,0.24,0.57),
('P5',0.70,0.58,0.61,0.58,0.52,0.81),
('P6',0.72,0.88,0.36,0.29,0.86,0.45);
