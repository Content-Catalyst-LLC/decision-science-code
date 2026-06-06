-- sample_queries.sql

-- Adaptive pathway score.
SELECT
    p.pathway_name,
    (
      0.20 * ps.initial_performance +
      0.18 * ps.flexibility +
      0.16 * ps.monitoring_quality +
      0.16 * ps.trigger_clarity -
      0.12 * ps.switching_cost +
      0.18 * ps.fallback_strength
    ) AS adaptive_pathway_score
FROM pathway_scores ps
JOIN pathways p ON ps.pathway_id = p.pathway_id
ORDER BY adaptive_pathway_score DESC;

-- Scenario robustness summary.
SELECT
    p.pathway_name,
    AVG(sp.performance) AS average_performance,
    MIN(sp.performance) AS worst_case_performance,
    MAX(sp.performance) - MIN(sp.performance) AS performance_range,
    AVG(CASE WHEN sp.performance >= 0.70 THEN 1.0 ELSE 0.0 END) AS threshold_pass_rate
FROM scenario_performance sp
JOIN pathways p ON sp.pathway_id = p.pathway_id
GROUP BY p.pathway_name
ORDER BY worst_case_performance DESC;

-- Trigger and fallback review.
SELECT
    p.pathway_name,
    ps.monitoring_quality,
    ps.trigger_clarity,
    ps.switching_cost,
    ps.fallback_strength,
    CASE
      WHEN ps.trigger_clarity < 0.45 OR ps.monitoring_quality < 0.45 OR ps.switching_cost > 0.70 OR ps.fallback_strength < 0.45
      THEN 'review'
      ELSE 'acceptable'
    END AS review_flag
FROM pathway_scores ps
JOIN pathways p ON ps.pathway_id = p.pathway_id
ORDER BY review_flag DESC, p.pathway_name;
