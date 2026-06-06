-- sample_queries.sql

-- Dynamic policy score.
SELECT
    pc.context_name,
    (
      0.24 * cs.balancing_correction -
      0.18 * cs.reinforcing_pressure -
      0.18 * cs.implementation_delay -
      0.18 * cs.resistance_intensity +
      0.22 * cs.monitoring_quality
    ) AS dynamic_policy_score
FROM context_scores cs
JOIN policy_contexts pc ON cs.context_id = pc.context_id
ORDER BY dynamic_policy_score DESC;

-- Scenario robustness summary.
SELECT
    pc.context_name,
    AVG(sp.performance) AS average_scenario_performance,
    MIN(sp.performance) AS worst_case_performance,
    MAX(sp.performance) - MIN(sp.performance) AS performance_range,
    AVG(CASE WHEN sp.performance >= 0.70 THEN 1.0 ELSE 0.0 END) AS threshold_pass_rate
FROM scenario_performance sp
JOIN policy_contexts pc ON sp.context_id = pc.context_id
GROUP BY pc.context_name
ORDER BY worst_case_performance DESC;

-- Review triggers.
SELECT
    pc.context_name,
    cs.reinforcing_pressure,
    cs.implementation_delay,
    cs.resistance_intensity,
    cs.monitoring_quality,
    CASE
      WHEN cs.reinforcing_pressure > 0.75 OR cs.implementation_delay > 0.65 OR cs.resistance_intensity > 0.65 OR cs.monitoring_quality < 0.50
      THEN 'review'
      ELSE 'acceptable'
    END AS review_flag
FROM context_scores cs
JOIN policy_contexts pc ON cs.context_id = pc.context_id
ORDER BY review_flag DESC, pc.context_name;
