-- framing_cases.sql

INSERT INTO framing_cases (
    case_id,
    domain,
    reference_point,
    sure_outcome,
    risky_high_outcome,
    risky_high_probability,
    loss_aversion,
    alpha,
    beta
)
VALUES
(1, 'Healthcare', 0, 120, 240, 0.60, 2.10, 0.88, 0.88),
(2, 'Public Policy', 100, 160, 300, 0.55, 2.30, 0.86, 0.90),
(3, 'Financial Risk', -100, 80, 180, 0.70, 1.70, 0.92, 0.84),
(4, 'Infrastructure', 0, 200, 360, 0.52, 2.60, 0.82, 0.86),
(5, 'AI Governance', 100, 120, 240, 0.65, 2.20, 0.88, 0.88);
