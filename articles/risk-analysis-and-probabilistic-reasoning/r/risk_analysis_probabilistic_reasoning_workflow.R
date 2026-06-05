# risk_analysis_probabilistic_reasoning_workflow.R
# Base R workflow for expected loss, volatility, tail exposure,
# threshold breach, scenario stress, and risk-profile comparison.

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

strategies <- read.csv(file.path(article_root, "data", "synthetic_risk_strategies.csv"), stringsAsFactors = FALSE)
stress_scenarios <- read.csv(file.path(article_root, "data", "synthetic_stress_scenarios.csv"), stringsAsFactors = FALSE)
probability_estimates <- read.csv(file.path(article_root, "data", "synthetic_probability_estimates.csv"), stringsAsFactors = FALSE)
consequences <- read.csv(file.path(article_root, "data", "synthetic_consequences.csv"), stringsAsFactors = FALSE)

n_trials <- 10000
risk_threshold <- -0.10
alpha <- 0.05

simulation_rows <- data.frame()

for (i in seq_len(nrow(strategies))) {
  s <- strategies[i, ]

  ordinary_returns <- rnorm(n_trials, mean = s$mean_return, sd = s$volatility)
  shocks <- ifelse(runif(n_trials) < s$shock_probability, s$shock_size, 0)
  simulated_return <- ordinary_returns + shocks + s$recovery_credit

  simulation_rows <- rbind(
    simulation_rows,
    data.frame(
      strategy = s$strategy,
      simulated_return = simulated_return,
      loss = pmax(0, -simulated_return),
      threshold_breach = simulated_return <= risk_threshold,
      stringsAsFactors = FALSE
    )
  )
}

risk_summary <- do.call(
  rbind,
  lapply(
    split(simulation_rows, simulation_rows$strategy),
    function(x) {
      sorted_returns <- sort(x$simulated_return)
      var_alpha <- quantile(x$simulated_return, probs = alpha, names = FALSE)
      cvar_alpha <- mean(x$simulated_return[x$simulated_return <= var_alpha])

      data.frame(
        strategy = unique(x$strategy),
        mean_return = mean(x$simulated_return),
        expected_loss = mean(x$loss),
        volatility = sd(x$simulated_return),
        downside_breach_probability = mean(x$threshold_breach),
        value_at_risk_5pct = var_alpha,
        conditional_value_at_risk_5pct = cvar_alpha,
        minimum_return = min(x$simulated_return),
        maximum_return = max(x$simulated_return),
        stringsAsFactors = FALSE
      )
    }
  )
)

risk_summary$risk_penalty_score <- (
  risk_summary$expected_loss * 0.35 +
  risk_summary$volatility * 0.20 +
  abs(risk_summary$conditional_value_at_risk_5pct) * 0.30 +
  risk_summary$downside_breach_probability * 0.15
)

risk_summary$risk_adjusted_score <- risk_summary$mean_return - risk_summary$risk_penalty_score
risk_summary <- risk_summary[order(-risk_summary$risk_adjusted_score), ]

write.csv(simulation_rows, file.path(tables_dir, "risk_simulation_trials.csv"), row.names = FALSE)
write.csv(risk_summary, file.path(tables_dir, "risk_profile_summary.csv"), row.names = FALSE)

stress_rows <- data.frame()

for (i in seq_len(nrow(strategies))) {
  s <- strategies[i, ]

  for (j in seq_len(nrow(stress_scenarios))) {
    sc <- stress_scenarios[j, ]

    stressed_mean <- s$mean_return + sc$return_shift
    stressed_volatility <- s$volatility * sc$volatility_multiplier
    stressed_shock <- s$shock_size * sc$shock_multiplier

    expected_stress_return <- stressed_mean + (s$shock_probability * stressed_shock) + s$recovery_credit

    stress_rows <- rbind(
      stress_rows,
      data.frame(
        strategy = s$strategy,
        scenario = sc$scenario,
        expected_stress_return = expected_stress_return,
        stressed_volatility = stressed_volatility,
        stressed_shock = stressed_shock,
        stringsAsFactors = FALSE
      )
    )
  }
}

write.csv(stress_rows, file.path(tables_dir, "scenario_stress_results.csv"), row.names = FALSE)

quality_map <- c(high = 1.00, medium = 0.65, low = 0.35)
probability_estimates$probability_quality_score <- quality_map[probability_estimates$quality]

probability_quality_summary <- aggregate(
  probability_quality_score ~ strategy,
  data = probability_estimates,
  FUN = mean
)

probability_quality_summary$probability_quality_flag <- ifelse(
  probability_quality_summary$probability_quality_score < 0.60,
  "review",
  "acceptable"
)

write.csv(probability_quality_summary, file.path(tables_dir, "probability_quality_summary.csv"), row.names = FALSE)

hazard_expected_loss <- merge(
  probability_estimates,
  consequences,
  by = c("hazard_id", "strategy"),
  all.x = TRUE
)

hazard_expected_loss$hazard_expected_loss <- hazard_expected_loss$probability * hazard_expected_loss$loss

write.csv(hazard_expected_loss, file.path(tables_dir, "hazard_expected_loss_summary.csv"), row.names = FALSE)

bayesian_update <- function(prior, sensitivity, false_positive_rate) {
  evidence_probability <- sensitivity * prior + false_positive_rate * (1 - prior)
  (sensitivity * prior) / evidence_probability
}

bayesian_rows <- data.frame(
  case = c("model drift signal", "cost escalation alert", "compound stress indicator"),
  prior = c(0.10, 0.15, 0.06),
  sensitivity = c(0.82, 0.76, 0.70),
  false_positive_rate = c(0.12, 0.18, 0.10),
  stringsAsFactors = FALSE
)

bayesian_rows$posterior_after_positive_signal <- mapply(
  bayesian_update,
  bayesian_rows$prior,
  bayesian_rows$sensitivity,
  bayesian_rows$false_positive_rate
)

write.csv(bayesian_rows, file.path(tables_dir, "bayesian_risk_update_summary.csv"), row.names = FALSE)

png(file.path(figures_dir, "risk_adjusted_score_by_strategy.png"), width = 1200, height = 800)
barplot(
  risk_summary$risk_adjusted_score,
  names.arg = risk_summary$strategy,
  las = 2,
  main = "Risk-Adjusted Score by Strategy",
  ylab = "Risk-adjusted score"
)
grid()
dev.off()

png(file.path(figures_dir, "expected_loss_by_strategy.png"), width = 1200, height = 800)
barplot(
  risk_summary$expected_loss,
  names.arg = risk_summary$strategy,
  las = 2,
  main = "Expected Loss by Strategy",
  ylab = "Expected loss"
)
grid()
dev.off()

png(file.path(figures_dir, "tail_exposure_by_strategy.png"), width = 1200, height = 800)
barplot(
  abs(risk_summary$conditional_value_at_risk_5pct),
  names.arg = risk_summary$strategy,
  las = 2,
  main = "Tail Exposure by Strategy",
  ylab = "Absolute CVaR at 5 percent"
)
grid()
dev.off()

print(risk_summary)
print(stress_rows)
print(probability_quality_summary)
print(bayesian_rows)
