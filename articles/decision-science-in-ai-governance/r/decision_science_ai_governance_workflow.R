# decision_science_ai_governance_workflow.R
# Base R workflow for AI governance decision science:
# risk scenarios, oversight, transparency, equity, and review flags.

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

options <- read.csv(file.path(article_root, "data", "synthetic_ai_governance_options.csv"), stringsAsFactors = FALSE)
scenarios <- read.csv(file.path(article_root, "data", "synthetic_scenarios.csv"), stringsAsFactors = FALSE)
scenario_performance <- read.csv(file.path(article_root, "data", "synthetic_scenario_performance.csv"), stringsAsFactors = FALSE)

scenario_probs <- scenarios$probability
names(scenario_probs) <- scenarios$scenario

scenario_matrix <- options[, c("baseline_value", "safety_stress", "equity_stress", "security_stress", "drift_stress")]

options$expected_governance_value <- (
  options$baseline_value * scenario_probs["baseline_value"] +
    options$safety_stress * scenario_probs["safety_stress"] +
    options$equity_stress * scenario_probs["equity_stress"] +
    options$security_stress * scenario_probs["security_stress"] +
    options$drift_stress * scenario_probs["drift_stress"]
)

options$worst_case_value <- apply(scenario_matrix, 1, min)
options$scenario_dispersion <- apply(scenario_matrix, 1, sd)

options$ai_governance_score <- (
  0.20 * options$expected_governance_value / 100 +
    0.18 * options$worst_case_value / 100 -
    0.08 * options$scenario_dispersion / 30 +
    0.14 * options$evidence_quality +
    0.14 * options$oversight_strength +
    0.12 * options$equity_score +
    0.10 * options$transparency_score +
    0.08 * options$security_readiness +
    0.06 * options$implementation_feasibility
)

options$review_flag <- ifelse(
  options$worst_case_value < 50 |
    options$evidence_quality < 0.60 |
    options$oversight_strength < 0.60 |
    options$equity_score < 0.55 |
    options$security_readiness < 0.55,
  "review",
  "acceptable"
)

options$rank <- rank(-options$ai_governance_score, ties.method = "min")
results <- options[order(options$rank), ]

write.csv(options, file.path(tables_dir, "ai_governance_option_profiles.csv"), row.names = FALSE)
write.csv(scenario_performance, file.path(tables_dir, "ai_governance_scenario_performance.csv"), row.names = FALSE)
write.csv(results, file.path(tables_dir, "ai_governance_decision_results.csv"), row.names = FALSE)

png(file.path(figures_dir, "ai_governance_scores.png"), width = 1200, height = 800)
barplot(
  results$ai_governance_score,
  names.arg = results$option,
  las = 2,
  main = "AI Governance Decision Scores",
  ylab = "Decision score"
)
grid()
dev.off()

png(file.path(figures_dir, "ai_governance_worst_case_value.png"), width = 1200, height = 800)
barplot(
  results$worst_case_value,
  names.arg = results$option,
  las = 2,
  main = "Worst-Case AI Governance Value",
  ylab = "Worst-case value"
)
grid()
dev.off()

print(results)
