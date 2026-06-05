-- sample_queries.sql

-- Expected loss by hazard and strategy.
SELECT
    p.strategy_name,
    p.hazard_id,
    p.probability,
    c.loss,
    p.probability * c.loss AS expected_loss
FROM probabilities p
JOIN consequences c
  ON p.hazard_id = c.hazard_id
 AND p.strategy_name = c.strategy_name
ORDER BY expected_loss DESC;

-- Probability quality by strategy.
SELECT
    strategy_name,
    AVG(
        CASE quality
            WHEN 'high' THEN 1.0
            WHEN 'medium' THEN 0.65
            WHEN 'low' THEN 0.35
            ELSE 0.0
        END
    ) AS average_probability_quality
FROM probabilities
GROUP BY strategy_name
ORDER BY average_probability_quality ASC;

-- Baseline stress exposure.
SELECT
    strategy_name,
    mean_return + shock_probability * shock_size + recovery_credit AS expected_baseline_stress_return
FROM strategies
ORDER BY expected_baseline_stress_return DESC;
