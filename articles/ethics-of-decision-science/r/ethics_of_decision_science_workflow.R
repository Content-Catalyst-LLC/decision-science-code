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

alternatives <- read.csv(file.path(article_root, "data", "synthetic_ethical_decision_alternatives.csv"), stringsAsFactors = FALSE)
distribution <- read.csv(file.path(article_root, "data", "synthetic_distributional_impacts.csv"), stringsAsFactors = FALSE)
criteria <- read.csv(file.path(article_root, "data", "synthetic_ethical_criteria.csv"), stringsAsFactors = FALSE)

alternatives$ethical_value_score <- (
  0.18 * alternatives$expected_value / 100 +
  0.18 * alternatives$equity_score +
  0.16 * alternatives$safety_score +
  0.14 * alternatives$legitimacy_score +
  0.10 * alternatives$transparency_score +
  0.10 * alternatives$contestability_score +
  0.08 * alternatives$reversibility_score +
  0.06 * alternatives$accountability_score
)

alternatives$ethical_risk_score <- (
  0.34 * alternatives$harm_risk +
  0.22 * alternatives$opacity_risk +
  0.24 * alternatives$exclusion_risk +
  0.20 * (1 - alternatives$accountability_score)
)

alternatives$net_ethical_score <- alternatives$ethical_value_score - 0.42 * alternatives$ethical_risk_score
alternatives$review_flag <- ifelse(
  alternatives$equity_score < 0.55 |
  alternatives$safety_score < 0.55 |
  alternatives$legitimacy_score < 0.55 |
  alternatives$contestability_score < 0.55 |
  alternatives$ethical_risk_score > 0.55,
  "review", "acceptable"
)
alternatives$rank <- rank(-alternatives$net_ethical_score, ties.method = "min")
results <- alternatives[order(alternatives$rank), ]

write.csv(criteria, file.path(tables_dir, "ethical_criteria.csv"), row.names = FALSE)
write.csv(distribution, file.path(tables_dir, "distributional_impacts.csv"), row.names = FALSE)
write.csv(results, file.path(tables_dir, "ethical_decision_results.csv"), row.names = FALSE)

png(file.path(figures_dir, "ethical_decision_scores.png"), width = 1200, height = 800)
barplot(results$net_ethical_score, names.arg = results$alternative, las = 2, main = "Net Ethical Decision Scores", ylab = "Net ethical score")
grid()
dev.off()

png(file.path(figures_dir, "ethical_risk_scores.png"), width = 1200, height = 800)
barplot(results$ethical_risk_score, names.arg = results$alternative, las = 2, main = "Ethical Risk Scores", ylab = "Ethical risk")
grid()
dev.off()

print(results)
