-- sample_queries.sql

-- Expected loss across regimes.
SELECT
    p.portfolio_name,
    (
      ps.normal * 0.55 +
      ps.recession * 0.20 +
      ps.liquidity_shock * 0.15 +
      ps.systemic_stress * 0.10
    ) AS expected_loss,
    MIN(ps.normal, ps.recession, ps.liquidity_shock, ps.systemic_stress) AS worst_case
FROM portfolio_scores ps
JOIN portfolios p ON ps.portfolio_id = p.portfolio_id
ORDER BY worst_case ASC;

-- Financial risk review flags.
SELECT
    p.portfolio_name,
    ps.liquidity_score,
    ps.governance_score,
    ps.model_confidence,
    MIN(ps.normal, ps.recession, ps.liquidity_shock, ps.systemic_stress) AS worst_case,
    CASE
      WHEN MIN(ps.normal, ps.recession, ps.liquidity_shock, ps.systemic_stress) < -20
        OR ps.liquidity_score < 0.45
        OR ps.governance_score < 0.55
        OR ps.model_confidence < 0.55
      THEN 'review'
      ELSE 'acceptable'
    END AS review_flag
FROM portfolio_scores ps
JOIN portfolios p ON ps.portfolio_id = p.portfolio_id
ORDER BY review_flag DESC, worst_case ASC;

-- Scenario performance by portfolio.
SELECT
    p.portfolio_name,
    s.scenario_name,
    s.probability,
    sp.loss_pct
FROM scenario_performance sp
JOIN portfolios p ON sp.portfolio_id = p.portfolio_id
JOIN scenarios s ON sp.scenario_id = s.scenario_id
ORDER BY p.portfolio_name, sp.loss_pct ASC;
