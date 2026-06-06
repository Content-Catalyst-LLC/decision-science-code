-- sample_queries.sql

-- Path quality score.
SELECT
    p.path_name,
    (
      0.24 * ps.initial_value +
      0.24 * ps.future_flexibility -
      0.16 * ps.switching_cost -
      0.18 * ps.lock_in_risk +
      0.14 * ps.reversibility -
      0.04 * ps.timing_sensitivity
    ) AS path_quality_score
FROM path_scores ps
JOIN paths p ON ps.path_id = p.path_id
ORDER BY path_quality_score DESC;

-- Scenario robustness summary.
SELECT
    p.path_name,
    AVG(sp.performance) AS average_scenario_performance,
    MIN(sp.performance) AS worst_case_performance,
    MAX(sp.performance) - MIN(sp.performance) AS performance_range,
    AVG(CASE WHEN sp.performance >= 0.70 THEN 1.0 ELSE 0.0 END) AS threshold_pass_rate
FROM scenario_performance sp
JOIN paths p ON sp.path_id = p.path_id
GROUP BY p.path_name
ORDER BY worst_case_performance DESC;

-- Lock-in review triggers.
SELECT
    p.path_name,
    ps.switching_cost,
    ps.lock_in_risk,
    ps.reversibility,
    CASE
      WHEN ps.switching_cost > 0.65 OR ps.lock_in_risk > 0.70 OR ps.reversibility < 0.35
      THEN 'review'
      ELSE 'acceptable'
    END AS review_flag
FROM path_scores ps
JOIN paths p ON ps.path_id = p.path_id
ORDER BY review_flag DESC, p.path_name;
