-- sample_queries.sql

-- Expected value by strategy.
SELECT
    s.strategy_name,
    SUM(p.payoff_value * c.weight) AS expected_value
FROM payoffs p
JOIN strategies s ON p.strategy_id = s.strategy_id
JOIN scenarios c ON p.scenario_id = c.scenario_id
GROUP BY s.strategy_name
ORDER BY expected_value DESC;

-- Maximin value by strategy.
SELECT
    s.strategy_name,
    MIN(p.payoff_value) AS maximin_value
FROM payoffs p
JOIN strategies s ON p.strategy_id = s.strategy_id
GROUP BY s.strategy_name
ORDER BY maximin_value DESC;

-- Scenario bests.
WITH scenario_bests AS (
    SELECT scenario_id, MAX(payoff_value) AS best_payoff
    FROM payoffs
    GROUP BY scenario_id
)
SELECT
    c.scenario_name,
    s.strategy_name,
    p.payoff_value,
    sb.best_payoff,
    sb.best_payoff - p.payoff_value AS regret_value
FROM payoffs p
JOIN strategies s ON p.strategy_id = s.strategy_id
JOIN scenarios c ON p.scenario_id = c.scenario_id
JOIN scenario_bests sb ON p.scenario_id = sb.scenario_id
ORDER BY c.scenario_name, regret_value ASC;

-- Minimax regret by strategy.
WITH scenario_bests AS (
    SELECT scenario_id, MAX(payoff_value) AS best_payoff
    FROM payoffs
    GROUP BY scenario_id
),
regrets AS (
    SELECT
        p.strategy_id,
        p.scenario_id,
        sb.best_payoff - p.payoff_value AS regret_value
    FROM payoffs p
    JOIN scenario_bests sb ON p.scenario_id = sb.scenario_id
)
SELECT
    s.strategy_name,
    MAX(r.regret_value) AS maximum_regret
FROM regrets r
JOIN strategies s ON r.strategy_id = s.strategy_id
GROUP BY s.strategy_name
ORDER BY maximum_regret ASC;

-- Threshold compliance.
SELECT
    s.strategy_name,
    AVG(CASE WHEN p.payoff_value >= 0.70 THEN 1.0 ELSE 0.0 END) AS threshold_pass_rate,
    SUM(CASE WHEN p.payoff_value < 0.70 THEN 1 ELSE 0 END) AS vulnerability_count
FROM payoffs p
JOIN strategies s ON p.strategy_id = s.strategy_id
GROUP BY s.strategy_name
ORDER BY threshold_pass_rate DESC, vulnerability_count ASC;
