-- sample_queries.sql

-- AI decision-support score by design.
SELECT
    d.design_name,
    (
      0.16 * s.model_performance +
      0.14 * s.uncertainty_visibility +
      0.16 * s.human_oversight +
      0.14 * s.contestability +
      0.14 * s.fairness_review +
      0.14 * s.accountability +
      0.10 * s.monitoring_strength -
      0.10 * s.automation_bias_risk -
      0.04 * s.process_burden
    ) AS decision_support_score,
    s.automation_bias_risk,
    s.human_oversight
FROM design_scores s
JOIN support_designs d ON s.design_id = d.design_id
ORDER BY decision_support_score DESC;

-- Oversight strength by role.
SELECT
    role_name,
    authority,
    information_access,
    time_available,
    training,
    override_rights,
    independence,
    oversight_strength
FROM oversight_records
ORDER BY oversight_strength DESC;

-- Review flags.
SELECT
    d.design_name,
    s.human_oversight,
    s.contestability,
    s.fairness_review,
    s.accountability,
    s.automation_bias_risk,
    CASE
      WHEN s.human_oversight < 0.60
        OR s.contestability < 0.60
        OR s.fairness_review < 0.60
        OR s.accountability < 0.60
        OR s.automation_bias_risk > 0.60
      THEN 'review'
      ELSE 'acceptable'
    END AS review_flag
FROM design_scores s
JOIN support_designs d ON s.design_id = d.design_id
ORDER BY review_flag DESC, s.automation_bias_risk DESC;
