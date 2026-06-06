-- sample_queries.sql

-- Expected-value comparison of sure and risky gain frames.
SELECT
    case_id,
    domain,
    sure_outcome AS ev_sure_gain,
    risky_high_outcome * risky_high_probability AS ev_risky_gain,
    (risky_high_outcome * risky_high_probability) - sure_outcome AS ev_gain_difference
FROM framing_cases
ORDER BY ABS((risky_high_outcome * risky_high_probability) - sure_outcome) DESC;

-- Reference-point distribution.
SELECT
    reference_point,
    COUNT(*) AS n_cases
FROM framing_cases
GROUP BY reference_point
ORDER BY reference_point;

-- Review frame reversals after frame_scores are populated.
SELECT
    c.case_id,
    c.domain,
    s.gain_frame_choice,
    s.loss_frame_choice,
    s.frame_reversal,
    s.frame_sensitivity_index,
    s.review_flag
FROM framing_cases c
JOIN frame_scores s ON c.case_id = s.case_id
WHERE s.review_flag = 'review';
