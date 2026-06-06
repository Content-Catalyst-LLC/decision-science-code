SELECT
    o.option_name,
    (s.baseline * 0.30 + s.rapid_escalation * 0.20 + s.resource_constraint * 0.15 + s.public_trust_stress * 0.15 + s.cascading_failure * 0.20) AS expected_response_value,
    MIN(s.baseline, s.rapid_escalation, s.resource_constraint, s.public_trust_stress, s.cascading_failure) AS worst_case_value
FROM option_scores s
JOIN response_options o ON s.option_id = o.option_id
ORDER BY expected_response_value DESC;
