-- sample_queries.sql

-- Long-horizon strategy score.
SELECT
    st.strategy_name,
    (
      0.24 * ss.resilience_score +
      0.22 * ss.adaptability_score -
      0.12 * ss.near_term_cost +
      0.24 * ss.long_term_value +
      0.18 * ss.reversibility
    ) AS long_horizon_score
FROM strategy_scores ss
JOIN strategies st ON ss.strategy_id = st.strategy_id
ORDER BY long_horizon_score DESC;

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
    ss.resilience_score,
    ss.adaptability_score,
    CASE
      WHEN ss.resilience_score < 0.50 OR ss.adaptability_score < 0.50
      THEN 'review'
      ELSE 'acceptable'
    END AS profile_review_flag
FROM strategy_scores ss
JOIN strategies st ON ss.strategy_id = st.strategy_id
ORDER BY profile_review_flag DESC, st.strategy_name;
