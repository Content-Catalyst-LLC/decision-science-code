-- sample_queries.sql

-- Expected performance by ambiguity profile.
SELECT
    ap.profile_name,
    st.strategy_name,
    SUM(p.performance_value * ap.weight) AS expected_value
FROM performance p
JOIN strategies st ON p.strategy_id = st.strategy_id
JOIN ambiguity_profiles ap ON p.scenario_id = ap.scenario_id
GROUP BY ap.profile_name, st.strategy_name
ORDER BY ap.profile_name, expected_value DESC;

-- Worst-case performance by strategy.
SELECT
    st.strategy_name,
    MIN(p.performance_value) AS worst_case
FROM performance p
JOIN strategies st ON p.strategy_id = st.strategy_id
GROUP BY st.strategy_name
ORDER BY worst_case DESC;

-- Threshold compliance by strategy.
SELECT
    st.strategy_name,
    AVG(CASE WHEN p.performance_value >= 0.70 THEN 1.0 ELSE 0.0 END) AS threshold_pass_rate,
    SUM(CASE WHEN p.performance_value < 0.70 THEN 1 ELSE 0 END) AS vulnerability_count
FROM performance p
JOIN strategies st ON p.strategy_id = st.strategy_id
GROUP BY st.strategy_name
ORDER BY threshold_pass_rate DESC, vulnerability_count ASC;

-- Scenario bests.
SELECT
    sc.scenario_name,
    st.strategy_name,
    p.performance_value
FROM performance p
JOIN scenarios sc ON p.scenario_id = sc.scenario_id
JOIN strategies st ON p.strategy_id = st.strategy_id
WHERE p.performance_value = (
    SELECT MAX(p2.performance_value)
    FROM performance p2
    WHERE p2.scenario_id = p.scenario_id
)
ORDER BY sc.scenario_name;
