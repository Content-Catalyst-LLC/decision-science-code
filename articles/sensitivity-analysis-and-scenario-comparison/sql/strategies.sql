-- strategies.sql

INSERT INTO strategies (
    strategy_name,
    base_value,
    demand_sensitivity,
    cost_sensitivity,
    disruption_sensitivity,
    resilience_buffer,
    adaptation_capacity,
    description
)
VALUES
('Efficiency Strategy', 78, 10, 16, 18, 4, 3, 'High baseline efficiency but fragile under stress'),
('Balanced Strategy', 75, 8, 10, 11, 9, 7, 'Moderate performance across most conditions'),
('Resilience Strategy', 70, 5.5, 8, 7, 16, 5, 'Strong downside protection and stress performance'),
('Adaptive Strategy', 73, 7, 9, 9, 12, 12, 'Strong under volatile and shifting conditions'),
('Precautionary Strategy', 68, 4, 6, 5, 18, 6, 'Conservative strategy with strong worst-case protection');
