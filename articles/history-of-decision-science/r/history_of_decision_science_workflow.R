# history_of_decision_science_workflow.R
# Base R workflow for comparing historical decision paradigms.

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

payoff_table <- read.csv(file.path(article_root, "data", "synthetic_strategy_payoffs.csv"), stringsAsFactors = FALSE, check.names = FALSE)

validate_probabilities <- function(probabilities, label) {
  total <- sum(probabilities)
  if (abs(total - 1) > 1e-8) {
    stop(paste(label, "must sum to 1. Current sum:", total))
  }
}

validate_probabilities(payoff_table$objective_probability, "Objective probabilities")
validate_probabilities(payoff_table$subjective_probability, "Subjective probabilities")

strategies <- setdiff(names(payoff_table), c("scenario", "objective_probability", "subjective_probability"))

utility_function <- function(x, risk_aversion = 0.016) {
  1 - exp(-risk_aversion * x)
}

expected_value <- function(payoff, probability) {
  sum(payoff * probability)
}

expected_utility <- function(payoff, probability) {
  sum(utility_function(payoff) * probability)
}

robustness_share <- function(payoff, threshold = 40) {
  mean(payoff >= threshold)
}

long_rows <- data.frame()

for (strategy in strategies) {
  temp <- data.frame(
    scenario = payoff_table$scenario,
    objective_probability = payoff_table$objective_probability,
    subjective_probability = payoff_table$subjective_probability,
    strategy = strategy,
    payoff = payoff_table[[strategy]],
    stringsAsFactors = FALSE
  )
  long_rows <- rbind(long_rows, temp)
}

best_by_scenario <- apply(payoff_table[, strategies], 1, max)

regret_rows <- data.frame()

for (strategy in strategies) {
  temp <- data.frame(
    scenario = payoff_table$scenario,
    strategy = strategy,
    payoff = payoff_table[[strategy]],
    best_payoff = best_by_scenario,
    regret = best_by_scenario - payoff_table[[strategy]],
    stringsAsFactors = FALSE
  )
  regret_rows <- rbind(regret_rows, temp)
}

summary_rows <- data.frame()

for (strategy in strategies) {
  payoff <- payoff_table[[strategy]]
  strategy_regret <- regret_rows$regret[regret_rows$strategy == strategy]

  temp <- data.frame(
    strategy = strategy,
    expected_monetary_value = expected_value(payoff, payoff_table$objective_probability),
    expected_utility = expected_utility(payoff, payoff_table$objective_probability),
    subjective_expected_utility = expected_utility(payoff, payoff_table$subjective_probability),
    minimum_payoff = min(payoff),
    maximum_payoff = max(payoff),
    maximum_regret = max(strategy_regret),
    average_regret = mean(strategy_regret),
    robustness_share = robustness_share(payoff, threshold = 40),
    satisficing_share = robustness_share(payoff, threshold = 50),
    stringsAsFactors = FALSE
  )

  summary_rows <- rbind(summary_rows, temp)
}

summary_rows$emv_rank <- rank(-summary_rows$expected_monetary_value, ties.method = "min")
summary_rows$eu_rank <- rank(-summary_rows$expected_utility, ties.method = "min")
summary_rows$subjective_eu_rank <- rank(-summary_rows$subjective_expected_utility, ties.method = "min")
summary_rows$minimax_regret_rank <- rank(summary_rows$maximum_regret, ties.method = "min")
summary_rows$robustness_rank <- rank(-summary_rows$robustness_share, ties.method = "min")

summary_rows$historical_profile <- ifelse(
  summary_rows$emv_rank == 1,
  "classical expected-value candidate",
  ifelse(
    summary_rows$minimax_regret_rank == 1,
    "robust regret-minimization candidate",
    ifelse(
      summary_rows$robustness_rank == 1,
      "robust threshold candidate",
      ifelse(
        summary_rows$subjective_eu_rank == 1,
        "subjective expected-utility candidate",
        "comparison strategy"
      )
    )
  )
)

summary_rows <- summary_rows[order(summary_rows$robustness_rank, summary_rows$minimax_regret_rank, summary_rows$emv_rank), ]

write.csv(payoff_table, file.path(tables_dir, "historical_paradigm_payoff_table.csv"), row.names = FALSE)
write.csv(long_rows, file.path(tables_dir, "historical_paradigm_long_payoffs.csv"), row.names = FALSE)
write.csv(regret_rows, file.path(tables_dir, "historical_paradigm_regret_table.csv"), row.names = FALSE)
write.csv(summary_rows, file.path(tables_dir, "historical_paradigm_comparison.csv"), row.names = FALSE)

png(file.path(figures_dir, "expected_monetary_value_by_strategy.png"), width = 1200, height = 800)
barplot(summary_rows$expected_monetary_value, names.arg = summary_rows$strategy, las = 2, main = "Expected Monetary Value by Strategy", ylab = "Expected monetary value")
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
