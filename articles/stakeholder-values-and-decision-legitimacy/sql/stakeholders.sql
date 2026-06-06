-- stakeholders.sql

INSERT INTO stakeholders (stakeholder_id, stakeholder_name, importance, minimum_threshold, description)
VALUES
('G1', 'Residents', 0.24, 0.66, 'People living in affected communities.'),
('G2', 'Service Users', 0.24, 0.68, 'People who rely on the service or system being changed.'),
('G3', 'Workers', 0.18, 0.64, 'People implementing or working inside the decision system.'),
('G4', 'Regulators', 0.18, 0.66, 'Institutions responsible for compliance oversight and public accountability.'),
('G5', 'Future Stakeholders', 0.16, 0.62, 'Future users, residents, ecosystems, or generations affected over time.');
