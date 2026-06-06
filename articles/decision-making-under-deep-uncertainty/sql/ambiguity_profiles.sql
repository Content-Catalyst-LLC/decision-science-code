-- ambiguity_profiles.sql

INSERT INTO ambiguity_profiles (profile_name, scenario_id, weight)
VALUES
('equal','C1',0.1666666667),('equal','C2',0.1666666667),('equal','C3',0.1666666667),('equal','C4',0.1666666667),('equal','C5',0.1666666667),('equal','C6',0.1666666667),
('precautionary','C1',0.10),('precautionary','C2',0.18),('precautionary','C3',0.22),('precautionary','C4',0.14),('precautionary','C5',0.18),('precautionary','C6',0.18),
('innovation','C1',0.24),('innovation','C2',0.12),('innovation','C3',0.12),('innovation','C4',0.24),('innovation','C5',0.14),('innovation','C6',0.14);
