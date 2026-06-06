-- sample_queries.sql

-- Forecast scoring and confidence gaps.
SELECT
    forecast_id,
    domain,
    forecast_probability,
    confidence,
    outcome,
    (forecast_probability - outcome) * (forecast_probability - outcome) AS brier_score,
    confidence - (1 - ((forecast_probability - outcome) * (forecast_probability - outcome))) AS confidence_error
FROM forecasts
ORDER BY confidence_error DESC;

-- Planning error diagnostics.
SELECT
    case_id,
    domain,
    estimated_duration,
    actual_duration,
    (actual_duration - estimated_duration) / estimated_duration AS duration_planning_error,
    estimated_cost,
    actual_cost,
    (actual_cost - estimated_cost) / estimated_cost AS cost_planning_error
FROM planning_estimates
ORDER BY duration_planning_error DESC;

-- Calibration gaps.
SELECT
    probability_bin,
    average_forecast_probability,
    observed_frequency,
    average_forecast_probability - observed_frequency AS calibration_gap,
    n_cases
FROM calibration_bins
ORDER BY ABS(average_forecast_probability - observed_frequency) DESC;
