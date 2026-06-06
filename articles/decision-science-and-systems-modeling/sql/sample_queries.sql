-- sample_queries.sql

-- Dynamic intervention score.
SELECT
    st.strategy_name,
    (
      0.22 * ss.stability_score +
      0.18 * ss.responsiveness_score -
      0.20 * ss.delay_sensitivity +
      0.26 * ss.resilience_score +
      0.14 * ss.transparency_score
    ) AS dynamic_intervention_score
FROM strategy_scores ss
JOIN strategies st ON ss.strategy_id = st.strategy_id
ORDER BY dynamic_intervention_score DESC;

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
    ss.delay_sensitivity,
    ss.resilience_score,
    ss.transparency_score,
    CASE
      WHEN ss.delay_sensitivity > 0.70 OR ss.resilience_score < 0.60 OR ss.transparency_score < 0.55
      THEN 'review'
      ELSE 'acceptable'
    END AS review_flag
FROM strategy_scores ss
JOIN strategies st ON ss.strategy_id = st.strategy_id
ORDER BY review_flag DESC, st.strategy_name;
