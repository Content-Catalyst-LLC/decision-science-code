# why_uncertainty_changes_decision_making_workflow.R
# Base R workflow for decision-making under uncertainty.

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

scenario_table <- read.csv(file.path(article_root, "data", "synthetic_payoff_matrix.csv"), stringsAsFactors = FALSE, check.names = FALSE)
ambiguity_exposure <- read.csv(file.path(article_root, "data", "synthetic_ambiguity_parameters.csv"), stringsAsFactors = FALSE)

strategies <- setdiff(names(scenario_table), c("scenario", "probability"))

validate_probabilities <- function(probabilities) {
  total <- sum(probabilities)
  if (abs(total - 1) > 1e-8) {
    stop(paste("Scenario probabilities must sum to 1. Current sum:", total))
  }
}

utility_function <- function(x, risk_aversion = 0.016) {
  1 - exp(-risk_aversion * x)
}

expected_utility <- function(payoff, probability) {
  sum(utility_function(payoff) * probability)
}

expected_value <- function(payoff, probability) {
  sum(payoff * probability)
}

robustness_share <- function(payoff, threshold = 45) {
  mean(payoff >= threshold)
}

validate_probabilities(scenario_table$probability)

long_rows <- data.frame()

for (strategy in strategies) {
  temp <- data.frame(
    scenario = scenario_table$scenario,
    probability = scenario_table$probability,
    strategy = strategy,
    payoff = scenario_table[[strategy]],
    stringsAsFactors = FALSE
  )
  long_rows <- rbind(long_rows, temp)
}

best_by_scenario <- apply(scenario_table[, strategies], 1, max)

regret_rows <- data.frame()

for (strategy in strategies) {
  temp <- data.frame(
    scenario = scenario_table$scenario,
    probability = scenario_table$probability,
    strategy = strategy,
    payoff = scenario_table[[strategy]],
    best_payoff = best_by_scenario,
    regret = best_by_scenario - scenario_table[[strategy]],
    stringsAsFactors = FALSE
  )
  regret_rows <- rbind(regret_rows, temp)
}

summary_rows <- data.frame()

for (strategy in strategies) {
  payoff <- scenario_table[[strategy]]
  strategy_regret <- regret_rows$regret[regret_rows$strategy == strategy]
  ambiguity <- ambiguity_exposure$ambiguity[ambiguity_exposure$strategy == strategy]
  reversibility <- ambiguity_exposure$reversibility[ambiguity_exposure$strategy == strategy]
  implementation_capacity <- ambiguity_exposure$implementation_capacity[ambiguity_exposure$strategy == strategy]
  evidence_quality <- ambiguity_exposure$evidence_quality[ambiguity_exposure$strategy == strategy]

  temp <- data.frame(
    strategy = strategy,
    expected_value = expected_value(payoff, scenario_table$probability),
    expected_utility = expected_utility(payoff, scenario_table$probability),
    ambiguity_exposure = ambiguity,
    ambiguity_adjusted_utility = expected_utility(payoff, scenario_table$probability) - 1.5 * ambiguity,
    minimum_payoff = min(payoff),
    maximum_payoff = max(payoff),
    payoff_range = max(payoff) - min(payoff),
    maximum_regret = max(strategy_regret),
    mean_regret = mean(strategy_regret),
    robustness_share = robustness_share(payoff, threshold = 45),
    reversibility = reversibility,
    implementation_capacity = implementation_capacity,
    evidence_quality = evidence_quality,
    stringsAsFactors = FALSE
  )

  summary_rows <- rbind(summary_rows, temp)
}

summary_rows$expected_value_rank <- rank(-summary_rows$expected_value, ties.method = "min")
summary_rows$ambiguity_adjusted_rank <- rank(-summary_rows$ambiguity_adjusted_utility, ties.method = "min")
summary_rows$minimax_regret_rank <- rank(summary_rows$maximum_regret, ties.method = "min")
summary_rows$robustness_rank <- rank(-summary_rows$robustness_share, ties.method = "min")

summary_rows$decision_profile <- ifelse(
  summary_rows$expected_value_rank == 1 & summary_rows$maximum_regret > median(summary_rows$maximum_regret),
  "high expected value but regret-sensitive",
  ifelse(
    summary_rows$robustness_rank == 1 & summary_rows$reversibility >= 0.75,
    "robust and option-preserving",
    ifelse(
      summary_rows$ambiguity_adjusted_rank == 1,
      "strong ambiguity-adjusted candidate",
      "comparison strategy"
    )
  )
)

summary_rows <- summary_rows[order(
  summary_rows$robustness_rank,
  summary_rows$minimax_regret_rank,
  summary_rows$ambiguity_adjusted_rank
), ]

ambiguity_lambda_values <- seq(0, 3, by = 0.25)
sensitivity_rows <- data.frame()

for (lambda in ambiguity_lambda_values) {
  temp_scores <- data.frame()

  for (strategy in strategies) {
    payoff <- scenario_table[[strategy]]
    ambiguity <- ambiguity_exposure$ambiguity[ambiguity_exposure$strategy == strategy]
    score <- expected_utility(payoff, scenario_table$probability) - lambda * ambiguity

    temp_scores <- rbind(
      temp_scores,
      data.frame(
        ambiguity_lambda = lambda,
        strategy = strategy,
        ambiguity_adjusted_score = score,
        stringsAsFactors = FALSE
      )
    )
  }

  top_strategy <- temp_scores$strategy[which.max(temp_scores$ambiguity_adjusted_score)]
  temp_scores$top_strategy_at_lambda <- top_strategy
  sensitivity_rows <- rbind(sensitivity_rows, temp_scores)
}

write.csv(scenario_table, file.path(tables_dir, "uncertainty_scenario_payoff_table.csv"), row.names = FALSE)
write.csv(long_rows, file.path(tables_dir, "uncertainty_long_payoff_table.csv"), row.names = FALSE)
write.csv(regret_rows, file.path(tables_dir, "uncertainty_regret_table.csv"), row.names = FALSE)
write.csv(summary_rows, file.path(tables_dir, "uncertainty_decision_summary.csv"), row.names = FALSE)
write.csv(sensitivity_rows, file.path(tables_dir, "ambiguity_sensitivity_diagnostics.csv"), row.names = FALSE)

png(file.path(figures_dir, "expected_value_by_strategy.png"), width = 1200, height = 800)
barplot(summary_rows$expected_value, names.arg = summary_rows$strategy, las = 2, main = "Expected Value by Strategy", ylab = "Expected value")
grid()
dev.off()

png(file.path(figures_dir, "maximum_regret_by_strategy.png"), width = 1200, height = 800)
barplot(summary_rows$maximum_regret, names.arg = summary_rows$strategy, las = 2, main = "Maximum Regret by Strategy", ylab = "Maximum regret")
grid()
dev.off()

png(file.path(figures_dir, "robustness_share_by_strategy.png"), width = 1200, height = 800)
barplot(summary_rows$robustness_share, names.arg = summary_rows$strategy, las = 2, main = "Robustness Share by Strategy", ylab = "Share of scenarios meeting threshold")
grid()
dev.off()

print(summary_rows)
print(head(sensitivity_rows, 12))
