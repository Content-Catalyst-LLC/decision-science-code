-- sample_queries.sql

-- Governance score by design.
SELECT
    d.design_name,
    (
      0.16 * s.decision_quality +
      0.14 * s.legitimacy +
      0.16 * s.accountability +
      0.12 * s.implementation_reliability +
      0.10 * s.evidence_traceability +
      0.10 * s.review_strength +
      0.10 * s.monitoring_strength +
      0.10 * s.corrective_capacity -
      0.08 * s.risk_exposure -
      0.04 * s.process_burden
    ) AS governance_score,
    s.risk_exposure,
    s.process_burden
FROM governance_scores s
JOIN governance_designs d ON s.design_id = d.design_id
ORDER BY governance_score DESC;

-- Responsibility gaps.
SELECT
    actor_name,
    role_name,
    decision_influence,
    accountability,
    MAX(0, decision_influence - accountability) AS responsibility_gap,
    CASE
      WHEN MAX(0, decision_influence - accountability) >= 0.28 THEN 'review'
      ELSE 'acceptable'
    END AS review_flag
FROM accountability_records
ORDER BY responsibility_gap DESC;

-- Governance review flags.
SELECT
    d.design_name,
    s.accountability,
    s.evidence_traceability,
    s.review_strength,
    s.corrective_capacity,
    s.risk_exposure,
    CASE
      WHEN s.accountability < 0.60
        OR s.evidence_traceability < 0.60
        OR s.review_strength < 0.60
        OR s.corrective_capacity < 0.60
        OR s.risk_exposure > 0.60
      THEN 'review'
      ELSE 'acceptable'
    END AS review_flag
FROM governance_scores s
JOIN governance_designs d ON s.design_id = d.design_id
ORDER BY review_flag DESC, s.risk_exposure DESC;
