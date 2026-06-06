-- sample_queries.sql

-- Scenario-weighted AI governance value.
SELECT
    o.option_name,
    (
      s.baseline_value * 0.35 +
      s.safety_stress * 0.20 +
      s.equity_stress * 0.15 +
      s.security_stress * 0.15 +
      s.drift_stress * 0.15
    ) AS expected_governance_value,
    MIN(s.baseline_value, s.safety_stress, s.equity_stress, s.security_stress, s.drift_stress) AS worst_case_value
FROM option_scores s
JOIN ai_options o ON s.option_id = o.option_id
ORDER BY expected_governance_value DESC;

-- Governance review flags.
SELECT
    o.option_name,
    s.evidence_quality,
    s.oversight_strength,
    s.equity_score,
    s.security_readiness,
    MIN(s.baseline_value, s.safety_stress, s.equity_stress, s.security_stress, s.drift_stress) AS worst_case_value,
    CASE
      WHEN MIN(s.baseline_value, s.safety_stress, s.equity_stress, s.security_stress, s.drift_stress) < 50
        OR s.evidence_quality < 0.60
        OR s.oversight_strength < 0.60
        OR s.equity_score < 0.55
        OR s.security_readiness < 0.55
      THEN 'review'
      ELSE 'acceptable'
    END AS review_flag
FROM option_scores s
JOIN ai_options o ON s.option_id = o.option_id
ORDER BY review_flag DESC, worst_case_value ASC;

-- Scenario performance.
SELECT
    o.option_name,
    sc.scenario_name,
    sc.probability,
    sp.value
FROM scenario_performance sp
JOIN ai_options o ON sp.option_id = o.option_id
JOIN scenarios sc ON sp.scenario_id = sc.scenario_id
ORDER BY o.option_name, sc.scenario_name;
