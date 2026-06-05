# bayesian_decision_making_workflow.R
# Base R workflow for Bayesian updating, posterior expected utility,
# prior sensitivity, evidence strength, and action comparison.

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

cases <- read.csv(file.path(article_root, "data", "synthetic_bayesian_cases.csv"), stringsAsFactors = FALSE)
likelihoods <- read.csv(file.path(article_root, "data", "synthetic_likelihoods.csv"), stringsAsFactors = FALSE)

bayesian_update <- function(prior, sensitivity, false_positive_rate) {
  numerator <- sensitivity * prior
  denominator <- numerator + false_positive_rate * (1 - prior)
  numerator / denominator
}

posterior_expected_utility_action <- function(posterior, success_utility, false_positive_cost) {
  posterior * success_utility + (1 - posterior) * false_positive_cost
}

posterior_expected_utility_wait <- function(posterior, miss_cost, true_negative_utility) {
  posterior * miss_cost + (1 - posterior) * true_negative_utility
}

cases$posterior <- mapply(
  bayesian_update,
  cases$prior,
  cases$sensitivity,
  cases$false_positive_rate
)

cases$bayes_factor <- cases$sensitivity / cases$false_positive_rate
cases$posterior_odds <- cases$posterior / (1 - cases$posterior)

cases$action_utility <- mapply(
  posterior_expected_utility_action,
  cases$posterior,
  cases$action_success_utility,
  cases$action_false_positive_cost
)

cases$wait_utility <- mapply(
  posterior_expected_utility_wait,
  cases$posterior,
  cases$inaction_miss_cost,
  cases$inaction_true_negative_utility
)

cases$utility_difference <- cases$action_utility - cases$wait_utility

cases$recommended_action <- ifelse(
  cases$action_utility >= cases$wait_utility,
  "Act",
  "Wait or gather more evidence"
)

cases$posterior_review_flag <- ifelse(
  abs(cases$utility_difference) < 10,
  "decision-sensitive: review assumptions",
  "stable under baseline assumptions"
)

write.csv(cases, file.path(tables_dir, "bayesian_decision_profiles.csv"), row.names = FALSE)

prior_grid <- seq(0.01, 0.90, by = 0.01)
sensitivity_rows <- data.frame()

for (i in seq_len(nrow(cases))) {
  row <- cases[i, ]

  for (prior_value in prior_grid) {
    posterior <- bayesian_update(
      prior_value,
      row$sensitivity,
      row$false_positive_rate
    )

    action_utility <- posterior_expected_utility_action(
      posterior,
      row$action_success_utility,
      row$action_false_positive_cost
    )

    wait_utility <- posterior_expected_utility_wait(
      posterior,
      row$inaction_miss_cost,
      row$inaction_true_negative_utility
    )

    sensitivity_rows <- rbind(
      sensitivity_rows,
      data.frame(
        case = row$case,
        prior = prior_value,
        posterior = posterior,
        action_utility = action_utility,
        wait_utility = wait_utility,
        utility_difference = action_utility - wait_utility,
        recommended_action = ifelse(action_utility >= wait_utility, "Act", "Wait"),
        stringsAsFactors = FALSE
      )
    )
  }
}

write.csv(sensitivity_rows, file.path(tables_dir, "bayesian_prior_sensitivity.csv"), row.names = FALSE)

threshold_rows <- data.frame()

for (case_name in unique(sensitivity_rows$case)) {
  subset_rows <- sensitivity_rows[sensitivity_rows$case == case_name, ]
  act_rows <- subset_rows[subset_rows$recommended_action == "Act", ]

  threshold_prior <- if (nrow(act_rows) == 0) {
    NA
  } else {
    min(act_rows$prior)
  }

  threshold_rows <- rbind(
    threshold_rows,
    data.frame(
      case = case_name,
      minimum_prior_for_action = threshold_prior,
      stringsAsFactors = FALSE
    )
  )
}

write.csv(threshold_rows, file.path(tables_dir, "bayesian_action_thresholds.csv"), row.names = FALSE)

quality_map <- c(high = 1.0, medium = 0.65, low = 0.35)
likelihoods$evidence_quality_score <- quality_map[likelihoods$evidence_quality]
likelihoods$quality_flag <- ifelse(likelihoods$evidence_quality_score < 0.60, "review", "acceptable")

write.csv(likelihoods, file.path(tables_dir, "bayesian_evidence_quality_summary.csv"), row.names = FALSE)

evsi_rows <- data.frame()

for (i in seq_len(nrow(cases))) {
  row <- cases[i, ]

  prior_action_utility <- posterior_expected_utility_action(
    row$prior,
    row$action_success_utility,
    row$action_false_positive_cost
  )

  prior_wait_utility <- posterior_expected_utility_wait(
    row$prior,
    row$inaction_miss_cost,
    row$inaction_true_negative_utility
  )

  baseline_best <- max(prior_action_utility, prior_wait_utility)

  posterior_positive <- bayesian_update(row$prior, row$sensitivity, row$false_positive_rate)
  likelihood_negative_h <- 1 - row$sensitivity
  likelihood_negative_not_h <- 1 - row$false_positive_rate
  posterior_negative <- (likelihood_negative_h * row$prior) / (
    likelihood_negative_h * row$prior + likelihood_negative_not_h * (1 - row$prior)
  )

  p_positive <- row$sensitivity * row$prior + row$false_positive_rate * (1 - row$prior)
  p_negative <- 1 - p_positive

  best_positive <- max(
    posterior_expected_utility_action(posterior_positive, row$action_success_utility, row$action_false_positive_cost),
    posterior_expected_utility_wait(posterior_positive, row$inaction_miss_cost, row$inaction_true_negative_utility)
  )

  best_negative <- max(
    posterior_expected_utility_action(posterior_negative, row$action_success_utility, row$action_false_positive_cost),
    posterior_expected_utility_wait(posterior_negative, row$inaction_miss_cost, row$inaction_true_negative_utility)
  )

  expected_utility_with_signal <- p_positive * best_positive + p_negative * best_negative

  evsi_rows <- rbind(
    evsi_rows,
    data.frame(
      case = row$case,
      baseline_best_utility = baseline_best,
      expected_utility_with_signal = expected_utility_with_signal,
      expected_value_of_sample_information_proxy = expected_utility_with_signal - baseline_best,
      stringsAsFactors = FALSE
    )
  )
}

write.csv(evsi_rows, file.path(tables_dir, "bayesian_value_of_information_proxy.csv"), row.names = FALSE)

png(file.path(figures_dir, "posterior_by_case.png"), width = 1200, height = 800)
barplot(
  cases$posterior,
  names.arg = cases$case,
  las = 2,
  main = "Posterior Probability by Case",
  ylab = "Posterior probability"
)
grid()
dev.off()

png(file.path(figures_dir, "posterior_utility_difference.png"), width = 1200, height = 800)
barplot(
  cases$utility_difference,
  names.arg = cases$case,
  las = 2,
  main = "Posterior Utility Difference: Act vs Wait",
  ylab = "Utility difference"
)
abline(h = 0, lty = 2)
grid()
dev.off()

png(file.path(figures_dir, "prior_sensitivity_selected_case.png"), width = 1200, height = 800)
selected_case <- sensitivity_rows[sensitivity_rows$case == "Model Drift Case", ]
plot(
  selected_case$prior,
  selected_case$posterior,
  type = "l",
  xlab = "Prior probability",
  ylab = "Posterior probability",
  main = "Prior Sensitivity: Model Drift Case"
)
grid()
dev.off()

print(cases)
print(threshold_rows)
print(evsi_rows)
