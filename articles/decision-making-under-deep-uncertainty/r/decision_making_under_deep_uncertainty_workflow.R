# decision_making_under_deep_uncertainty_workflow.R
# Base R workflow for decision-making under deep uncertainty:
# ambiguity profiles, expected value, worst-case performance, regret,
# threshold compliance, vulnerability analysis, adaptive simulation,
# and review tables.

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

set.seed(42)

strategies <- read.csv(file.path(article_root, "data", "synthetic_strategies.csv"), stringsAsFactors = FALSE)
scenarios_data <- read.csv(file.path(article_root, "data", "synthetic_scenarios.csv"), stringsAsFactors = FALSE)
performance <- read.csv(file.path(article_root, "data", "synthetic_performance_matrix.csv"), stringsAsFactors = FALSE)
profiles_data <- read.csv(file.path(article_root, "data", "synthetic_ambiguity_profiles.csv"), stringsAsFactors = FALSE)
thresholds_data <- read.csv(file.path(article_root, "data", "synthetic_thresholds.csv"), stringsAsFactors = FALSE)

scenarios <- scenarios_data$scenario
thresholds <- setNames(thresholds_data$value, thresholds_data$threshold_name)

performance_threshold <- thresholds["minimum_acceptable_performance"]
high_regret_threshold <- thresholds["high_regret_threshold"]
low_worst_case_threshold <- thresholds["low_worst_case_threshold"]
low_pass_rate_threshold <- thresholds["low_pass_rate_threshold"]

performance_matrix <- as.matrix(performance[, scenarios])
scenario_maxima <- apply(performance_matrix, 2, max)
regret_matrix <- matrix(0, nrow = nrow(performance_matrix), ncol = length(scenarios))
colnames(regret_matrix) <- scenarios

for (j in seq_along(scenarios)) {
  regret_matrix[, j] <- scenario_maxima[j] - performance_matrix[, j]
}

profile_names <- unique(profiles_data$profile)
profile_results <- list()

for (p in seq_along(profile_names)) {
  profile_name <- profile_names[p]
  profile_subset <- profiles_data[profiles_data$profile == profile_name, ]
  weights <- setNames(profile_subset$weight, profile_subset$scenario)

  if (abs(sum(weights) - 1) > 1e-6) {
    stop(paste("Weights must sum to 1 for profile:", profile_name))
  }

  expected_value <- as.vector(performance_matrix %*% weights[scenarios])
  worst_case <- apply(performance_matrix, 1, min)
  best_case <- apply(performance_matrix, 1, max)
  performance_range <- best_case - worst_case
  average_regret <- rowMeans(regret_matrix)
  max_regret <- apply(regret_matrix, 1, max)
  threshold_pass_rate <- rowMeans(performance_matrix >= performance_threshold)
  vulnerability_count <- rowSums(performance_matrix < performance_threshold)

  robustness_score <- (
    0.28 * worst_case +
      0.24 * threshold_pass_rate +
      0.20 * (1 - max_regret) +
      0.18 * expected_value +
      0.10 * (1 - performance_range)
  )

  temp <- data.frame(
    profile = profile_name,
    strategy = performance$strategy,
    expected_value = expected_value,
    worst_case = worst_case,
    best_case = best_case,
    performance_range = performance_range,
    average_regret = average_regret,
    max_regret = max_regret,
    threshold_pass_rate = threshold_pass_rate,
    vulnerability_count = vulnerability_count,
    robustness_score = robustness_score,
    stringsAsFactors = FALSE
  )

  temp$rank <- rank(-temp$robustness_score, ties.method = "min")
  temp$review_flag <- ifelse(
    temp$worst_case < low_worst_case_threshold |
      temp$max_regret > high_regret_threshold |
      temp$threshold_pass_rate < low_pass_rate_threshold,
    "review",
    "acceptable"
  )

  profile_results[[p]] <- temp[order(temp$rank), ]
}

results <- do.call(rbind, profile_results)
results <- results[order(results$profile, results$rank), ]

write.csv(
  performance,
  file.path(tables_dir, "dmdu_strategy_performance_matrix.csv"),
  row.names = FALSE
)

write.csv(
  profiles_data,
  file.path(tables_dir, "dmdu_ambiguity_profiles.csv"),
  row.names = FALSE
)

write.csv(
  results,
  file.path(tables_dir, "dmdu_robustness_results_by_profile.csv"),
  row.names = FALSE
)

regret_table <- data.frame(
  strategy = performance$strategy,
  regret_matrix,
  check.names = FALSE,
  stringsAsFactors = FALSE
)

write.csv(
  regret_table,
  file.path(tables_dir, "dmdu_regret_matrix.csv"),
  row.names = FALSE
)

vulnerability_table <- data.frame(
  strategy = performance$strategy,
  performance_matrix < performance_threshold,
  check.names = FALSE,
  stringsAsFactors = FALSE
)

write.csv(
  vulnerability_table,
  file.path(tables_dir, "dmdu_vulnerability_table.csv"),
  row.names = FALSE
)

scenario_summary <- data.frame(
  scenario = scenarios,
  best_strategy = performance$strategy[apply(performance_matrix, 2, which.max)],
  max_performance = apply(performance_matrix, 2, max),
  min_performance = apply(performance_matrix, 2, min),
  scenario_spread = apply(performance_matrix, 2, max) - apply(performance_matrix, 2, min),
  stringsAsFactors = FALSE
)

write.csv(
  scenario_summary,
  file.path(tables_dir, "dmdu_scenario_summary.csv"),
  row.names = FALSE
)

review_summary <- as.data.frame(table(results$profile, results$review_flag), stringsAsFactors = FALSE)
names(review_summary) <- c("profile", "review_flag", "n_strategies")

write.csv(
  review_summary,
  file.path(tables_dir, "dmdu_review_summary.csv"),
  row.names = FALSE
)

# Adaptive simulation under structural uncertainty.
simulation_records <- list()
summary_records <- list()
record_counter <- 1

for (i in seq_len(nrow(strategies))) {
  value <- 100
  values <- numeric(40)
  growth_rates <- numeric(40)

  for (t in seq_len(40)) {
    regime_shift <- sample(
      c(-2.5, -1.0, 0.0, 1.0, 2.0),
      size = 1,
      prob = c(0.10, 0.20, 0.30, 0.25, 0.15)
    )

    structural_shock <- rnorm(1, mean = 0, sd = strategies$volatility[i])
    adaptive_buffer <- strategies$adaptability[i] * runif(1, 0.4, 1.4)
    resilience_buffer <- strategies$resilience[i] * runif(1, 0.3, 1.0)

    growth <- strategies$base_return[i] + regime_shift + structural_shock + adaptive_buffer + resilience_buffer
    value <- max(20, value * (1 + growth / 100))

    values[t] <- value
    growth_rates[t] <- growth

    simulation_records[[record_counter]] <- data.frame(
      strategy = strategies$strategy[i],
      time = t,
      strategy_value_index = value,
      growth_rate = growth,
      regime_shift = regime_shift,
      structural_shock = structural_shock,
      stringsAsFactors = FALSE
    )
    record_counter <- record_counter + 1
  }

  summary_records[[i]] <- data.frame(
    strategy = strategies$strategy[i],
    final_value = values[length(values)],
    min_value = min(values),
    max_value = max(values),
    average_value = mean(values),
    value_volatility = sd(values),
    average_growth_rate = mean(growth_rates),
    worst_growth_rate = min(growth_rates),
    stringsAsFactors = FALSE
  )
}

simulation_table <- do.call(rbind, simulation_records)
simulation_summary <- do.call(rbind, summary_records)
simulation_summary <- simulation_summary[order(-simulation_summary$final_value), ]

write.csv(
  simulation_table,
  file.path(tables_dir, "dmdu_adaptive_strategy_simulation.csv"),
  row.names = FALSE
)

write.csv(
  simulation_summary,
  file.path(tables_dir, "dmdu_adaptive_strategy_summary.csv"),
  row.names = FALSE
)

png(file.path(figures_dir, "dmdu_robustness_scores_equal_profile.png"), width = 1200, height = 800)
equal_results <- results[results$profile == "equal", ]
barplot(
  equal_results$robustness_score,
  names.arg = equal_results$strategy,
  las = 2,
  main = "Robustness Scores Under Equal Ambiguity Profile",
  ylab = "Robustness score"
)
grid()
dev.off()

png(file.path(figures_dir, "dmdu_worst_case_performance.png"), width = 1200, height = 800)
barplot(
  equal_results$worst_case,
  names.arg = equal_results$strategy,
  las = 2,
  main = "Worst-Case Strategy Performance",
  ylab = "Worst-case performance"
)
grid()
dev.off()

png(file.path(figures_dir, "dmdu_max_regret.png"), width = 1200, height = 800)
barplot(
  equal_results$max_regret,
  names.arg = equal_results$strategy,
  las = 2,
  main = "Maximum Regret by Strategy",
  ylab = "Maximum regret"
)
grid()
dev.off()

print(results)
print(scenario_summary)
print(review_summary)
print(simulation_summary)
