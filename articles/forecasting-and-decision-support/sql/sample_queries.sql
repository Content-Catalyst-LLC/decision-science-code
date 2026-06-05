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

-- Threshold-supported action.
SELECT
    f.domain,
    f.forecast_probability,
    t.probability_threshold,
    CASE
        WHEN f.forecast_probability >= t.probability_threshold THEN 'Act'
        ELSE 'Wait or monitor'
    END AS threshold_action
FROM forecasts f
JOIN thresholds t ON f.domain = t.domain;

-- Forecast value proxy using expected-loss reduction.
SELECT
    f.domain,
    f.forecast_probability,
    f.base_rate,
    t.probability_threshold,
    f.forecast_cost,
    CASE
        WHEN f.forecast_probability >= t.probability_threshold
        THEN (1 - f.forecast_probability) * t.false_positive_cost
        ELSE f.forecast_probability * t.false_negative_cost
    END AS expected_loss_with_forecast,
    CASE
        WHEN f.base_rate >= t.probability_threshold
        THEN (1 - f.base_rate) * t.false_positive_cost
        ELSE f.base_rate * t.false_negative_cost
    END AS expected_loss_without_forecast
FROM forecasts f
JOIN thresholds t ON f.domain = t.domain;
