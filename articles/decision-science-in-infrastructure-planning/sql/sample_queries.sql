-- sample_queries.sql

-- Scenario-weighted infrastructure value.
SELECT
    a.alternative_name,
    (
      s.baseline * 0.30 +
      s.climate_stress * 0.20 +
      s.demand_growth * 0.20 +
      s.funding_constraint * 0.15 +
      s.disruption * 0.15
    ) AS expected_service_value,
    MIN(s.baseline, s.climate_stress, s.demand_growth, s.funding_constraint, s.disruption) AS worst_case_value
FROM alternative_scores s
JOIN alternatives a ON s.alternative_id = a.alternative_id
ORDER BY expected_service_value DESC;

-- Review flags.
SELECT
    a.alternative_name,
    s.equity_score,
    s.resilience_score,
    s.environmental_score,
    s.implementation_feasibility,
    MIN(s.baseline, s.climate_stress, s.demand_growth, s.funding_constraint, s.disruption) AS worst_case_value,
    CASE
      WHEN MIN(s.baseline, s.climate_stress, s.demand_growth, s.funding_constraint, s.disruption) < 50
        OR s.equity_score < 0.55
        OR s.resilience_score < 0.55
        OR s.environmental_score < 0.50
        OR s.implementation_feasibility < 0.50
      THEN 'review'
      ELSE 'acceptable'
    END AS review_flag
FROM alternative_scores s
JOIN alternatives a ON s.alternative_id = a.alternative_id
ORDER BY review_flag DESC, worst_case_value ASC;

-- Scenario performance.
SELECT
    a.alternative_name,
    sc.scenario_name,
    sc.probability,
    sp.value
FROM scenario_performance sp
JOIN alternatives a ON sp.alternative_id = a.alternative_id
JOIN scenarios sc ON sp.scenario_id = sc.scenario_id
ORDER BY a.alternative_name, sc.scenario_name;
