# future_directions_decision_science_workflow.R
# Base R workflow for comparing future decision science pathways:
# AI readiness, governance, uncertainty capability, participation, reproducibility,
# systems modeling, ethics, adaptive capacity, burden, and failure risk.

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

pathways <- read.csv(file.path(article_root, "data", "synthetic_future_pathways.csv"), stringsAsFactors = FALSE)
maturity <- read.csv(file.path(article_root, "data", "synthetic_maturity_records.csv"), stringsAsFactors = FALSE)
review_triggers <- read.csv(file.path(article_root, "data", "synthetic_review_triggers.csv"), stringsAsFactors = FALSE)

pathways$future_decision_score <- (
  0.12 * pathways$ai_readiness +
    0.14 * pathways$governance_maturity +
    0.14 * pathways$uncertainty_capability +
    0.12 * pathways$participatory_legitimacy +
    0.12 * pathways$reproducibility +
    0.12 * pathways$systems_modeling +
    0.14 * pathways$ethical_accountability +
    0.14 * pathways$adaptive_capacity -
    0.04 * pathways$process_burden -
    0.12 * pathways$failure_risk
)

pathways$review_flag <- ifelse(
  pathways$governance_maturity < 0.60 |
    pathways$uncertainty_capability < 0.60 |
    pathways$ethical_accountability < 0.60 |
    pathways$adaptive_capacity < 0.60 |
    pathways$failure_risk > 0.55,
  "review",
  "acceptable"
)

pathways$rank <- rank(-pathways$future_decision_score, ties.method = "min")
results <- pathways[order(pathways$rank), ]

maturity$review_flag <- ifelse(maturity$gap >= 0.30, "review", "acceptable")

write.csv(results, file.path(tables_dir, "future_decision_science_pathways.csv"), row.names = FALSE)
write.csv(maturity, file.path(tables_dir, "future_maturity_records.csv"), row.names = FALSE)
write.csv(review_triggers, file.path(tables_dir, "review_triggers.csv"), row.names = FALSE)

png(file.path(figures_dir, "future_decision_science_scores.png"), width = 1200, height = 800)
barplot(
  results$future_decision_score,
  names.arg = results$pathway,
  las = 2,
  main = "Future Decision Science Pathway Scores",
  ylab = "Future decision score"
)
grid()
dev.off()

png(file.path(figures_dir, "future_decision_failure_risk.png"), width = 1200, height = 800)
barplot(
  results$failure_risk,
  names.arg = results$pathway,
  las = 2,
  main = "Failure Risk by Future Decision Pathway",
  ylab = "Failure risk"
)
grid()
dev.off()

print(results)
