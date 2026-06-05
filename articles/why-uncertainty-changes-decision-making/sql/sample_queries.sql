-- sample_queries.sql

-- Expected payoff by alternative.
SELECT
    a.alternative_name,
    SUM(s.probability * o.payoff) AS expected_payoff
FROM alternatives a
JOIN scenario_outcomes o ON a.alternative_id = o.alternative_id
JOIN scenarios s ON o.scenario_id = s.scenario_id
GROUP BY a.alternative_name
ORDER BY expected_payoff DESC;

-- Alternatives ordered by robustness.
SELECT
    a.alternative_name,
    r.threshold,
    r.robustness_share
FROM alternatives a
JOIN robustness_results r ON a.alternative_id = r.alternative_id
ORDER BY r.robustness_share DESC;

-- Maximum regret by alternative.
SELECT
    a.alternative_name,
    MAX(r.regret) AS maximum_regret
FROM alternatives a
JOIN regret_results r ON a.alternative_id = r.alternative_id
GROUP BY a.alternative_name
ORDER BY maximum_regret ASC;
