-- sample_queries.sql

-- Composite decision quality score.
SELECT
    decision_name,
    (
        0.16 * objective_clarity +
        0.15 * alternative_quality +
        0.17 * information_strength +
        0.18 * tradeoff_transparency +
        0.18 * uncertainty_treatment +
        0.16 * implementation_readiness
    ) AS decision_quality_score
FROM decisions
ORDER BY decision_quality_score DESC;

-- Strategic alignment score.
SELECT
    decision_name,
    (
        0.45 * strategic_fit +
        0.30 * capability_fit +
        0.25 * value_fit
    ) AS strategic_alignment_score
FROM decisions
ORDER BY strategic_alignment_score DESC;

-- Review queue.
SELECT
    decision_name,
    (
        0.16 * objective_clarity +
        0.15 * alternative_quality +
        0.17 * information_strength +
        0.18 * tradeoff_transparency +
        0.18 * uncertainty_treatment +
        0.16 * implementation_readiness
    ) AS decision_quality_score,
    (
        0.45 * strategic_fit +
        0.30 * capability_fit +
        0.25 * value_fit
    ) AS strategic_alignment_score
FROM decisions
WHERE
    (
        0.16 * objective_clarity +
        0.15 * alternative_quality +
        0.17 * information_strength +
        0.18 * tradeoff_transparency +
        0.18 * uncertainty_treatment +
        0.16 * implementation_readiness
    ) < 0.70
    OR
    (
        0.45 * strategic_fit +
        0.30 * capability_fit +
        0.25 * value_fit
    ) < 0.70;
