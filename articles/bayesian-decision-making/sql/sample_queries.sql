-- sample_queries.sql

-- Bayesian posterior after a positive signal using prior, sensitivity, and false positive rate.
SELECT
    h.case_name,
    h.hypothesis_name,
    p.prior_probability,
    l.sensitivity,
    l.false_positive_rate,
    (l.sensitivity * p.prior_probability) /
      ((l.sensitivity * p.prior_probability) + (l.false_positive_rate * (1 - p.prior_probability)))
      AS posterior_after_positive_signal
FROM hypotheses h
JOIN priors p ON h.hypothesis_id = p.hypothesis_id
JOIN likelihoods l ON h.hypothesis_id = l.hypothesis_id;

-- Bayes factor by case.
SELECT
    h.case_name,
    l.sensitivity / l.false_positive_rate AS bayes_factor_positive
FROM hypotheses h
JOIN likelihoods l ON h.hypothesis_id = l.hypothesis_id
ORDER BY bayes_factor_positive DESC;

-- Utility table for action comparison.
SELECT
    case_name,
    action_name,
    state_name,
    utility_value
FROM utilities
ORDER BY case_name, action_name, state_name;
