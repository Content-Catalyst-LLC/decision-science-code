-- policy_contexts.sql

INSERT INTO policy_contexts (context_id, context_name, description)
VALUES
('P1', 'Fast Response Low Resistance', 'Fast response context with strong balancing correction and low resistance.'),
('P2', 'Delayed Response Moderate Resistance', 'Moderate resistance context with substantial implementation delay.'),
('P3', 'High Reinforcement High Resistance', 'High-risk context where reinforcing pressure and resistance dominate.'),
('P4', 'Adaptive Balanced System', 'Adaptive system with meaningful monitoring and balancing correction.'),
('P5', 'Capacity Constrained Policy', 'Policy constrained by delay capacity and resistance.'),
('P6', 'Robust Feedback-Aware Policy', 'Feedback-aware policy with low resistance and strong monitoring.');
