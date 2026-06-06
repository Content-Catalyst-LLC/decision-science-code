-- sample_queries.sql

-- Confidence-gap diagnostics.
SELECT
    case_id,
    domain,
    bias_profile,
    judged_probability,
    confidence,
    confidence - judged_probability AS confidence_gap
FROM judgment_cases
ORDER BY ABS(confidence - judged_probability) DESC;

-- Brier score by case.
SELECT
    case_id,
    domain,
    bias_profile,
    judged_probability,
    outcome,
    (judged_probability - outcome) * (judged_probability - outcome) AS brier_score
FROM judgment_cases
ORDER BY brier_score DESC;

-- Cases needing debiasing review.
SELECT
    case_id,
    domain,
    bias_profile,
    judged_probability,
    confidence,
    outcome,
    CASE
        WHEN ABS(confidence - judged_probability) > 0.12 THEN 'review confidence'
        WHEN (judged_probability - outcome) * (judged_probability - outcome) > 0.25 THEN 'review calibration'
        ELSE 'acceptable'
    END AS review_flag
FROM judgment_cases;
