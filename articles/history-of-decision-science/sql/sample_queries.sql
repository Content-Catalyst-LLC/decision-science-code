-- sample_queries.sql

-- Expected payoff by paradigm under objective probabilities.
SELECT
    p.paradigm_name,
    SUM(s.objective_probability * y.payoff) AS expected_payoff
FROM paradigms p
JOIN payoffs y ON p.paradigm_id = y.paradigm_id
JOIN scenarios s ON y.scenario_id = s.scenario_id
GROUP BY p.paradigm_name
ORDER BY expected_payoff DESC;

-- Maximum regret by paradigm.
SELECT
    p.paradigm_name,
    MAX(r.regret) AS maximum_regret
FROM paradigms p
JOIN regret_results r ON p.paradigm_id = r.paradigm_id
GROUP BY p.paradigm_name
ORDER BY maximum_regret ASC;
