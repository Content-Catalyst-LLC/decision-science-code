# democratic_public_reasoning_workflow.R
# Base R workflow for decision science and democratic public reasoning:
# evidence quality, participation, transparency, legitimacy, contestability,
# equity, accountability, process burden, and public-trust risk.

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

processes <- read.csv(file.path(article_root, "data", "synthetic_democratic_processes.csv"), stringsAsFactors = FALSE)
participation <- read.csv(file.path(article_root, "data", "synthetic_participation_records.csv"), stringsAsFactors = FALSE)
review_triggers <- read.csv(file.path(article_root, "data", "synthetic_review_triggers.csv"), stringsAsFactors = FALSE)

processes$democratic_decision_quality <- (
  0.14 * processes$evidence_quality +
    0.12 * processes$transparency +
    0.14 * processes$participation +
    0.14 * processes$procedural_fairness +
    0.12 * processes$contestability +
    0.12 * processes$equity_review +
    0.12 * processes$accountability +
    0.10 * processes$uncertainty_communication -
    0.05 * processes$process_burden -
    0.10 * processes$public_trust_risk
)

processes$review_flag <- ifelse(
  processes$participation < 0.55 |
    processes$procedural_fairness < 0.55 |
    processes$contestability < 0.55 |
    processes$equity_review < 0.55 |
    processes$accountability < 0.55 |
    processes$public_trust_risk > 0.60,
  "review",
  "acceptable"
)

processes$rank <- rank(-processes$democratic_decision_quality, ties.method = "min")
results <- processes[order(processes$rank), ]

participation$standing_access_gap <- pmax(0, participation$standing - participation$access)
participation$participation_review_flag <- ifelse(
  participation$standing_access_gap > 0.30 | participation$response_to_input < 0.50,
  "review",
  "acceptable"
)

write.csv(results, file.path(tables_dir, "democratic_public_reasoning_results.csv"), row.names = FALSE)
write.csv(participation, file.path(tables_dir, "participation_records.csv"), row.names = FALSE)
write.csv(review_triggers, file.path(tables_dir, "review_triggers.csv"), row.names = FALSE)

png(file.path(figures_dir, "democratic_decision_quality_scores.png"), width = 1200, height = 800)
barplot(
  results$democratic_decision_quality,
  names.arg = results$process,
  las = 2,
  main = "Democratic Decision Quality by Process",
  ylab = "Democratic decision quality"
)
grid()
dev.off()

png(file.path(figures_dir, "public_trust_risk.png"), width = 1200, height = 800)
barplot(
  results$public_trust_risk,
  names.arg = results$process,
  las = 2,
  main = "Public Trust Risk by Process",
  ylab = "Public trust risk"
)
grid()
dev.off()

print(results)
