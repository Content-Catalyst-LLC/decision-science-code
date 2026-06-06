-- sample_queries.sql

-- Multi-objective public policy score.
SELECT
    p.policy_name,
    (
      0.18 * ps.efficiency +
      0.22 * ps.equity +
      0.18 * ps.resilience +
      0.14 * ps.feasibility +
      0.14 * ps.legitimacy +
      0.14 * ps.implementation_capacity
    ) AS policy_value_score
FROM policy_scores ps
JOIN policies p ON ps.policy_id = p.policy_id
ORDER BY policy_value_score DESC;

-- Scenario robustness summary.
SELECT
    p.policy_name,
    AVG(sp.performance) AS average_performance,
    MIN(sp.performance) AS worst_case_performance,
    MAX(sp.performance) - MIN(sp.performance) AS performance_range,
    AVG(CASE WHEN sp.performance >= 0.70 THEN 1.0 ELSE 0.0 END) AS threshold_pass_rate
FROM scenario_performance sp
JOIN policies p ON sp.policy_id = p.policy_id
GROUP BY p.policy_name
ORDER BY worst_case_performance DESC;

-- Equity, legitimacy, and implementation review.
SELECT
    p.policy_name,
    ps.equity,
    ps.legitimacy,
    ps.implementation_capacity,
    CASE
      WHEN ps.equity < 0.55 OR ps.legitimacy < 0.55 OR ps.implementation_capacity < 0.55
      THEN 'review'
      ELSE 'acceptable'
    END AS review_flag
FROM policy_scores ps
JOIN policies p ON ps.policy_id = p.policy_id
ORDER BY review_flag DESC, p.policy_name;
