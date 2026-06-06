-- sample_queries.sql

-- Future decision score by pathway.
SELECT
    p.pathway_name,
    (
      0.12 * s.ai_readiness +
      0.14 * s.governance_maturity +
      0.14 * s.uncertainty_capability +
      0.12 * s.participatory_legitimacy +
      0.12 * s.reproducibility +
      0.12 * s.systems_modeling +
      0.14 * s.ethical_accountability +
      0.14 * s.adaptive_capacity -
      0.04 * s.process_burden -
      0.12 * s.failure_risk
    ) AS future_decision_score,
    s.failure_risk,
    s.governance_maturity,
    s.adaptive_capacity
FROM pathway_scores s
JOIN future_pathways p ON s.pathway_id = p.pathway_id
ORDER BY future_decision_score DESC;

-- Maturity gaps.
SELECT
    dimension_name,
    current_maturity,
    target_maturity,
    gap,
    priority,
    CASE
      WHEN gap >= 0.30 THEN 'review'
      ELSE 'acceptable'
    END AS review_flag
FROM maturity_records
ORDER BY gap DESC;

-- Review flags.
SELECT
    p.pathway_name,
    s.governance_maturity,
    s.uncertainty_capability,
    s.ethical_accountability,
    s.adaptive_capacity,
    s.failure_risk,
    CASE
      WHEN s.governance_maturity < 0.60
        OR s.uncertainty_capability < 0.60
        OR s.ethical_accountability < 0.60
        OR s.adaptive_capacity < 0.60
        OR s.failure_risk > 0.55
      THEN 'review'
      ELSE 'acceptable'
    END AS review_flag
FROM pathway_scores s
JOIN future_pathways p ON s.pathway_id = p.pathway_id
ORDER BY review_flag DESC, s.failure_risk DESC;
