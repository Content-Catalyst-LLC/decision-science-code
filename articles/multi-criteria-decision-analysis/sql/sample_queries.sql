-- sample_queries.sql

-- Base ranking.
SELECT
    r.profile_name,
    a.alternative_name,
    r.composite_score,
    r.rank
FROM rankings r
JOIN alternatives a ON r.alternative_id = a.alternative_id
ORDER BY r.profile_name, r.rank;

-- Criterion contributions under one profile.
SELECT
    a.alternative_name,
    c.criterion_name,
    s.normalized_score,
    w.weight,
    s.normalized_score * w.weight AS weighted_contribution
FROM scores s
JOIN alternatives a ON s.alternative_id = a.alternative_id
JOIN criteria c ON s.criterion_id = c.criterion_id
JOIN weights w ON s.criterion_id = w.criterion_id
WHERE w.profile_name = 'Base Profile'
ORDER BY a.alternative_name, weighted_contribution DESC;

-- Evidence-quality review.
SELECT
    a.alternative_name,
    c.criterion_name,
    s.raw_score,
    s.normalized_score,
    s.evidence_quality
FROM scores s
JOIN alternatives a ON s.alternative_id = a.alternative_id
JOIN criteria c ON s.criterion_id = c.criterion_id
WHERE s.evidence_quality = 'low';
