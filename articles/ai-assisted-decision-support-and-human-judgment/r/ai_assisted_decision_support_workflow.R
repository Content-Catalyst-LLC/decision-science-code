# ai_assisted_decision_support_workflow.R
# Base R workflow for AI-assisted decision support:
# model performance, oversight, contestability, fairness, accountability,
# automation-bias risk, and governance review flags.

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

designs <- read.csv(file.path(article_root, "data", "synthetic_ai_support_designs.csv"), stringsAsFactors = FALSE)
oversight <- read.csv(file.path(article_root, "data", "synthetic_oversight_records.csv"), stringsAsFactors = FALSE)
review_triggers <- read.csv(file.path(article_root, "data", "synthetic_review_triggers.csv"), stringsAsFactors = FALSE)

designs$decision_support_score <- (
  0.16 * designs$model_performance +
    0.14 * designs$uncertainty_visibility +
    0.16 * designs$human_oversight +
    0.14 * designs$contestability +
    0.14 * designs$fairness_review +
    0.14 * designs$accountability +
    0.10 * designs$monitoring_strength -
    0.10 * designs$automation_bias_risk -
    0.04 * designs$process_burden
)

designs$review_flag <- ifelse(
  designs$human_oversight < 0.60 |
    designs$contestability < 0.60 |
    designs$fairness_review < 0.60 |
    designs$accountability < 0.60 |
    designs$automation_bias_risk > 0.60,
  "review",
  "acceptable"
)

designs$rank <- rank(-designs$decision_support_score, ties.method = "min")
results <- designs[order(designs$rank), ]

write.csv(results, file.path(tables_dir, "ai_decision_support_design_results.csv"), row.names = FALSE)
write.csv(oversight, file.path(tables_dir, "oversight_records.csv"), row.names = FALSE)
write.csv(review_triggers, file.path(tables_dir, "review_triggers.csv"), row.names = FALSE)

png(file.path(figures_dir, "ai_decision_support_scores.png"), width = 1200, height = 800)
barplot(
  results$decision_support_score,
  names.arg = results$design,
  las = 2,
  main = "AI-Assisted Decision Support Scores",
  ylab = "Decision-support score"
)
grid()
dev.off()

png(file.path(figures_dir, "automation_bias_risk.png"), width = 1200, height = 800)
barplot(
  results$automation_bias_risk,
  names.arg = results$design,
  las = 2,
  main = "Automation-Bias Risk by Design",
  ylab = "Automation-bias risk"
)
grid()
dev.off()

print(results)
