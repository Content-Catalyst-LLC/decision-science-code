-- bias_profiles.sql

INSERT INTO bias_profiles (bias_profile, primary_mechanism, typical_distortion, review_priority)
VALUES
('availability', 'salience weighting', 'memorable cases inflate perceived likelihood', 'high'),
('representativeness', 'similarity substitution', 'base rates and sample size are underweighted', 'high'),
('anchoring', 'initial-value dependence', 'estimates remain too close to early numbers', 'high'),
('confirmation', 'asymmetric evidence weighting', 'confirming evidence is overweighted', 'high'),
('overconfidence', 'confidence inflation', 'confidence exceeds calibration or evidence quality', 'high'),
('balanced', 'low distortion', 'evidence and confidence remain close to calibrated estimates', 'low');
