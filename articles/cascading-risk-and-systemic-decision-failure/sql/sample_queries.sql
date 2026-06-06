-- sample_queries.sql

-- Cascade risk score by system.
SELECT
    s.system_name,
    (
      0.22 * ss.exposure +
      0.22 * ss.dependency_centrality +
      0.20 * ss.buffer_weakness +
      0.18 * ss.common_mode_risk -
      0.09 * ss.monitoring_quality -
      0.09 * ss.response_capacity
    ) AS cascade_risk_score
FROM system_scores ss
JOIN systems s ON ss.system_id = s.system_id
ORDER BY cascade_risk_score DESC;

-- Scenario resilience summary.
SELECT
    s.system_name,
    AVG(sp.service_continuity) AS average_continuity,
    MIN(sp.service_continuity) AS worst_case_continuity,
    MAX(sp.service_continuity) - MIN(sp.service_continuity) AS continuity_range,
    AVG(CASE WHEN sp.service_continuity >= 0.70 THEN 1.0 ELSE 0.0 END) AS threshold_pass_rate
FROM scenario_performance sp
JOIN systems s ON sp.system_id = s.system_id
GROUP BY s.system_name
ORDER BY worst_case_continuity DESC;

-- Common-mode and buffer review.
SELECT
    s.system_name,
    ss.buffer_weakness,
    ss.common_mode_risk,
    ss.response_capacity,
    CASE
      WHEN ss.buffer_weakness > 0.70 OR ss.common_mode_risk > 0.70 OR ss.response_capacity < 0.45
      THEN 'review'
      ELSE 'acceptable'
    END AS review_flag
FROM system_scores ss
JOIN systems s ON ss.system_id = s.system_id
ORDER BY review_flag DESC, s.system_name;
