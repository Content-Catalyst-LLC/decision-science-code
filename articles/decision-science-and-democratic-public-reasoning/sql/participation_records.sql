-- participation_records.sql

INSERT INTO participation_records (group_id, group_name, standing, access, participation_quality, deliberation_quality, response_to_input, trust_effect, notes)
VALUES
('G1', 'Affected residents', 0.90, 0.62, 0.70, 0.68, 0.64, 0.66, 'Directly affected public with high standing and moderate access.'),
('G2', 'Low-power communities', 0.88, 0.46, 0.54, 0.52, 0.42, 0.48, 'High standing but lower access and weaker institutional response.'),
('G3', 'Technical experts', 0.72, 0.84, 0.78, 0.76, 0.74, 0.62, 'Strong evidence role but should not dominate values.'),
('G4', 'Frontline implementers', 0.76, 0.68, 0.72, 0.70, 0.66, 0.64, 'Practical implementation knowledge.'),
('G5', 'Organized interest groups', 0.58, 0.82, 0.76, 0.62, 0.70, 0.54, 'High access but may not represent wider affected publics.'),
('G6', 'Future generations', 0.84, 0.22, 0.30, 0.34, 0.28, 0.40, 'High ethical standing but weak direct voice.'),
('G7', 'Public oversight body', 0.70, 0.78, 0.74, 0.72, 0.80, 0.72, 'Can strengthen accountability and public trust.');
