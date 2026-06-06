-- sample_queries.sql

-- Maximum stakeholder burden by alternative.
SELECT
    a.alternative_name,
    MAX(b.burden) AS maximum_stakeholder_burden,
    AVG(b.burden) AS average_stakeholder_burden
FROM burdens b
JOIN alternatives a ON b.alternative_id = a.alternative_id
GROUP BY a.alternative_name
ORDER BY maximum_stakeholder_burden ASC;

-- Procedural legitimacy score with fixed weights.
SELECT
    a.alternative_name,
    (0.24 * p.voice + 0.20 * p.transparency + 0.20 * p.explanation + 0.18 * p.contestability + 0.18 * p.review) AS procedural_score
FROM procedure_scores p
JOIN alternatives a ON p.alternative_id = a.alternative_id
ORDER BY procedural_score DESC;

-- Stakeholder score by group and alternative.
SELECT
    a.alternative_name,
    s.stakeholder_name,
    (
      vw1.weight * a.cost_efficiency +
      vw2.weight * a.service_quality +
      vw3.weight * a.equity +
      vw4.weight * a.autonomy +
      vw5.weight * a.resilience +
      vw6.weight * a.transparency
    ) AS stakeholder_score
FROM alternatives a
JOIN stakeholders s
JOIN value_weights vw1 ON vw1.stakeholder_id = s.stakeholder_id AND vw1.criterion_id = 'C1'
JOIN value_weights vw2 ON vw2.stakeholder_id = s.stakeholder_id AND vw2.criterion_id = 'C2'
JOIN value_weights vw3 ON vw3.stakeholder_id = s.stakeholder_id AND vw3.criterion_id = 'C3'
JOIN value_weights vw4 ON vw4.stakeholder_id = s.stakeholder_id AND vw4.criterion_id = 'C4'
JOIN value_weights vw5 ON vw5.stakeholder_id = s.stakeholder_id AND vw5.criterion_id = 'C5'
JOIN value_weights vw6 ON vw6.stakeholder_id = s.stakeholder_id AND vw6.criterion_id = 'C6'
ORDER BY a.alternative_name, stakeholder_score DESC;
