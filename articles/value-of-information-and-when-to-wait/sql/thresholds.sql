-- thresholds.sql
-- Included for consistency with related Decision Science companion workflows.

CREATE TABLE IF NOT EXISTS thresholds (
    threshold_name TEXT PRIMARY KEY,
    threshold_value REAL,
    description TEXT
);

INSERT INTO thresholds (threshold_name, threshold_value, description)
VALUES
('positive_net_value_waiting', 0, 'Waiting is favored when net value of waiting is greater than zero.'),
('decision_change_probability_review', 0.35, 'Review if evidence has meaningful probability of changing action.');
