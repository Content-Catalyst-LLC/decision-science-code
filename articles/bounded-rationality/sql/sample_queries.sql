-- sample_queries.sql

-- Adjusted utility and net value by alternative.
SELECT
    alternative_id,
    decision_context,
    option_name,
    raw_utility,
    implementation_risk,
    uncertainty_penalty,
    search_order,
    raw_utility - implementation_risk - uncertainty_penalty AS adjusted_utility
FROM alternatives
ORDER BY decision_context, search_order;

-- First acceptable option by decision context using a simple fixed threshold.
SELECT
    decision_context,
    option_name,
    raw_utility - implementation_risk - uncertainty_penalty AS adjusted_utility,
    search_order
FROM alternatives
WHERE raw_utility - implementation_risk - uncertainty_penalty >= 0.70
ORDER BY decision_context, search_order;

-- Adaptive aspiration update.
SELECT
    period,
    domain,
    aspiration,
    feedback,
    learning_rate,
    aspiration + learning_rate * (feedback - aspiration) AS next_aspiration
FROM aspiration_levels
ORDER BY period;
