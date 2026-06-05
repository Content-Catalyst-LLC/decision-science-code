-- sample_queries.sql

-- Deterministic strategy score under a scenario-like parameter set.
SELECT
    strategy_name,
    base_value
      + demand_sensitivity * 0.50
      - cost_sensitivity * 0.30
      - disruption_sensitivity * 0.20
      + resilience_buffer * 0.20
      + adaptation_capacity * ABS(0.50)
      AS baseline_score
FROM strategies
ORDER BY baseline_score DESC;

-- Parameter evidence quality.
SELECT
    parameter_name,
    evidence_quality,
    CASE evidence_quality
        WHEN 'high' THEN 1.0
        WHEN 'medium' THEN 0.65
        WHEN 'low' THEN 0.35
        ELSE 0.0
    END AS evidence_quality_score
FROM parameters
ORDER BY evidence_quality_score ASC;

-- Worst-case scenario score by strategy after scenario_scores are populated.
SELECT
    strategy_name,
    MIN(composite_score) AS worst_scenario_score,
    AVG(regret) AS average_regret,
    MAX(regret) AS maximum_regret
FROM scenario_scores
GROUP BY strategy_name
ORDER BY worst_scenario_score DESC;
