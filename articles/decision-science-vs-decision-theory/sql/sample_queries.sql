-- sample_queries.sql

-- Expected payoff by alternative under a probability set.
SELECT
    a.alternative_name,
    SUM(p.probability * u.payoff) AS expected_payoff
FROM alternatives a
JOIN utilities u ON a.alternative_id = u.alternative_id
JOIN probabilities p ON u.scenario_id = p.scenario_id
WHERE p.probability_set = 'base'
GROUP BY a.alternative_name
ORDER BY expected_payoff DESC;

-- Maximum regret by alternative.
SELECT
    a.alternative_name,
    MAX(r.regret) AS maximum_regret
FROM alternatives a
JOIN regret_profiles r ON a.alternative_id = r.alternative_id
GROUP BY a.alternative_name
ORDER BY maximum_regret ASC;
