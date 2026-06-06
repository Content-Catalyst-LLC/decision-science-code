-- sample_queries.sql

-- Current expected value by action.
SELECT
    a.action_name,
    SUM(p.payoff_value * s.prior_probability) AS current_expected_value
FROM payoffs p
JOIN actions a ON p.action_id = a.action_id
JOIN states s ON p.state_id = s.state_id
GROUP BY a.action_name
ORDER BY current_expected_value DESC;

-- Expected value with perfect information.
SELECT
    SUM(state_best.best_payoff * state_best.prior_probability) AS expected_value_with_perfect_information
FROM (
    SELECT
        s.state_id,
        s.prior_probability,
        MAX(p.payoff_value) AS best_payoff
    FROM states s
    JOIN payoffs p ON s.state_id = p.state_id
    GROUP BY s.state_id, s.prior_probability
) state_best;

-- Evidence posterior table.
SELECT
    ep.evidence_name,
    ep.evidence_probability,
    s.state_name,
    ep.posterior_probability
FROM evidence_posteriors ep
JOIN states s ON ep.state_id = s.state_id
ORDER BY ep.evidence_name, s.state_name;

-- Expected value by evidence signal and action.
SELECT
    ep.evidence_name,
    a.action_name,
    SUM(p.payoff_value * ep.posterior_probability) AS expected_value_after_evidence
FROM evidence_posteriors ep
JOIN payoffs p ON ep.state_id = p.state_id
JOIN actions a ON p.action_id = a.action_id
GROUP BY ep.evidence_name, a.action_name
ORDER BY ep.evidence_name, expected_value_after_evidence DESC;
