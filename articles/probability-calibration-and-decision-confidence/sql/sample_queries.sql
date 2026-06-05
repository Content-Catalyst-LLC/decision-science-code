-- sample_queries.sql

-- Brier score by forecast.
SELECT
    f.forecast_id,
    f.domain,
    f.forecast_probability,
    o.outcome,
    (f.forecast_probability - o.outcome) * (f.forecast_probability - o.outcome) AS brier_score
FROM forecasts f
JOIN outcomes o ON f.forecast_id = o.forecast_id
ORDER BY brier_score DESC;

-- Average calibration gap by domain.
SELECT
    f.domain,
    AVG(f.forecast_probability) AS average_forecast_probability,
    AVG(o.outcome) AS observed_frequency,
    AVG(f.forecast_probability) - AVG(o.outcome) AS calibration_gap
FROM forecasts f
JOIN outcomes o ON f.forecast_id = o.forecast_id
GROUP BY f.domain
ORDER BY ABS(AVG(f.forecast_probability) - AVG(o.outcome)) DESC;

-- Threshold action review.
SELECT
    f.domain,
    f.forecast_probability,
    t.probability_threshold,
    CASE
        WHEN f.forecast_probability >= t.probability_threshold THEN 'Act'
        ELSE 'Wait or gather evidence'
    END AS threshold_action
FROM forecasts f
JOIN thresholds t ON f.domain = t.decision_context;
