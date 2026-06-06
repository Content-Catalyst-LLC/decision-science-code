# decision_science_financial_risk_workflow.R
# Base R workflow for financial risk decision science:
# regime stress testing, capital buffer review, and generated outputs.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)

if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}

setwd(article_root)

tables_dir <- file.path(article_root, "outputs", "tables")
figures_dir <- file.path(article_root, "outputs", "figures")
dir.create(tables_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(figures_dir, recursive = TRUE, showWarnings = FALSE)

portfolios <- read.csv(file.path(article_root, "data", "synthetic_portfolio_profiles.csv"), stringsAsFactors = FALSE)
scenarios <- read.csv(file.path(article_root, "data", "synthetic_scenarios.csv"), stringsAsFactors = FALSE)
scenario_performance <- read.csv(file.path(article_root, "data", "synthetic_scenario_performance.csv"), stringsAsFactors = FALSE)

scenario_probs <- scenarios$probability
names(scenario_probs) <- scenarios$scenario

expected_loss <- (
  portfolios$normal * scenario_probs["normal"] +
    portfolios$recession * scenario_probs["recession"] +
    portfolios$liquidity_shock * scenario_probs["liquidity_shock"] +
    portfolios$systemic_stress * scenario_probs["systemic_stress"]
)

loss_matrix <- portfolios[, c("normal", "recession", "liquidity_shock", "systemic_stress")]
worst_case <- apply(loss_matrix, 1, min)
regime_dispersion <- apply(loss_matrix, 1, sd)
capital_buffer_needed <- abs(worst_case) * 1.15

risk_resilience_score <- (
  0.24 * portfolios$liquidity_score +
    0.22 * portfolios$governance_score +
    0.18 * portfolios$model_confidence -
    0.16 * abs(expected_loss) / 30 -
    0.14 * abs(worst_case) / 30 -
    0.06 * regime_dispersion / 10
)

results <- data.frame(
  portfolio = portfolios$portfolio,
  expected_loss = round(expected_loss, 4),
  worst_case = round(worst_case, 4),
  regime_dispersion = round(regime_dispersion, 4),
  capital_buffer_needed = round(capital_buffer_needed, 4),
  liquidity_score = portfolios$liquidity_score,
  governance_score = portfolios$governance_score,
  model_confidence = portfolios$model_confidence,
  risk_resilience_score = round(risk_resilience_score, 4),
  stringsAsFactors = FALSE
)

results$review_flag <- ifelse(
  results$worst_case < -20 |
    results$liquidity_score < 0.45 |
    results$governance_score < 0.55 |
    results$model_confidence < 0.55 |
    results$capital_buffer_needed > 25,
  "review",
  "acceptable"
)

results$rank <- rank(-results$risk_resilience_score, ties.method = "min")
results <- results[order(results$rank), ]

write.csv(portfolios, file.path(tables_dir, "financial_risk_portfolio_profiles.csv"), row.names = FALSE)
write.csv(scenario_performance, file.path(tables_dir, "financial_risk_scenario_performance.csv"), row.names = FALSE)
write.csv(results, file.path(tables_dir, "financial_risk_regime_stress_results.csv"), row.names = FALSE)

png(file.path(figures_dir, "financial_risk_worst_case_losses.png"), width = 1200, height = 800)
barplot(
  results$worst_case,
  names.arg = results$portfolio,
  las = 2,
  main = "Worst-Case Portfolio Loss Across Regimes",
  ylab = "Worst-case loss (%)"
)
grid()
dev.off()

png(file.path(figures_dir, "financial_risk_capital_buffer_needed.png"), width = 1200, height = 800)
barplot(
  results$capital_buffer_needed,
  names.arg = results$portfolio,
  las = 2,
  main = "Capital Buffer Needed Under Stress",
  ylab = "Capital buffer index"
)
grid()
dev.off()

print(results)
