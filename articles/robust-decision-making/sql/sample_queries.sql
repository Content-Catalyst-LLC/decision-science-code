-- Expected performance by strategy.
SELECT s.strategy_name, SUM(p.performance_value * c.weight) AS expected_value
FROM performance p JOIN strategies s ON p.strategy_id = s.strategy_id JOIN scenarios c ON p.scenario_id = c.scenario_id
GROUP BY s.strategy_name ORDER BY expected_value DESC;

-- Worst-case performance by strategy.
SELECT s.strategy_name, MIN(p.performance_value) AS worst_case
FROM performance p JOIN strategies s ON p.strategy_id = s.strategy_id
GROUP BY s.strategy_name ORDER BY worst_case DESC;

-- Threshold compliance by strategy.
SELECT s.strategy_name,
       AVG(CASE WHEN p.performance_value >= 0.70 THEN 1.0 ELSE 0.0 END) AS threshold_pass_rate,
       SUM(CASE WHEN p.performance_value < 0.70 THEN 1 ELSE 0 END) AS vulnerability_count
FROM performance p JOIN strategies s ON p.strategy_id = s.strategy_id
GROUP BY s.strategy_name ORDER BY threshold_pass_rate DESC, vulnerability_count ASC;
