-- decisions.sql

INSERT INTO decisions (record_id, decision_context, decision_owner, recommendation_owner, decision_date, selected_action, rationale)
VALUES
('DR-001', 'AI deployment approval', 'AI governance board', 'model risk team', '2026-01-15', 'conditional deployment', 'Proceed with monitoring and human oversight'),
('DR-002', 'Infrastructure investment', 'capital committee', 'infrastructure planning office', '2026-02-10', 'staged investment', 'Select robust pathway with review gates'),
('DR-003', 'Healthcare protocol change', 'clinical governance board', 'quality improvement team', '2026-03-05', 'protocol revision', 'Reduce care variation while monitoring safety'),
('DR-004', 'Strategic market entry', 'strategy committee', 'growth team', '2026-04-12', 'market entry', 'Enter market with limited evidence and high assumed growth'),
('DR-005', 'Climate adaptation pathway', 'adaptation steering group', 'resilience planning team', '2026-05-01', 'adaptive pathway', 'Preserve reversibility under climate uncertainty');
