-- sample_queries.sql

-- Complex-system strategy score.
SELECT
    st.strategy_name,
    (
      0.18 * ss.adaptability +
      0.18 * ss.robustness +
      0.16 * ss.feedback_awareness +
      0.16 * ss.interdependence_handling -
      0.10 * ss.coordination_burden +
      0.12 * ss.legitimacy +
      0.20 * ss.threshold_resilience
    ) AS complex_system_score
FROM strategy_scores ss
JOIN strategies st ON ss.strategy_id = st.strategy_id
ORDER BY complex_system_score DESC;

-- Scenario robustness summary.
SELECT
    st.strategy_name,
    AVG(sp.performance) AS average_scenario_performance,
    MIN(sp.performance) AS worst_case_performance,
    MAX(sp.performance) - MIN(sp.performance) AS performance_range,
    AVG(CASE WHEN sp.performance >= 0.70 THEN 1.0 ELSE 0.0 END) AS threshold_pass_rate
FROM scenario_performance sp
JOIN strategies st ON sp.strategy_id = st.strategy_id
GROUP BY st.strategy_name
ORDER BY worst_case_performance DESC;

-- Review triggers.
SELECT
    st.strategy_name,
    ss.robustness,
    ss.feedback_awareness,
    ss.coordination_burden,
    ss.threshold_resilience,
    CASE
      WHEN ss.robustness < 0.60 OR ss.feedback_awareness < 0.55 OR ss.threshold_resilience < 0.60 OR ss.coordination_burden > 0.70
      THEN 'review'
      ELSE 'acceptable'
    END AS review_flag
FROM strategy_scores ss
JOIN strategies st ON ss.strategy_id = st.strategy_id
ORDER BY review_flag DESC, st.strategy_name;
