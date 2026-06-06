# decision_science_crisis_management_workflow.R
# Base R workflow for crisis-management decision science.

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

options <- read.csv(file.path(article_root, "data", "synthetic_crisis_response_options.csv"), stringsAsFactors = FALSE)
scenarios <- read.csv(file.path(article_root, "data", "synthetic_scenarios.csv"), stringsAsFactors = FALSE)
scenario_performance <- read.csv(file.path(article_root, "data", "synthetic_scenario_performance.csv"), stringsAsFactors = FALSE)

scenario_probs <- scenarios$probability
names(scenario_probs) <- scenarios$scenario

scenario_matrix <- options[, c("baseline", "rapid_escalation", "resource_constraint", "public_trust_stress", "cascading_failure")]

options$expected_response_value <- (
  options$baseline * scenario_probs["baseline"] +
    options$rapid_escalation * scenario_probs["rapid_escalation"] +
    options$resource_constraint * scenario_probs["resource_constraint"] +
    options$public_trust_stress * scenario_probs["public_trust_stress"] +
    options$cascading_failure * scenario_probs["cascading_failure"]
)

options$worst_case_value <- apply(scenario_matrix, 1, min)
options$scenario_dispersion <- apply(scenario_matrix, 1, sd)

options$crisis_decision_score <- (
  0.22 * options$expected_response_value / 100 +
    0.20 * options$worst_case_value / 100 -
    0.08 * options$scenario_dispersion / 30 +
    0.12 * options$speed_score +
    0.10 * options$feasibility_score +
    0.14 * options$equity_score +
    0.12 * options$trust_score +
    0.10 * options$continuity_score +
    0.10 * options$adaptability
)

options$review_flag <- ifelse(
  options$worst_case_value < 50 |
    options$equity_score < 0.55 |
    options$trust_score < 0.55 |
    options$continuity_score < 0.50 |
    options$feasibility_score < 0.50,
  "review",
  "acceptable"
)

options$rank <- rank(-options$crisis_decision_score, ties.method = "min")
results <- options[order(options$rank), ]

write.csv(options, file.path(tables_dir, "crisis_response_option_profiles.csv"), row.names = FALSE)
write.csv(scenario_performance, file.path(tables_dir, "crisis_response_scenario_performance.csv"), row.names = FALSE)
write.csv(results, file.path(tables_dir, "crisis_response_decision_results.csv"), row.names = FALSE)

png(file.path(figures_dir, "crisis_response_scores.png"), width = 1200, height = 800)
barplot(results$crisis_decision_score, names.arg = results$option, las = 2, main = "Crisis Response Decision Scores", ylab = "Decision score")
grid()
dev.off()

png(file.path(figures_dir, "crisis_worst_case_value.png"), width = 1200, height = 800)
barplot(results$worst_case_value, names.arg = results$option, las = 2, main = "Worst-Case Crisis Response Value", ylab = "Worst-case scenario value")
grid()
dev.off()

print(results)
