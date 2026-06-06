-- thresholds.sql

INSERT INTO thresholds (threshold_name, threshold_value, description)
VALUES
('minimum_acceptable_performance', 0.70, 'Minimum satisfactory performance under a plausible future.'),
('high_regret_threshold', 0.35, 'Maximum regret level triggering review.'),
('low_worst_case_threshold', 0.50, 'Worst-case performance level triggering review.'),
('low_pass_rate_threshold', 0.50, 'Minimum acceptable scenario pass rate.');
