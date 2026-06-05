-- sample_queries.sql
-- Decision science query examples.

-- Alternatives ranked by average scenario outcome.
SELECT
    a.alternative_name,
    AVG(o.outcome_value) AS average_outcome,
    MIN(o.outcome_value) AS minimum_outcome,
    MAX(o.outcome_value) AS maximum_outcome
FROM alternatives a
JOIN scenario_outcomes o
    ON a.alternative_id = o.alternative_id
GROUP BY a.alternative_name
ORDER BY average_outcome DESC;

-- Expected value by alternative.
SELECT
    a.alternative_name,
    SUM(s.probability * o.outcome_value) AS expected_value
FROM alternatives a
JOIN scenario_outcomes o
    ON a.alternative_id = o.alternative_id
JOIN scenarios s
    ON o.scenario_id = s.scenario_id
GROUP BY a.alternative_name
ORDER BY expected_value DESC;
