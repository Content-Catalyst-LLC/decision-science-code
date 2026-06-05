-- sample_queries.sql

-- Expected value by prospect.
SELECT
    p.prospect_name,
    SUM(o.outcome_value * pr.probability) AS expected_value
FROM prospects p
JOIN outcomes o ON p.prospect_id = o.prospect_id
JOIN probabilities pr ON o.outcome_id = pr.outcome_id
WHERE pr.probability_set = 'baseline'
GROUP BY p.prospect_name
ORDER BY expected_value DESC;

-- Probability quality by prospect.
SELECT
    p.prospect_name,
    AVG(
        CASE pr.quality
            WHEN 'high' THEN 1.0
            WHEN 'medium' THEN 0.65
            WHEN 'low' THEN 0.35
            ELSE 0.0
        END
    ) AS average_probability_quality
FROM prospects p
JOIN outcomes o ON p.prospect_id = o.prospect_id
JOIN probabilities pr ON o.outcome_id = pr.outcome_id
GROUP BY p.prospect_name
ORDER BY average_probability_quality ASC;
