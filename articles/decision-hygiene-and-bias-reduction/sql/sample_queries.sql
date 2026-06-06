-- sample_queries.sql

-- Bias and error before and after hygiene.
SELECT
    case_id,
    domain,
    bias_source,
    hygiene_practice,
    pre_hygiene_judgment - true_value AS pre_error,
    post_hygiene_judgment - true_value AS post_error,
    ABS(pre_hygiene_judgment - true_value) - ABS(post_hygiene_judgment - true_value) AS error_reduction
FROM decision_cases
ORDER BY error_reduction DESC;

-- Brier scores before and after hygiene.
SELECT
    case_id,
    domain,
    (pre_hygiene_judgment - outcome) * (pre_hygiene_judgment - outcome) AS pre_brier_score,
    (post_hygiene_judgment - outcome) * (post_hygiene_judgment - outcome) AS post_brier_score
FROM decision_cases
ORDER BY post_brier_score DESC;

-- Low-evidence, high-stakes cases requiring review.
SELECT
    case_id,
    domain,
    bias_source,
    hygiene_practice,
    evidence_quality,
    decision_stakes
FROM decision_cases
WHERE evidence_quality = 'low' AND decision_stakes = 'high';
