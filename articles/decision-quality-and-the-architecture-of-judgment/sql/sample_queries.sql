-- sample_queries.sql

-- Weighted decision-quality score by alternative.
SELECT
    a.alternative_name,
    SUM(qc.weight * qs.score) AS decision_quality_score
FROM alternatives a
JOIN quality_scores qs ON a.alternative_id = qs.alternative_id
JOIN quality_components qc ON qs.component_id = qc.component_id
GROUP BY a.alternative_name
ORDER BY decision_quality_score DESC;

-- Outcome rate by alternative.
SELECT
    a.alternative_name,
    AVG(o.favorable_outcome) AS favorable_outcome_rate,
    AVG(o.realized_outcome) AS mean_outcome
FROM alternatives a
JOIN outcomes o ON a.alternative_id = o.alternative_id
GROUP BY a.alternative_name
ORDER BY favorable_outcome_rate DESC;
