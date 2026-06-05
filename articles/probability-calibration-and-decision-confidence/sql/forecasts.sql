-- forecasts.sql

INSERT INTO forecasts (forecast_id, domain, event_definition, forecast_probability, reference_class, base_rate, confidence_profile)
VALUES
(1, 'Strategic Forecast', 'strategic outcome occurs before resolution date', 0.72, 'Strategic Forecast', 0.58, 'well calibrated'),
(2, 'Risk Forecast', 'risk event occurs before resolution date', 0.84, 'Risk Forecast', 0.34, 'overconfident'),
(3, 'Operational Forecast', 'operational target is achieved', 0.58, 'Operational Forecast', 0.62, 'underconfident'),
(4, 'Policy Forecast', 'policy adoption target is achieved', 0.41, 'Policy Forecast', 0.46, 'well calibrated'),
(5, 'Model Governance Forecast', 'model governance trigger occurs', 0.76, 'Model Governance Forecast', 0.40, 'well calibrated');
