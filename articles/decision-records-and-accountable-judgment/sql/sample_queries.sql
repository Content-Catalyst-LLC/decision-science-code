-- sample_queries.sql

-- Evidence traceability by record.
SELECT
    record_id,
    AVG(evidence_linked) AS traceability_share,
    AVG(evidence_quality) AS average_evidence_quality
FROM evidence
GROUP BY record_id
ORDER BY traceability_share ASC;

-- Assumption risk by record.
SELECT
    record_id,
    AVG(criticality * (1.0 - confidence)) AS average_assumption_risk,
    SUM(CASE WHEN criticality >= 0.75 AND monitored = 0 THEN 1 ELSE 0 END) AS critical_monitoring_gaps
FROM assumptions
GROUP BY record_id
ORDER BY average_assumption_risk DESC;

-- Active review triggers.
SELECT
    record_id,
    indicator,
    current_value,
    lower_bound,
    upper_bound,
    review_owner
FROM review_triggers
WHERE active = 1;
