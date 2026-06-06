-- decision_cases.sql

INSERT INTO decision_cases (
    case_id,
    domain,
    bias_source,
    hygiene_practice,
    true_value,
    evidence_quality,
    decision_stakes,
    pre_hygiene_judgment,
    post_hygiene_judgment,
    outcome
)
VALUES
(1, 'Public Policy', 'anchoring', 'independent_estimates', 0.62, 'medium', 'high', 0.76, 0.66, 1),
(2, 'Healthcare', 'confirmation', 'structured_dissent', 0.78, 'high', 'high', 0.86, 0.80, 1),
(3, 'Financial Risk', 'overconfidence', 'calibration_review', 0.44, 'medium', 'high', 0.61, 0.50, 0),
(4, 'Infrastructure', 'availability', 'base_rate_check', 0.56, 'medium', 'high', 0.64, 0.58, 1),
(5, 'AI Governance', 'model_overtrust', 'model_validation', 0.69, 'low', 'high', 0.84, 0.75, 0);
