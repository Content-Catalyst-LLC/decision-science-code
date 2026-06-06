-- judgment_cases.sql

INSERT INTO judgment_cases (
    case_id,
    domain,
    prior,
    likelihood_if_true,
    likelihood_if_false,
    posterior,
    anchor,
    anchor_weight,
    evidence_quality
)
VALUES
(1, 'Public Policy', 0.35, 0.72, 0.28, 0.581395, 0.60, 0.40, 'medium'),
(2, 'Healthcare', 0.58, 0.84, 0.22, 0.840909, 0.55, 0.25, 'high'),
(3, 'Financial Risk', 0.28, 0.66, 0.44, 0.368421, 0.70, 0.48, 'medium'),
(4, 'Infrastructure', 0.42, 0.75, 0.35, 0.608696, 0.50, 0.30, 'medium'),
(5, 'AI Governance', 0.33, 0.80, 0.30, 0.567010, 0.68, 0.45, 'low');
