# value_of_information_when_to_wait_workflow.R
# Base R workflow for value of information and decision timing:
# EVPI, EVSI-style sample information, net value of information,
# delay cost, decision-change probability, and timing recommendations.

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

actions <- read.csv(file.path(article_root, "data", "synthetic_payoff_matrix.csv"), stringsAsFactors = FALSE)
states_data <- read.csv(file.path(article_root, "data", "synthetic_prior_probabilities.csv"), stringsAsFactors = FALSE)
posterior_data <- read.csv(file.path(article_root, "data", "synthetic_evidence_posteriors.csv"), stringsAsFactors = FALSE)
costs_data <- read.csv(file.path(article_root, "data", "synthetic_information_costs.csv"), stringsAsFactors = FALSE)

states <- states_data$state
prior_probabilities <- setNames(states_data$probability, states_data$state)
costs <- setNames(costs_data$value, costs_data$cost_name)

if (abs(sum(prior_probabilities) - 1) > 1e-9) {
  stop("Prior probabilities must sum to 1.")
}

payoff_matrix <- as.matrix(actions[, states])
current_expected_values <- as.vector(payoff_matrix %*% prior_probabilities[states])
current_best_index <- which.max(current_expected_values)
current_best_action <- actions$action[current_best_index]
current_expected_value <- max(current_expected_values)

perfect_information_value <- sum(prior_probabilities[states] * apply(payoff_matrix, 2, max))
evpi <- perfect_information_value - current_expected_value

evidence_outcomes <- unique(posterior_data$evidence)
evidence_probabilities <- tapply(posterior_data$evidence_probability, posterior_data$evidence, unique)
evidence_probabilities <- as.numeric(evidence_probabilities)
names(evidence_probabilities) <- evidence_outcomes

if (abs(sum(evidence_probabilities) - 1) > 1e-9) {
  stop("Evidence probabilities must sum to 1.")
}

sample_rows <- list()

for (signal in evidence_outcomes) {
  subset <- posterior_data[posterior_data$evidence == signal, ]
  posterior <- setNames(subset$posterior_probability, subset$state)

  if (abs(sum(posterior) - 1) > 1e-9) {
    stop(paste("Posterior probabilities must sum to 1 for signal:", signal))
  }

  posterior_expected_values <- as.vector(payoff_matrix %*% posterior[states])
  best_index <- which.max(posterior_expected_values)

  sample_rows[[signal]] <- data.frame(
    evidence = signal,
    evidence_probability = unique(subset$evidence_probability),
    best_action_after_evidence = actions$action[best_index],
    expected_value_after_evidence = max(posterior_expected_values),
    decision_changes = actions$action[best_index] != current_best_action,
    stringsAsFactors = FALSE
  )
}

sample_results <- do.call(rbind, sample_rows)

ev_sample <- sum(
  sample_results$evidence_probability *
    sample_results$expected_value_after_evidence
)

evsi <- ev_sample - current_expected_value
information_cost <- costs["information_cost"]
delay_cost <- costs["delay_cost"]
net_value_information <- evsi - information_cost
net_value_waiting <- evsi - information_cost - delay_cost
decision_change_probability <- sum(sample_results$evidence_probability * as.numeric(sample_results$decision_changes))

recommendation <- ifelse(
  net_value_waiting > 0,
  "wait_for_information",
  ifelse(net_value_information > 0 & delay_cost > evsi * 0.5, "learn_while_acting", "act_now_or_stage")
)

summary <- data.frame(
  metric = c(
    "current_best_action",
    "current_expected_value",
    "expected_value_with_perfect_information",
    "expected_value_of_perfect_information",
    "expected_value_with_sample_information",
    "expected_value_of_sample_information",
    "information_cost",
    "delay_cost",
    "net_value_of_information",
    "net_value_of_waiting",
    "decision_change_probability",
    "recommendation"
  ),
  value = c(
    current_best_action,
    round(current_expected_value, 4),
    round(perfect_information_value, 4),
    round(evpi, 4),
    round(ev_sample, 4),
    round(evsi, 4),
    round(information_cost, 4),
    round(delay_cost, 4),
    round(net_value_information, 4),
    round(net_value_waiting, 4),
    round(decision_change_probability, 4),
    recommendation
  ),
  stringsAsFactors = FALSE
)

timing_recommendation <- data.frame(
  current_best_action = current_best_action,
  evpi = evpi,
  evsi = evsi,
  information_cost = information_cost,
  delay_cost = delay_cost,
  net_value_information = net_value_information,
  net_value_waiting = net_value_waiting,
  decision_change_probability = decision_change_probability,
  recommendation = recommendation,
  stringsAsFactors = FALSE
)

current_ev_table <- data.frame(
  action = actions$action,
  current_expected_value = current_expected_values,
  stringsAsFactors = FALSE
)

write.csv(
  actions,
  file.path(tables_dir, "voi_payoff_matrix.csv"),
  row.names = FALSE
)

write.csv(
  states_data,
  file.path(tables_dir, "voi_prior_probabilities.csv"),
  row.names = FALSE
)

write.csv(
  posterior_data,
  file.path(tables_dir, "voi_posterior_probabilities_by_evidence.csv"),
  row.names = FALSE
)

write.csv(
  current_ev_table,
  file.path(tables_dir, "voi_current_expected_values.csv"),
  row.names = FALSE
)

write.csv(
  sample_results,
  file.path(tables_dir, "voi_sample_information_results.csv"),
  row.names = FALSE
)

write.csv(
  summary,
  file.path(tables_dir, "voi_summary_metrics.csv"),
  row.names = FALSE
)

write.csv(
  timing_recommendation,
  file.path(tables_dir, "voi_timing_recommendation.csv"),
  row.names = FALSE
)

png(file.path(figures_dir, "voi_expected_values_by_action.png"), width = 1200, height = 800)
barplot(
  current_expected_values,
  names.arg = actions$action,
  las = 2,
  main = "Current Expected Value by Action",
  ylab = "Expected value"
)
grid()
dev.off()

png(file.path(figures_dir, "voi_information_value_comparison.png"), width = 1200, height = 800)
barplot(
  c(evpi, evsi, net_value_information, net_value_waiting),
  names.arg = c("EVPI", "EVSI", "Net Info", "Net Waiting"),
  las = 2,
  main = "Information Value and Timing Comparison",
  ylab = "Value"
)
abline(h = 0)
grid()
dev.off()

print(summary)
print(sample_results)
print(timing_recommendation)
