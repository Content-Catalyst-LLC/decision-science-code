-- evidence.sql

INSERT INTO evidence_posteriors (evidence_name, evidence_probability, state_id, posterior_probability)
VALUES
('reassuring_signal',0.40,'S1',0.58),
('reassuring_signal',0.40,'S2',0.18),
('reassuring_signal',0.40,'S3',0.10),
('reassuring_signal',0.40,'S4',0.14),
('warning_signal',0.35,'S1',0.18),
('warning_signal',0.35,'S2',0.46),
('warning_signal',0.35,'S3',0.18),
('warning_signal',0.35,'S4',0.18),
('disruption_signal',0.25,'S1',0.12),
('disruption_signal',0.25,'S2',0.18),
('disruption_signal',0.25,'S3',0.52),
('disruption_signal',0.25,'S4',0.18);
