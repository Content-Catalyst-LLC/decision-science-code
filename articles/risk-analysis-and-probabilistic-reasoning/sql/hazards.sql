-- hazards.sql

INSERT INTO hazards (hazard_id, hazard_name, category, description)
VALUES
('H1', 'cost escalation', 'financial', 'Cost growth beyond baseline assumptions'),
('H2', 'model drift', 'technical', 'Performance degradation after deployment or environmental change'),
('H3', 'demand shock', 'market', 'Demand changes outside expected range'),
('H4', 'service disruption', 'operational', 'Failure of service continuity under stress'),
('H5', 'regulatory change', 'governance', 'Rule changes that alter feasibility or exposure'),
('H6', 'compound stress', 'systemic', 'Multiple risks occurring together');
