# decision_science_vs_decision_theory_workflow.R
# Base R workflow for comparing decision-theoretic and decision-science criteria.

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
strategies <- setdiff(names(scenario_table), c("scenario", "probability"))

validate_probabilities <- function(probabilities) {
  total <- sum(probabilities)
  if (abs(total - 1) > 1e-8) {
    stop(paste("Scenario probabilities must sum to 1. Current sum:", total))
  }
}

utility_function <- function(x, risk_aversion = 0.018) {
  1 - exp(-risk_aversion * x)
}

expected_value <- function(payoff, probability) {
  sum(payoff * probability)
}

expected_utility <- function(payoff, probability) {
  sum(utility_function(payoff) * probability)
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

  temp <- data.frame(
    strategy = strategy,
    expected_value = expected_value(payoff, scenario_table$probability),
    expected_utility = expected_utility(payoff, scenario_table$probability),
    minimum_payoff = min(payoff),
    maximum_payoff = max(payoff),
    payoff_range = max(payoff) - min(payoff),
    max_regret = max(strategy_regret),
    mean_regret = mean(strategy_regret),
    robustness_share = robustness_share(payoff, threshold = 45),
    stringsAsFactors = FALSE
  )

  summary_rows <- rbind(summary_rows, temp)
}

summary_rows$ev_rank <- rank(-summary_rows$expected_value, ties.method = "min")
summary_rows$eu_rank <- rank(-summary_rows$expected_utility, ties.method = "min")
summary_rows$maximin_rank <- rank(-summary_rows$minimum_payoff, ties.method = "min")
summary_rows$minimax_regret_rank <- rank(summary_rows$max_regret, ties.method = "min")
summary_rows$robustness_rank <- rank(-summary_rows$robustness_share, ties.method = "min")

summary_rows$decision_profile <- ifelse(
  summary_rows$ev_rank == 1 & summary_rows$minimax_regret_rank > 2,
  "high expected value but regret-sensitive",
  ifelse(
    summary_rows$robustness_rank == 1 & summary_rows$minimum_payoff >= 40,
    "robust applied decision-science candidate",
    ifelse(
      summary_rows$maximin_rank == 1,
      "strong downside-protection candidate",
      "comparison strategy"
    )
  )
)

summary_rows <- summary_rows[order(summary_rows$robustness_rank, summary_rows$minimax_regret_rank, summary_rows$ev_rank), ]

shock_values <- seq(0.05, 0.40, by = 0.05)
sensitivity_rows <- data.frame()

for (shock_probability in shock_values) {
  revised <- scenario_table
  shock_index <- which(revised$scenario == "System shock")
  non_shock_index <- setdiff(seq_len(nrow(revised)), shock_index)

  remaining_total <- 1 - shock_probability
  original_non_shock_sum <- sum(revised$probability[non_shock_index])

  revised$probability[shock_index] <- shock_probability
  revised$probability[non_shock_index] <- revised$probability[non_shock_index] / original_non_shock_sum * remaining_total

  validate_probabilities(revised$probability)

  ev_scores <- sapply(strategies, function(strategy) {
    expected_value(revised[[strategy]], revised$probability)
  })

  best_strategy <- names(ev_scores)[which.max(ev_scores)]

  temp <- data.frame(
    shock_probability = shock_probability,
    top_expected_value_strategy = best_strategy,
    top_expected_value = max(ev_scores),
    stringsAsFactors = FALSE
  )

  for (strategy in strategies) {
    temp[[paste0(strategy, "_expected_value")]] <- ev_scores[[strategy]]
  }

  sensitivity_rows <- rbind(sensitivity_rows, temp)
}

write.csv(scenario_table, file.path(tables_dir, "scenario_payoff_table.csv"), row.names = FALSE)
write.csv(long_rows, file.path(tables_dir, "long_strategy_payoff_table.csv"), row.names = FALSE)
write.csv(regret_rows, file.path(tables_dir, "regret_profile_table.csv"), row.names = FALSE)
write.csv(summary_rows, file.path(tables_dir, "decision_criteria_comparison.csv"), row.names = FALSE)
write.csv(sensitivity_rows, file.path(tables_dir, "probability_sensitivity_diagnostics.csv"), row.names = FALSE)

png(file.path(figures_dir, "expected_value_by_strategy.png"), width = 1200, height = 800)
barplot(summary_rows$expected_value, names.arg = summary_rows$strategy, las = 2, main = "Expected Value by Strategy", ylab = "Expected value")
grid()
dev.off()

png(file.path(figures_dir, "maximum_regret_by_strategy.png"), width = 1200, height = 800)
barplot(summary_rows$max_regret, names.arg = summary_rows$strategy, las = 2, main = "Maximum Regret by Strategy", ylab = "Maximum regret")
grid()
dev.off()

png(file.path(figures_dir, "robustness_share_by_strategy.png"), width = 1200, height = 800)
barplot(summary_rows$robustness_share, names.arg = summary_rows$strategy, las = 2, main = "Robustness Share by Strategy", ylab = "Share of scenarios meeting threshold")
grid()
dev.off()

print(summary_rows)
print(sensitivity_rows)
