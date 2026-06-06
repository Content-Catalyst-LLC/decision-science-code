-- reference_points.sql

INSERT INTO reference_points (reference_point_type, value, description)
VALUES
('status_quo', 0, 'current condition as baseline'),
('target', 100, 'planned or expected target as baseline'),
('worst_case', -100, 'adverse scenario as comparison baseline'),
('prior_performance', 50, 'previous period performance as baseline'),
('peer_benchmark', 75, 'comparable organization or group benchmark');
