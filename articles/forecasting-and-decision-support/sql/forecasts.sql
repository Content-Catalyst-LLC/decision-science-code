-- forecasts.sql

INSERT INTO forecasts (forecast_id, domain, forecast_target, base_rate, forecast_probability, forecast_horizon_days, forecast_cost, method_notes)
VALUES
(1, 'Public Policy', 'program adoption threshold', 0.46, 0.62, 90, 5.20, 'reference class plus implementation signals'),
(2, 'Healthcare', 'patient risk threshold', 0.52, 0.74, 30, 4.10, 'clinical-style synthetic risk forecast'),
(3, 'Financial Risk', 'risk event threshold', 0.28, 0.41, 7, 3.80, 'short-term risk signal forecast'),
(4, 'Infrastructure', 'asset investment threshold', 0.34, 0.57, 365, 9.40, 'long-horizon asset-risk forecast'),
(5, 'AI Governance', 'model governance review threshold', 0.40, 0.68, 30, 6.60, 'model drift and harm-risk forecast');
