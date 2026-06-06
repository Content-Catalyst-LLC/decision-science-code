-- decision_records.sql

INSERT INTO decision_records (record_id, decision_context, selected_action, rationale, review_trigger)
VALUES
('DR1', 'Regret and minimax strategy review', 'Staged Optionality Strategy', 'Strong minimax-regret profile and broad threshold compliance.', 'Review if scenario set or payoff assumptions materially change.');
