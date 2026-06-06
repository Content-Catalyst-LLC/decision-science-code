-- sample_queries.sql

-- Influence concentration by group.
SELECT
    group_id,
    MAX(influence_weight) AS influence_concentration
FROM influence_weights
GROUP BY group_id
ORDER BY influence_concentration DESC;

-- Hidden-profile risk by group.
SELECT
    group_id,
    domain,
    shared_information,
    unique_information,
    CAST(unique_information AS REAL) / (shared_information + unique_information) AS hidden_profile_risk
FROM groups_table
ORDER BY hidden_profile_risk DESC;

-- Estimate movement after social influence.
SELECT
    group_id,
    member_id,
    role_name,
    independent_estimate,
    influenced_estimate,
    influenced_estimate - independent_estimate AS influence_shift
FROM members
ORDER BY ABS(influence_shift) DESC;

-- Unique evidence requiring structured elicitation.
SELECT
    group_id,
    evidence_id,
    evidence_type,
    quality,
    description
FROM evidence_items
WHERE shared_status = 'unique'
ORDER BY group_id, quality DESC;
