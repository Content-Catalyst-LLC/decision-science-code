# decision_governance_accountability_workflow.R
# Base R workflow for decision governance:
# decision rights, evidence standards, accountability, review, monitoring, and governance burden.

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

governance_designs <- read.csv(file.path(article_root, "data", "synthetic_governance_designs.csv"), stringsAsFactors = FALSE)
accountability_records <- read.csv(file.path(article_root, "data", "synthetic_accountability_records.csv"), stringsAsFactors = FALSE)
review_triggers <- read.csv(file.path(article_root, "data", "synthetic_review_triggers.csv"), stringsAsFactors = FALSE)

governance_designs$governance_score <- (
  0.16 * governance_designs$decision_quality +
    0.14 * governance_designs$legitimacy +
    0.16 * governance_designs$accountability +
    0.12 * governance_designs$implementation_reliability +
    0.10 * governance_designs$evidence_traceability +
    0.10 * governance_designs$review_strength +
    0.10 * governance_designs$monitoring_strength +
    0.10 * governance_designs$corrective_capacity -
    0.08 * governance_designs$risk_exposure -
    0.04 * governance_designs$process_burden
)

governance_designs$review_flag <- ifelse(
  governance_designs$accountability < 0.60 |
    governance_designs$evidence_traceability < 0.60 |
    governance_designs$review_strength < 0.60 |
    governance_designs$corrective_capacity < 0.60 |
    governance_designs$risk_exposure > 0.60,
  "review",
  "acceptable"
)

governance_designs$rank <- rank(-governance_designs$governance_score, ties.method = "min")
results <- governance_designs[order(governance_designs$rank), ]

accountability_records$responsibility_gap <- pmax(0, accountability_records$decision_influence - accountability_records$accountability)
accountability_records$gap_review_flag <- ifelse(accountability_records$responsibility_gap >= 0.28, "review", "acceptable")

write.csv(results, file.path(tables_dir, "decision_governance_design_results.csv"), row.names = FALSE)
write.csv(accountability_records, file.path(tables_dir, "accountability_records.csv"), row.names = FALSE)
write.csv(review_triggers, file.path(tables_dir, "review_triggers.csv"), row.names = FALSE)

png(file.path(figures_dir, "decision_governance_scores.png"), width = 1200, height = 800)
barplot(
  results$governance_score,
  names.arg = results$design,
  las = 2,
  main = "Decision Governance Design Scores",
  ylab = "Governance score"
)
grid()
dev.off()

png(file.path(figures_dir, "decision_governance_risk_burden.png"), width = 1200, height = 800)
barplot(
  results$risk_exposure,
  names.arg = results$design,
  las = 2,
  main = "Governance Risk Exposure by Design",
  ylab = "Risk exposure"
)
grid()
dev.off()

print(results)
