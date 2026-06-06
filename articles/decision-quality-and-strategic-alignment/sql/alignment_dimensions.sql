-- alignment_dimensions.sql

INSERT INTO alignment_dimensions (dimension_id, dimension_name, weight, description)
VALUES
('A1', 'strategic_fit', 0.45, 'Fit with stated strategic priorities.'),
('A2', 'capability_fit', 0.30, 'Fit with organizational capabilities.'),
('A3', 'value_fit', 0.25, 'Fit with values and responsibilities.');
