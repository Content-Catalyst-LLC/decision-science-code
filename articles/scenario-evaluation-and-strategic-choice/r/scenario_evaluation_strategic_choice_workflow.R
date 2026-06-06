# scenario_evaluation_strategic_choice_workflow.R
# Base R workflow for scenario evaluation and strategic choice:
# expected performance, worst-case performance, regret,
# dispersion, threshold pass rate, and robustness ranking.

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

strategy_info <- read.csv(file.path(article_root, "data", "synthetic_strategies.csv"), stringsAsFactors = FALSE)
scenarios <- read.csv(file.path(article_root, "data", "synthetic_scenarios.csv"), stringsAsFactors = FALSE)
performance <- read.csv(file.path(article_root, "data", "synthetic_scenario_performance.csv"), stringsAsFactors = FALSE)

scenario_names <- scenarios$scenario
scenario_probs <- scenarios$probability
names(scenario_probs) <- scenario_names

strategies <- unique(performance$strategy)

performance_matrix <- matrix(
  NA_real_,
  nrow = length(strategies),
  ncol = length(scenario_names),
  dimnames = list(strategies, scenario_names)
)

for (i in seq_len(nrow(performance))) {
  performance_matrix[performance$strategy[i], performance$scenario[i]] <- performance$performance[i]
}

scenario_best <- apply(performance_matrix, 2, max)
regret_matrix <- sweep(performance_matrix, 2, scenario_best, FUN = function(value, best) best - value)

threshold <- 0.70

results <- data.frame(
  strategy = rownames(performance_matrix),
  expected_value = as.vector(performance_matrix %*% scenario_probs),
  worst_case = apply(performance_matrix, 1, min),
  average_performance = apply(performance_matrix, 1, mean),
  scenario_dispersion = apply(performance_matrix, 1, sd),
  maximum_regret = apply(regret_matrix, 1, max),
  threshold_pass_rate = apply(performance_matrix, 1, function(x) mean(x >= threshold)),
  stringsAsFactors = FALSE
)

results$scenario_robustness_score <- (
  0.26 * results$expected_value +
    0.24 * results$worst_case +
    0.20 * results$threshold_pass_rate -
    0.16 * results$maximum_regret -
    0.14 * results$scenario_dispersion
)

results$review_flag <- ifelse(
  results$worst_case < 0.55 |
    results$threshold_pass_rate < 0.60 |
    results$maximum_regret > 0.35,
  "review",
  "acceptable"
)

results$rank <- rank(-results$scenario_robustness_score, ties.method = "min")
results <- results[order(results$rank), ]

scenario_long <- data.frame(
  strategy = rep(rownames(performance_matrix), each = length(scenario_names)),
  scenario = rep(scenario_names, times = nrow(performance_matrix)),
  performance = as.vector(t(performance_matrix)),
  stringsAsFactors = FALSE
)

regret_long <- data.frame(
  strategy = rep(rownames(regret_matrix), each = length(scenario_names)),
  scenario = rep(scenario_names, times = nrow(regret_matrix)),
  regret = as.vector(t(regret_matrix)),
  stringsAsFactors = FALSE
)

write.csv(
  strategy_info,
  file.path(tables_dir, "scenario_strategy_profiles.csv"),
  row.names = FALSE
)

write.csv(
  scenario_long,
  file.path(tables_dir, "scenario_strategy_performance_long.csv"),
  row.names = FALSE
)

write.csv(
  regret_long,
  file.path(tables_dir, "scenario_regret_table.csv"),
  row.names = FALSE
)

write.csv(
  results,
  file.path(tables_dir, "scenario_evaluation_results.csv"),
  row.names = FALSE
)

png(file.path(figures_dir, "scenario_robustness_scores.png"), width = 1200, height = 800)
barplot(
  results$scenario_robustness_score,
  names.arg = results$strategy,
  las = 2,
  main = "Scenario Robustness Score by Strategy",
  ylab = "Robustness score"
)
grid()
dev.off()

png(file.path(figures_dir, "scenario_worst_case_performance.png"), width = 1200, height = 800)
barplot(
  results$worst_case,
  names.arg = results$strategy,
  las = 2,
  main = "Worst-Case Scenario Performance",
  ylab = "Worst-case performance"
)
grid()
dev.off()

print(results)
