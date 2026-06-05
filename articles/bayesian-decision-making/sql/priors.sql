-- priors.sql

INSERT INTO priors (hypothesis_id, prior_probability, prior_type, source, confidence)
VALUES
(1, 0.10, 'empirical', 'base rate and patient context', 0.72),
(2, 0.18, 'monitoring', 'prior monitoring history', 0.64),
(3, 0.35, 'expert', 'expert elicitation and prior studies', 0.58),
(4, 0.08, 'empirical', 'alert history and base rates', 0.62),
(5, 0.22, 'inspection', 'asset history and inspection context', 0.67);
