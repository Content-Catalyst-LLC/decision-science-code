-- sample_queries.sql

-- Bayesian-style posterior using odds and likelihood ratio.
SELECT
    case_id,
    domain,
    prior,
    likelihood_if_true,
    likelihood_if_false,
    (prior / (1 - prior)) * (likelihood_if_true / likelihood_if_false) AS posterior_odds,
    ((prior / (1 - prior)) * (likelihood_if_true / likelihood_if_false)) /
      (1 + ((prior / (1 - prior)) * (likelihood_if_true / likelihood_if_false))) AS computed_posterior
FROM judgment_cases;

-- Forecast scoring after forecast_scores are populated.
SELECT
    forecast_id,
    forecast_probability,
    confidence,
    outcome,
    (forecast_probability - outcome) * (forecast_probability - outcome) AS computed_brier_score,
    confidence - forecast_probability AS computed_confidence_gap
FROM forecast_scores
ORDER BY computed_brier_score DESC;

-- Calibration gaps.
SELECT
    probability_bin,
    average_forecast_probability,
    observed_frequency,
    average_forecast_probability - observed_frequency AS calibration_gap,
    n_cases
FROM calibration_bins
ORDER BY ABS(average_forecast_probability - observed_frequency) DESC;
