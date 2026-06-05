-- sample_queries.sql

-- Expected value by strategy.
SELECT
    p.strategy,
    SUM(p.probability * o.terminal_value) AS gross_expected_value
FROM probabilities p
JOIN outcomes o
  ON p.decision_id = o.decision_id
 AND p.strategy = o.strategy
 AND p.outcome_state = o.outcome_state
WHERE p.decision_id = 1
GROUP BY p.strategy
ORDER BY gross_expected_value DESC;

-- Probability quality by strategy.
SELECT
    strategy,
    AVG(
        CASE quality
            WHEN 'high' THEN 1.0
            WHEN 'medium' THEN 0.65
            WHEN 'low' THEN 0.35
            ELSE 0.0
        END
    ) AS average_probability_quality
FROM probabilities
GROUP BY strategy
ORDER BY average_probability_quality ASC;
