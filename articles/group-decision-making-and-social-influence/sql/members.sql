-- members.sql

INSERT INTO members (
    member_id,
    group_id,
    role_name,
    expertise,
    status,
    independent_estimate,
    influenced_estimate
)
VALUES
(1, 1, 'chair', 0.72, 0.91, 0.66, 0.64),
(2, 1, 'analyst', 0.61, 0.42, 0.55, 0.58),
(3, 1, 'domain expert', 0.80, 0.36, 0.68, 0.65),
(4, 1, 'operations lead', 0.47, 0.25, 0.50, 0.55),
(5, 1, 'stakeholder representative', 0.69, 0.50, 0.63, 0.62),
(6, 1, 'risk reviewer', 0.58, 0.34, 0.59, 0.60),
(7, 1, 'technical reviewer', 0.84, 0.44, 0.70, 0.66);
