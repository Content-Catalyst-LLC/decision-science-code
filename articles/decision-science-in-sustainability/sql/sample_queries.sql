-- sample_queries.sql

-- Multi-objective sustainability value score.
SELECT
    s.strategy_name,
    (
      0.22 * ss.emissions_reduction +
      0.20 * ss.social_equity -
      0.12 * ss.cost_burden +
      0.18 * ss.resilience_score +
      0.12 * ss.implementation_feasibility +
      0.16 * ss.threshold_protection
    ) AS sustainability_value_score
FROM strategy_scores ss
JOIN strategies s ON ss.strategy_id = s.strategy_id
ORDER BY sustainability_value_score DESC;

-- Scenario robustness summary.
SELECT
    s.strategy_name,
    AVG(sp.performance) AS average_performance,
    MIN(sp.performance) AS worst_case_performance,
    MAX(sp.performance) - MIN(sp.performance) AS performance_range,
    AVG(CASE WHEN sp.performance >= 0.65 THEN 1.0 ELSE 0.0 END) AS threshold_pass_rate
FROM scenario_performance sp
JOIN strategies s ON sp.strategy_id = s.strategy_id
GROUP BY s.strategy_name
ORDER BY worst_case_performance DESC;

-- Threshold, equity, and resilience review.
SELECT
    s.strategy_name,
    ss.social_equity,
    ss.resilience_score,
    ss.threshold_protection,
    ss.cost_burden,
    CASE
      WHEN ss.social_equity < 0.50 OR ss.resilience_score < 0.50 OR ss.threshold_protection < 0.55 OR ss.cost_burden > 0.70
      THEN 'review'
      ELSE 'acceptable'
    END AS review_flag
FROM strategy_scores ss
JOIN strategies s ON ss.strategy_id = s.strategy_id
ORDER BY review_flag DESC, s.strategy_name;
