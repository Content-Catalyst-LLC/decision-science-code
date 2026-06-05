# forecasting_decision_support_workflow.R
# Base R workflow for forecast evaluation, probabilistic forecasts,
# threshold decisions, calibration, forecast value, and decision-support summaries.

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

n <- 900

domains <- c(
  "Public Policy",
  "Healthcare",
  "Financial Risk",
  "Infrastructure",
  "AI Governance",
  "Organizational Strategy"
)

forecast_data <- data.frame(
  forecast_id = seq_len(n),
  domain = sample(domains, n, replace = TRUE),
  base_rate = runif(n, 0.15, 0.80),
  signal_strength = runif(n, -0.20, 0.25),
  forecast_horizon_days = sample(c(7, 30, 90, 180, 365), n, replace = TRUE),
  forecast_cost = runif(n, 1, 12),
  false_positive_cost = runif(n, 5, 30),
  false_negative_cost = runif(n, 20, 90),
  stringsAsFactors = FALSE
)

horizon_penalty <- forecast_data$forecast_horizon_days / 365 * runif(n, -0.10, 0.10)

true_probability <- pmin(
  pmax(forecast_data$base_rate + forecast_data$signal_strength + horizon_penalty, 0.02),
  0.98
)

forecast_noise <- rnorm(n, mean = 0, sd = 0.08)

forecast_data$true_probability <- true_probability
forecast_data$forecast_probability <- pmin(pmax(true_probability + forecast_noise, 0.01), 0.99)
forecast_data$outcome <- rbinom(n, size = 1, prob = true_probability)

forecast_data$brier_score <- (forecast_data$forecast_probability - forecast_data$outcome)^2

forecast_data$log_loss <- -(
  forecast_data$outcome * log(forecast_data$forecast_probability) +
  (1 - forecast_data$outcome) * log(1 - forecast_data$forecast_probability)
)

forecast_data$probability_bin <- cut(
  forecast_data$forecast_probability,
  breaks = seq(0, 1, by = 0.1),
  include.lowest = TRUE,
  right = FALSE
)

forecast_data$decision_threshold <- forecast_data$false_positive_cost /
  (forecast_data$false_positive_cost + forecast_data$false_negative_cost)

forecast_data$forecast_supported_action <- forecast_data$forecast_probability >= forecast_data$decision_threshold
forecast_data$base_rate_action <- forecast_data$base_rate >= forecast_data$decision_threshold

expected_loss <- function(action, probability, false_positive_cost, false_negative_cost) {
  ifelse(
    action,
    (1 - probability) * false_positive_cost,
    probability * false_negative_cost
  )
}

forecast_data$expected_loss_with_forecast <- expected_loss(
  forecast_data$forecast_supported_action,
  forecast_data$forecast_probability,
  forecast_data$false_positive_cost,
  forecast_data$false_negative_cost
)

forecast_data$expected_loss_without_forecast <- expected_loss(
  forecast_data$base_rate_action,
  forecast_data$base_rate,
  forecast_data$false_positive_cost,
  forecast_data$false_negative_cost
)

forecast_data$forecast_value_proxy <- (
  forecast_data$expected_loss_without_forecast -
  forecast_data$expected_loss_with_forecast -
  forecast_data$forecast_cost
)

write.csv(
  forecast_data,
  file.path(tables_dir, "forecast_decision_observations.csv"),
  row.names = FALSE
)

calibration_table <- do.call(
  rbind,
  lapply(
    split(forecast_data, forecast_data$probability_bin),
    function(x) {
      data.frame(
        probability_bin = as.character(unique(x$probability_bin)),
        n_forecasts = nrow(x),
        average_forecast_probability = mean(x$forecast_probability),
        observed_frequency = mean(x$outcome),
        calibration_gap = mean(x$forecast_probability) - mean(x$outcome),
        absolute_calibration_gap = abs(mean(x$forecast_probability) - mean(x$outcome)),
        average_brier_score = mean(x$brier_score),
        average_log_loss = mean(x$log_loss),
        stringsAsFactors = FALSE
      )
    }
  )
)

calibration_table$weighted_calibration_error <- (
  calibration_table$n_forecasts / sum(calibration_table$n_forecasts)
) * calibration_table$absolute_calibration_gap

write.csv(
  calibration_table,
  file.path(tables_dir, "forecast_calibration_table.csv"),
  row.names = FALSE
)

domain_summary <- do.call(
  rbind,
  lapply(
    split(forecast_data, forecast_data$domain),
    function(x) {
      data.frame(
        domain = unique(x$domain),
        n_forecasts = nrow(x),
        average_forecast_probability = mean(x$forecast_probability),
        observed_frequency = mean(x$outcome),
        brier_score = mean(x$brier_score),
        log_loss = mean(x$log_loss),
        average_forecast_value_proxy = mean(x$forecast_value_proxy),
        positive_forecast_value_rate = mean(x$forecast_value_proxy > 0),
        action_rate_with_forecast = mean(x$forecast_supported_action),
        action_rate_without_forecast = mean(x$base_rate_action),
        stringsAsFactors = FALSE
      )
    }
  )
)

domain_summary <- domain_summary[order(-domain_summary$average_forecast_value_proxy), ]

write.csv(
  domain_summary,
  file.path(tables_dir, "domain_forecast_decision_support_summary.csv"),
  row.names = FALSE
)

horizon_summary <- do.call(
  rbind,
  lapply(
    split(forecast_data, forecast_data$forecast_horizon_days),
    function(x) {
      data.frame(
        forecast_horizon_days = unique(x$forecast_horizon_days),
        n_forecasts = nrow(x),
        brier_score = mean(x$brier_score),
        log_loss = mean(x$log_loss),
        calibration_gap = mean(x$forecast_probability) - mean(x$outcome),
        average_forecast_value_proxy = mean(x$forecast_value_proxy),
        stringsAsFactors = FALSE
      )
    }
  )
)

horizon_summary <- horizon_summary[order(horizon_summary$forecast_horizon_days), ]

write.csv(
  horizon_summary,
  file.path(tables_dir, "forecast_horizon_summary.csv"),
  row.names = FALSE
)

threshold_summary <- data.frame()

for (threshold in c(0.25, 0.40, 0.55, 0.70, 0.85)) {
  acted <- forecast_data$forecast_probability >= threshold

  threshold_summary <- rbind(
    threshold_summary,
    data.frame(
      threshold = threshold,
      action_rate = mean(acted),
      observed_frequency_among_acted = ifelse(sum(acted) == 0, NA, mean(forecast_data$outcome[acted])),
      average_probability_among_acted = ifelse(sum(acted) == 0, NA, mean(forecast_data$forecast_probability[acted])),
      average_brier_among_acted = ifelse(sum(acted) == 0, NA, mean(forecast_data$brier_score[acted])),
      stringsAsFactors = FALSE
    )
  )
}

write.csv(
  threshold_summary,
  file.path(tables_dir, "forecast_threshold_summary.csv"),
  row.names = FALSE
)

reference_classes <- read.csv(file.path(article_root, "data", "synthetic_reference_classes.csv"), stringsAsFactors = FALSE)

base_rate_rows <- merge(
  domain_summary[, c("domain", "average_forecast_probability", "observed_frequency")],
  reference_classes,
  by.x = "domain",
  by.y = "reference_class",
  all.x = TRUE
)

base_rate_rows$forecast_minus_base_rate <- base_rate_rows$average_forecast_probability - base_rate_rows$base_rate
base_rate_rows$observed_minus_base_rate <- base_rate_rows$observed_frequency - base_rate_rows$base_rate

write.csv(
  base_rate_rows,
  file.path(tables_dir, "base_rate_reference_class_checks.csv"),
  row.names = FALSE
)

early_warning <- read.csv(file.path(article_root, "data", "synthetic_early_warning_signals.csv"), stringsAsFactors = FALSE)
early_warning$triggered <- ifelse(
  early_warning$direction == "above",
  early_warning$current_value >= early_warning$review_threshold,
  early_warning$current_value <= early_warning$review_threshold
)

write.csv(
  early_warning,
  file.path(tables_dir, "early_warning_signal_summary.csv"),
  row.names = FALSE
)

overall_metrics <- data.frame(
  metric = c(
    "overall_brier_score",
    "overall_log_loss",
    "expected_calibration_error",
    "average_forecast_value_proxy",
    "positive_forecast_value_rate",
    "forecast_action_rate",
    "base_rate_action_rate"
  ),
  value = c(
    mean(forecast_data$brier_score),
    mean(forecast_data$log_loss),
    sum(calibration_table$weighted_calibration_error),
    mean(forecast_data$forecast_value_proxy),
    mean(forecast_data$forecast_value_proxy > 0),
    mean(forecast_data$forecast_supported_action),
    mean(forecast_data$base_rate_action)
  ),
  stringsAsFactors = FALSE
)

write.csv(
  overall_metrics,
  file.path(tables_dir, "overall_forecast_decision_metrics.csv"),
  row.names = FALSE
)

png(file.path(figures_dir, "forecast_reliability_diagram.png"), width = 1200, height = 800)
plot(
  calibration_table$average_forecast_probability,
  calibration_table$observed_frequency,
  xlim = c(0, 1),
  ylim = c(0, 1),
  xlab = "Average forecast probability",
  ylab = "Observed frequency",
  main = "Forecast Reliability Diagram",
  pch = 19
)
abline(0, 1, lty = 2)
grid()
dev.off()

png(file.path(figures_dir, "forecast_value_by_domain.png"), width = 1200, height = 800)
barplot(
  domain_summary$average_forecast_value_proxy,
  names.arg = domain_summary$domain,
  las = 2,
  main = "Average Forecast Value Proxy by Domain",
  ylab = "Expected loss reduction minus forecast cost"
)
abline(h = 0, lty = 2)
grid()
dev.off()

png(file.path(figures_dir, "forecast_quality_by_horizon.png"), width = 1200, height = 800)
plot(
  horizon_summary$forecast_horizon_days,
  horizon_summary$brier_score,
  type = "b",
  xlab = "Forecast horizon in days",
  ylab = "Brier score",
  main = "Forecast Quality by Horizon"
)
grid()
dev.off()

print(overall_metrics)
print(domain_summary)
print(horizon_summary)
print(threshold_summary)
