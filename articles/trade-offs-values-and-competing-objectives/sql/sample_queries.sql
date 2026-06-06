-- sample_queries.sql

-- Weighted objective contributions under the base profile.
SELECT
    a.alternative_name,
    o.objective_name,
    s.score,
    w.weight,
    s.score * w.weight AS weighted_contribution
FROM scores s
JOIN alternatives a ON s.alternative_id = a.alternative_id
JOIN objectives o ON s.objective_id = o.objective_id
JOIN weights w ON s.objective_id = w.objective_id
WHERE w.profile_name = 'Base Profile'
ORDER BY a.alternative_name, weighted_contribution DESC;

-- Base composite scores.
SELECT
    a.alternative_name,
    SUM(s.score * w.weight) AS composite_score
FROM scores s
JOIN alternatives a ON s.alternative_id = a.alternative_id
JOIN weights w ON s.objective_id = w.objective_id
WHERE w.profile_name = 'Base Profile'
GROUP BY a.alternative_name
ORDER BY composite_score DESC;

-- Objective weights by scenario.
SELECT
    scenario_name,
    objective_id,
    weight
FROM scenario_weights
ORDER BY scenario_name, objective_id;
