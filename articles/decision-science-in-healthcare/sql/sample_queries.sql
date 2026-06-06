-- sample_queries.sql

-- Treatment value score.
SELECT
    t.treatment_name,
    (
      0.30 * ts.expected_benefit -
      0.18 * ts.adverse_event_risk -
      0.14 * ts.cost_burden +
      0.18 * ts.patient_preference_fit +
      0.10 * ts.equity_score +
      0.10 * ts.implementation_feasibility
    ) AS treatment_value_score
FROM treatment_scores ts
JOIN treatments t ON ts.treatment_id = t.treatment_id
ORDER BY treatment_value_score DESC;

-- Scenario robustness summary.
SELECT
    t.treatment_name,
    AVG(sp.performance) AS average_performance,
    MIN(sp.performance) AS worst_case_performance,
    MAX(sp.performance) - MIN(sp.performance) AS performance_range,
    AVG(CASE WHEN sp.performance >= 0.65 THEN 1.0 ELSE 0.0 END) AS threshold_pass_rate
FROM scenario_performance sp
JOIN treatments t ON sp.treatment_id = t.treatment_id
GROUP BY t.treatment_name
ORDER BY worst_case_performance DESC;

-- Clinical review flags.
SELECT
    t.treatment_name,
    ts.adverse_event_risk,
    ts.patient_preference_fit,
    ts.equity_score,
    ts.implementation_feasibility,
    CASE
      WHEN ts.adverse_event_risk > 0.25 OR ts.patient_preference_fit < 0.60 OR ts.equity_score < 0.55 OR ts.implementation_feasibility < 0.55
      THEN 'review'
      ELSE 'acceptable'
    END AS review_flag
FROM treatment_scores ts
JOIN treatments t ON ts.treatment_id = t.treatment_id
ORDER BY review_flag DESC, t.treatment_name;
