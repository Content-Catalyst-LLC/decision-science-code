-- sample_queries.sql

-- Scenario-weighted expected strategic value.
SELECT
    s.strategy_name,
    (
      ss.low_growth * 0.25 +
      ss.base_case * 0.35 +
      ss.high_growth * 0.20 +
      ss.disruption * 0.20
    ) AS expected_value,
    MIN(ss.low_growth, ss.base_case, ss.high_growth, ss.disruption) AS downside_robustness
FROM strategy_scores ss
JOIN strategies s ON ss.strategy_id = s.strategy_id
ORDER BY expected_value DESC;

-- Strategic review flags.
SELECT
    s.strategy_name,
    ss.capability_fit,
    ss.governance_feasibility,
    ss.reversibility,
    MIN(ss.low_growth, ss.base_case, ss.high_growth, ss.disruption) AS downside_robustness,
    CASE
      WHEN MIN(ss.low_growth, ss.base_case, ss.high_growth, ss.disruption) < 50
        OR ss.capability_fit < 0.55
        OR ss.governance_feasibility < 0.55
        OR ss.reversibility < 0.40
      THEN 'review'
      ELSE 'acceptable'
    END AS review_flag
FROM strategy_scores ss
JOIN strategies s ON ss.strategy_id = s.strategy_id
ORDER BY review_flag DESC, downside_robustness ASC;

-- Scenario performance table.
SELECT
    s.strategy_name,
    c.scenario_name,
    c.probability,
    sp.value
FROM scenario_performance sp
JOIN strategies s ON sp.strategy_id = s.strategy_id
JOIN scenarios c ON sp.scenario_id = c.scenario_id
ORDER BY s.strategy_name, c.scenario_name;
