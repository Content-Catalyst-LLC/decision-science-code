-- portfolio_scores.sql

INSERT INTO portfolio_scores (portfolio_id, normal, recession, liquidity_shock, systemic_stress, liquidity_score, governance_score, model_confidence)
VALUES
('P1',-1.2,-4.8,-3.6,-6.2,0.82,0.78,0.74),
('P2',-2.1,-7.3,-8.9,-11.8,0.68,0.72,0.70),
('P3',-3.5,-11.6,-14.2,-19.5,0.48,0.58,0.56),
('P4',-4.8,-15.4,-18.7,-27.4,0.36,0.42,0.46),
('P5',-2.4,-8.6,-16.5,-22.6,0.28,0.54,0.52),
('P6',-1.8,-5.9,-6.8,-9.4,0.76,0.84,0.78);
