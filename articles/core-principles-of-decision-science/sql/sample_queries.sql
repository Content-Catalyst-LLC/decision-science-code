-- sample_queries.sql

-- Weighted decision quality by alternative.
SELECT
    a.alternative_name,
    SUM(c.weight * ps.score) AS weighted_decision_quality
FROM alternatives a
JOIN principle_scores ps ON a.alternative_id = ps.alternative_id
JOIN criteria c ON ps.criterion_id = c.criterion_id
GROUP BY a.alternative_name
ORDER BY weighted_decision_quality DESC;

-- Lowest principle score by alternative.
SELECT
    a.alternative_name,
    MIN(ps.score) AS minimum_principle_score
FROM alternatives a
JOIN principle_scores ps ON a.alternative_id = ps.alternative_id
GROUP BY a.alternative_name
ORDER BY minimum_principle_score DESC;
