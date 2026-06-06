-- groups.sql

INSERT INTO groups_table (
    group_id,
    domain,
    true_value,
    authority_concentration,
    consensus_pressure,
    shared_information,
    unique_information,
    decision_rule
)
VALUES
(1, 'Public Policy', 0.62, 0.30, 0.45, 8, 5, 'consultative decision'),
(2, 'Healthcare', 0.78, 0.22, 0.25, 10, 4, 'expert recommendation'),
(3, 'Financial Risk', 0.44, 0.55, 0.65, 6, 8, 'committee vote'),
(4, 'Infrastructure', 0.56, 0.42, 0.58, 7, 7, 'supermajority'),
(5, 'AI Governance', 0.69, 0.48, 0.70, 5, 9, 'review board');
