-- parameters.sql

INSERT INTO parameters (parameter_name, baseline, low_value, high_value, evidence_quality, source_type, description)
VALUES
('demand_shift', 0.50, -2.00, 3.00, 'medium', 'scenario estimate', 'Demand growth or contraction relative to baseline'),
('cost_pressure', 0.30, 0.00, 1.50, 'medium', 'expert estimate', 'Cost escalation pressure'),
('disruption_pressure', 0.20, 0.00, 1.80, 'low', 'stress scenario', 'External disruption or systemic stress'),
('volatility', 3.00, 0.50, 10.00, 'medium', 'model estimate', 'Unmodeled variation around expected performance'),
('resilience_weight', 0.22, 0.05, 0.60, 'medium', 'value judgment', 'Decision weight placed on resilience');
