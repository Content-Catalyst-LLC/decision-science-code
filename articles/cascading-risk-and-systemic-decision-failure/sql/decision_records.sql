-- decision_records.sql

INSERT INTO decision_records (record_id, decision_context, selected_action, rationale, review_trigger)
VALUES
('DR1', 'Cascading risk and systemic decision failure review', 'Diversified Buffered System', 'Strong buffers, low common-mode risk, and high response capacity.', 'Review if common-mode exposure or worst-case continuity deteriorates.');
