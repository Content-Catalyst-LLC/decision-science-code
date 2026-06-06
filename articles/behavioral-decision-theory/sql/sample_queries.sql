-- sample_queries.sql

-- Expected value for each prospect.
SELECT
    p.prospect_id,
    a.domain,
    a.option_name,
    p.outcome_1 * p.probability_1 + p.outcome_2 * p.probability_2 AS expected_value
FROM prospects p
JOIN alternatives a ON p.alternative_id = a.alternative_id
ORDER BY expected_value DESC;

-- Framing-equivalence checks.
SELECT
    frame_id,
    domain,
    frame_type,
    positive_frame,
    negative_frame,
    ABS((1.0 - positive_value) - negative_value) AS equivalence_gap
FROM framing_cases
ORDER BY equivalence_gap DESC;

-- Review flagged behavioral scores after population.
SELECT
    a.domain,
    a.option_name,
    s.expected_utility,
    s.prospect_score,
    s.rank_divergence,
    s.frame_sensitivity_index,
    s.review_flag
FROM behavioral_scores s
JOIN alternatives a ON s.alternative_id = a.alternative_id
WHERE s.review_flag = 'review'
ORDER BY ABS(s.rank_divergence) DESC;
