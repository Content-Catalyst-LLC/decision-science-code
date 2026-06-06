-- governance_designs.sql

INSERT INTO governance_designs (design_id, design_name, description)
VALUES
('G1', 'Informal Managerial Approval', 'Fast lightweight approval with weak records, review, accountability, and corrective capacity.'),
('G2', 'Committee Review', 'Committee-based review with moderate legitimacy but responsibility diffusion.'),
('G3', 'Risk-Tiered Governance', 'Governance requirements scaled by decision risk, stakes, and uncertainty.'),
('G4', 'Independent Challenge Model', 'Strong independent review and dissent protection with higher process burden.'),
('G5', 'Decision Record and Audit Model', 'Strong documentation, auditability, and institutional memory.'),
('G6', 'Adaptive Accountability System', 'Governance with records, review triggers, monitoring, corrective authority, and learning loops.');
