-- accountability_records.sql

INSERT INTO accountability_records (actor_id, actor_name, decision_influence, accountability, role_name, notes)
VALUES
('A1', 'Executive Sponsor', 0.86, 0.76, 'approver', 'High authority with formal accountability.'),
('A2', 'Decision Owner', 0.78, 0.82, 'owner', 'Owns context, rationale, evidence, and monitoring.'),
('A3', 'Technical Review Team', 0.68, 0.54, 'reviewer', 'Strong influence but limited formal outcome accountability.'),
('A4', 'Vendor', 0.62, 0.34, 'external provider', 'Influences system behavior but weak accountability unless contract governs it.'),
('A5', 'Implementation Team', 0.58, 0.70, 'implementer', 'Owns operational execution and reporting.'),
('A6', 'Affected Stakeholders', 0.24, 0.18, 'affected group', 'High exposure but limited institutional influence.'),
('A7', 'Audit Function', 0.44, 0.62, 'assurance', 'Reviews records, controls, and corrective action.');
