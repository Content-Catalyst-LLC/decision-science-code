-- framing_cases.sql

INSERT INTO framing_cases (frame_id, frame_type, positive_frame, negative_frame, positive_value, negative_value, domain)
VALUES
('F1', 'attribute', '90 percent survival', '10 percent mortality', 0.90, 0.10, 'Healthcare'),
('F2', 'attribute', '95 percent effective', '5 percent ineffective', 0.95, 0.05, 'AI Governance'),
('F3', 'goal', 'investment avoids losses', 'delay increases losses', 0.70, 0.30, 'Infrastructure'),
('F4', 'cost', 'program costs 10 million', 'program avoids 20 million in damages', 0.50, 0.50, 'Public Policy'),
('F5', 'risk', 'low probability catastrophic loss', 'rare but severe downside', 0.08, 0.08, 'Financial Risk');
