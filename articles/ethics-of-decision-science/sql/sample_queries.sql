SELECT
  a.alternative_name,
  (
    0.18 * s.expected_value / 100 +
    0.18 * s.equity_score +
    0.16 * s.safety_score +
    0.14 * s.legitimacy_score +
    0.10 * s.transparency_score +
    0.10 * s.contestability_score +
    0.08 * s.reversibility_score +
    0.06 * s.accountability_score
  ) AS ethical_value_score,
  (
    0.34 * s.harm_risk +
    0.22 * s.opacity_risk +
    0.24 * s.exclusion_risk +
    0.20 * (1 - s.accountability_score)
  ) AS ethical_risk_score
FROM alternative_scores s
JOIN alternatives a ON s.alternative_id = a.alternative_id
ORDER BY ethical_value_score - 0.42 * ethical_risk_score DESC;

SELECT
  a.alternative_name,
  MIN(d.net_benefit) AS minimum_group_net_benefit
FROM distributional_impacts d
JOIN alternatives a ON d.alternative_id = a.alternative_id
GROUP BY a.alternative_name
ORDER BY minimum_group_net_benefit DESC;
