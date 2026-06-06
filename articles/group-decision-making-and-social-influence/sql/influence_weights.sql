-- influence_weights.sql

INSERT INTO influence_weights (group_id, member_id, influence_weight, influence_basis)
VALUES
(1, 1, 0.18, 'authority and expertise'),
(1, 2, 0.13, 'expertise'),
(1, 3, 0.15, 'expertise'),
(1, 4, 0.10, 'operational role'),
(1, 5, 0.14, 'stakeholder knowledge'),
(1, 6, 0.12, 'risk review'),
(1, 7, 0.18, 'technical expertise');
