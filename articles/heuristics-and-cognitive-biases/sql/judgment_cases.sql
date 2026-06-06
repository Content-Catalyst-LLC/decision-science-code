-- judgment_cases.sql

INSERT INTO judgment_cases (
    case_id,
    domain,
    bias_profile,
    base_rate,
    evidence_signal,
    anchor,
    salience_multiplier,
    confirming_evidence,
    disconfirming_evidence,
    judged_probability,
    confidence,
    outcome
)
VALUES
(1, 'Public Policy', 'availability', 0.42, 0.08, 0.70, 1.45, 0.16, 0.08, 0.72, 0.77, 1),
(2, 'Healthcare', 'representativeness', 0.62, -0.10, 0.55, 1.10, 0.12, 0.20, 0.54, 0.56, 0),
(3, 'Financial Risk', 'anchoring', 0.30, 0.12, 0.80, 0.95, 0.11, 0.07, 0.61, 0.64, 0),
(4, 'Infrastructure', 'confirmation', 0.38, 0.09, 0.60, 1.20, 0.24, 0.06, 0.67, 0.71, 1),
(5, 'AI Governance', 'overconfidence', 0.44, 0.16, 0.72, 1.15, 0.18, 0.10, 0.60, 0.75, 0);
