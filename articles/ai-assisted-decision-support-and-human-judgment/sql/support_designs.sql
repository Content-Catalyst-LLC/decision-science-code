-- support_designs.sql

INSERT INTO support_designs (design_id, design_name, description)
VALUES
('S1', 'Manual Judgment Baseline', 'Unaided human judgment with limited monitoring and no model performance.'),
('S2', 'AI Evidence Assistant', 'AI gathers and summarizes evidence while humans retain strong review authority.'),
('S3', 'AI Recommendation with Review', 'AI recommends actions with required human review and moderate automation-bias risk.'),
('S4', 'AI Triage with Appeal', 'AI prioritizes cases while preserving appeal rights and monitoring.'),
('S5', 'Automated Decision with Monitoring', 'AI automates decisions with weak human oversight and high overreliance risk.'),
('S6', 'Adaptive Human-AI Governance', 'AI supports decisions with strong uncertainty visibility, oversight, contestability, monitoring, and accountability.');
