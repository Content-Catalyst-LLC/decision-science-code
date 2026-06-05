# decision_science_summary_reporting.R
# Base R reporting workflow for What Is Decision Science?
# Reads Python outputs and creates diagnostic summaries and plots.

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

if (!dir.exists(tables_dir)) {
  dir.create(tables_dir, recursive = TRUE)
}

if (!dir.exists(figures_dir)) {
  dir.create(figures_dir, recursive = TRUE)
}

summary_path <- file.path(tables_dir, "decision_summary.csv")
regret_path <- file.path(tables_dir, "decision_regret_matrix.csv")
mcda_path <- file.path(tables_dir, "decision_mcda_scores.csv")
sensitivity_path <- file.path(tables_dir, "decision_sensitivity_analysis.csv")

required_files <- c(summary_path, regret_path, mcda_path, sensitivity_path)
missing_files <- required_files[!file.exists(required_files)]

if (length(missing_files) > 0) {
  stop(paste("Missing required files. Run the Python workflow first:", paste(missing_files, collapse = ", ")))
}

decision_summary <- read.csv(summary_path, stringsAsFactors = FALSE)
regret_matrix <- read.csv(regret_path, stringsAsFactors = FALSE)
mcda_scores <- read.csv(mcda_path, stringsAsFactors = FALSE)
sensitivity <- read.csv(sensitivity_path, stringsAsFactors = FALSE)

decision_summary <- decision_summary[order(
  -decision_summary$robustness_share,
  -decision_summary$expected_value,
  decision_summary$maximum_regret,
  -decision_summary$mcda_score
), ]

top_alternative <- decision_summary$alternative[1]

regret_profile <- aggregate(
  regret ~ alternative,
  data = regret_matrix,
  FUN = function(x) c(mean = mean(x), max = max(x), sd = sd(x))
)

regret_profile_expanded <- data.frame(
  alternative = regret_profile$alternative,
  average_regret = regret_profile$regret[, "mean"],
  maximum_regret_profile = regret_profile$regret[, "max"],
  regret_sd = regret_profile$regret[, "sd"]
)

sensitivity_instability <- aggregate(
  ranking_changed ~ changed_criterion,
  data = sensitivity,
  FUN = function(x) mean(as.logical(x))
)

names(sensitivity_instability) <- c("criterion", "ranking_instability_rate")

diagnostic_report <- merge(decision_summary, regret_profile_expanded, by = "alternative", all.x = TRUE)
diagnostic_report <- diagnostic_report[order(
  -diagnostic_report$robustness_share,
  diagnostic_report$maximum_regret_profile,
  -diagnostic_report$expected_value
), ]

diagnostic_report$interpretive_status <- ifelse(
  diagnostic_report$alternative == top_alternative,
  "current recommended candidate",
  ifelse(
    diagnostic_report$maximum_regret_profile > quantile(diagnostic_report$maximum_regret_profile, 0.75),
    "regret-sensitive alternative",
    "comparison alternative"
  )
)

write.csv(
  diagnostic_report,
  file.path(tables_dir, "decision_diagnostic_report.csv"),
  row.names = FALSE
)

write.csv(
  sensitivity_instability,
  file.path(tables_dir, "decision_weight_instability_summary.csv"),
  row.names = FALSE
)

plot_bar <- function(values, names, title, y_label, file_name) {
  png(file.path(figures_dir, file_name), width = 1200, height = 750)
  barplot(
    values,
    names.arg = names,
    las = 2,
    ylab = y_label,
    main = title
  )
  grid()
  dev.off()
}

plot_bar(
  decision_summary$expected_value,
  decision_summary$alternative,
  "Expected Value by Alternative",
  "Expected value",
  "expected_value_by_alternative.png"
)

plot_bar(
  decision_summary$maximum_regret,
  decision_summary$alternative,
  "Maximum Regret by Alternative",
  "Maximum regret",
  "maximum_regret_by_alternative.png"
)

plot_bar(
  decision_summary$robustness_share,
  decision_summary$alternative,
  "Robustness Share by Alternative",
  "Share of scenarios meeting threshold",
  "robustness_share_by_alternative.png"
)

plot_bar(
  decision_summary$mcda_score,
  decision_summary$alternative,
  "MCDA Score by Alternative",
  "Weighted MCDA score",
  "mcda_score_by_alternative.png"
)

plot_bar(
  sensitivity_instability$ranking_instability_rate,
  sensitivity_instability$criterion,
  "Ranking Instability by Criterion",
  "Share of perturbations changing top rank",
  "ranking_instability_by_criterion.png"
)

print(decision_summary)
print(diagnostic_report)
print(sensitivity_instability)
