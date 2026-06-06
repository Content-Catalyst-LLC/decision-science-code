-- oversight_records.sql

INSERT INTO oversight_records (role_id, role_name, authority, information_access, time_available, training, override_rights, independence, oversight_strength, notes)
VALUES
('R1', 'Decision Owner', 0.86, 0.82, 0.72, 0.78, 0.90, 0.76, 0.81, 'Owns final decision and rationale.'),
('R2', 'Human Reviewer', 0.72, 0.74, 0.58, 0.72, 0.82, 0.70, 0.71, 'Reviews AI output and may override.'),
('R3', 'Model Owner', 0.62, 0.88, 0.70, 0.84, 0.54, 0.66, 0.70, 'Owns validation, monitoring, and model limits.'),
('R4', 'Data Owner', 0.56, 0.84, 0.66, 0.76, 0.46, 0.60, 0.65, 'Owns data quality, provenance, and access.'),
('R5', 'Governance Body', 0.88, 0.72, 0.62, 0.70, 0.84, 0.86, 0.77, 'Approves high-risk use cases and corrective action.'),
('R6', 'Affected Stakeholder', 0.24, 0.40, 0.34, 0.28, 0.36, 0.50, 0.35, 'Has limited influence unless contestability pathway exists.'),
('R7', 'Audit Function', 0.68, 0.78, 0.64, 0.74, 0.64, 0.88, 0.73, 'Tests controls, records, performance, and accountability.');
