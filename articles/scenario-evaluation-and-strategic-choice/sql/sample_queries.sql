-- sample_queries.sql

-- Expected value by strategy.
SELECT
    st.strategy_name,
    SUM(sp.performance * sc.probability) AS expected_value
FROM scenario_performance sp
JOIN strategies st ON sp.strategy_id = st.strategy_id
JOIN scenarios sc ON sp.scenario_id = sc.scenario_id
GROUP BY st.strategy_name
ORDER BY expected_value DESC;

-- Worst-case performance and threshold pass rate.
SELECT
    st.strategy_name,
    MIN(sp.performance) AS worst_case,
    AVG(CASE WHEN sp.performance >= 0.70 THEN 1.0 ELSE 0.0 END) AS threshold_pass_rate
FROM scenario_performance sp
JOIN strategies st ON sp.strategy_id = st.strategy_id
GROUP BY st.strategy_name
ORDER BY worst_case DESC;

-- Regret table.
WITH scenario_best AS (
    SELECT scenario_id, MAX(performance) AS best_performance
    FROM scenario_performance
    GROUP BY scenario_id
)
SELECT
    st.strategy_name,
    sc.scenario_name,
    sp.performance,
    sb.best_performance,
    sb.best_performance - sp.performance AS regret
FROM scenario_performance sp
JOIN scenario_best sb ON sp.scenario_id = sb.scenario_id
JOIN strategies st ON sp.strategy_id = st.strategy_id
JOIN scenarios sc ON sp.scenario_id = sc.scenario_id
ORDER BY sc.scenario_name, regret DESC;
