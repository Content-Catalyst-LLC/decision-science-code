-- alternatives.sql

INSERT INTO alternatives (
    alternative_id,
    decision_context,
    option_name,
    raw_utility,
    implementation_risk,
    uncertainty_penalty,
    search_order
)
VALUES
('A1', 'Public Policy', 'incremental pilot', 0.68, 0.08, 0.04, 1),
('A2', 'Public Policy', 'full deployment', 0.82, 0.18, 0.06, 2),
('A3', 'Healthcare', 'monitoring protocol', 0.70, 0.06, 0.03, 1),
('A4', 'Healthcare', 'intervention protocol', 0.88, 0.16, 0.05, 2),
('A5', 'Financial Risk', 'hedge position', 0.76, 0.10, 0.07, 1),
('A6', 'Financial Risk', 'liquidity reserve', 0.72, 0.05, 0.04, 2);
