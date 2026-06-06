-- sample_queries.sql

-- Democratic decision quality score by process.
SELECT
    p.process_name,
    (
      0.14 * s.evidence_quality +
      0.12 * s.transparency +
      0.14 * s.participation +
      0.14 * s.procedural_fairness +
      0.12 * s.contestability +
      0.12 * s.equity_review +
      0.12 * s.accountability +
      0.10 * s.uncertainty_communication -
      0.05 * s.process_burden -
      0.10 * s.public_trust_risk
    ) AS democratic_decision_quality,
    s.public_trust_risk,
    s.participation,
    s.contestability
FROM process_scores s
JOIN democratic_processes p ON s.process_id = p.process_id
ORDER BY democratic_decision_quality DESC;

-- Standing-access gaps.
SELECT
    group_name,
    standing,
    access,
    MAX(0, standing - access) AS standing_access_gap,
    response_to_input,
    CASE
      WHEN MAX(0, standing - access) > 0.30 OR response_to_input < 0.50 THEN 'review'
      ELSE 'acceptable'
    END AS review_flag
FROM participation_records
ORDER BY standing_access_gap DESC;

-- Democratic review flags.
SELECT
    p.process_name,
    s.participation,
    s.procedural_fairness,
    s.contestability,
    s.equity_review,
    s.accountability,
    s.public_trust_risk,
    CASE
      WHEN s.participation < 0.55
        OR s.procedural_fairness < 0.55
        OR s.contestability < 0.55
        OR s.equity_review < 0.55
        OR s.accountability < 0.55
        OR s.public_trust_risk > 0.60
      THEN 'review'
      ELSE 'acceptable'
    END AS review_flag
FROM process_scores s
JOIN democratic_processes p ON s.process_id = p.process_id
ORDER BY review_flag DESC, s.public_trust_risk DESC;
