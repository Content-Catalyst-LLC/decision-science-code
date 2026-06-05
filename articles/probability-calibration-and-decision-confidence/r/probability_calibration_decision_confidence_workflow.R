# probability_calibration_decision_confidence_workflow.R
# Base R workflow for probability calibration, Brier scores,
# log loss, reliability tables, confidence diagnostics, and threshold decisions.

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

n <- 1200

domains <- c(
  "Strategic Forecast",
  "Risk Forecast",
  "Operational Forecast",
  "Policy Forecast",
  "Model Governance Forecast"
)

forecast_data <- data.frame(
  forecast_id = seq_len(n),
  domain = sample(domains, n, replace = TRUE),
  base_rate = runif(n, 0.10, 0.85),
  evidence_strength = runif(n, -0.25, 0.25),
  confidence_profile = sample(
    c("well calibrated", "overconfident", "underconfident"),
    n,
    replace = TRUE,
    prob = c(0.55, 0.30, 0.15)
  ),
  stringsAsFactors = FALSE
)

true_probability <- pmin(
  pmax(forecast_data$base_rate + forecast_data$evidence_strength, 0.02),
  0.98
)

forecast_data$outcome <- rbinom(n, size = 1, prob = true_probability)
forecast_data$true_probability <- true_probability
forecast_data$forecast_probability <- true_probability

overconfident <- forecast_data$confidence_profile == "overconfident"
underconfident <- forecast_data$confidence_profile == "underconfident"

forecast_data$forecast_probability[overconfident] <- (
  0.5 + 1.35 * (forecast_data$forecast_probability[overconfident] - 0.5)
)

forecast_data$forecast_probability[underconfident] <- (
  0.5 + 0.65 * (forecast_data$forecast_probability[underconfident] - 0.5)
)

forecast_data$forecast_probability <- pmin(pmax(forecast_data$forecast_probability, 0.01), 0.99)

forecast_data$brier_component <- (forecast_data$forecast_probability - forecast_data$outcome)^2

forecast_data$log_loss_component <- -(
  forecast_data$outcome * log(forecast_data$forecast_probability) +
  (1 - forecast_data$outcome) * log(1 - forecast_data$forecast_probability)
)

forecast_data$probability_bin <- cut(
  forecast_data$forecast_probability,
  breaks = seq(0, 1, by = 0.1),
  include.lowest = TRUE,
  right = FALSE
)

write.csv(
  forecast_data,
  file.path(tables_dir, "forecast_calibration_observations.csv"),
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
        average_brier_score = mean(x$brier_component),
        average_log_loss = mean(x$log_loss_component),
        stringsAsFactors = FALSE
      )
    }
  )
)

calibration_table$weighted_calibration_error <- (
  calibration_table$n_forecasts / sum(calibration_table$n_forecasts)
) * calibration_table$absolute_calibration_gap

expected_calibration_error <- sum(calibration_table$weighted_calibration_error)

write.csv(
  calibration_table,
  file.path(tables_dir, "calibration_reliability_table.csv"),
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
        calibration_gap = mean(x$forecast_probability) - mean(x$outcome),
        absolute_calibration_gap = abs(mean(x$forecast_probability) - mean(x$outcome)),
        brier_score = mean(x$brier_component),
        log_loss = mean(x$log_loss_component),
        stringsAsFactors = FALSE
      )
    }
  )
)

domain_summary <- domain_summary[order(domain_summary$brier_score), ]

write.csv(
  domain_summary,
  file.path(tables_dir, "domain_calibration_summary.csv"),
  row.names = FALSE
)

thresholds <- c(0.55, 0.65, 0.75, 0.85)
threshold_rows <- data.frame()

for (threshold in thresholds) {
  acted <- forecast_data$forecast_probability >= threshold

  if (sum(acted) == 0) {
    observed_success_rate <- NA
    average_probability <- NA
    calibration_gap <- NA
    brier_among_acted <- NA
  } else {
    observed_success_rate <- mean(forecast_data$outcome[acted])
    average_probability <- mean(forecast_data$forecast_probability[acted])
    calibration_gap <- average_probability - observed_success_rate
    brier_among_acted <- mean(forecast_data$brier_component[acted])
  }

  threshold_rows <- rbind(
    threshold_rows,
    data.frame(
      decision_threshold = threshold,
      action_count = sum(acted),
      action_rate = mean(acted),
      average_probability_among_acted = average_probability,
      observed_success_rate_among_acted = observed_success_rate,
      threshold_calibration_gap = calibration_gap,
      brier_score_among_acted = brier_among_acted,
      stringsAsFactors = FALSE
    )
  )
}

write.csv(
  threshold_rows,
  file.path(tables_dir, "decision_threshold_calibration.csv"),
  row.names = FALSE
)

confidence_profile_summary <- do.call(
  rbind,
  lapply(
    split(forecast_data, forecast_data$confidence_profile),
    function(x) {
      data.frame(
        confidence_profile = unique(x$confidence_profile),
        n_forecasts = nrow(x),
        average_forecast_probability = mean(x$forecast_probability),
        observed_frequency = mean(x$outcome),
        calibration_gap = mean(x$forecast_probability) - mean(x$outcome),
        absolute_calibration_gap = abs(mean(x$forecast_probability) - mean(x$outcome)),
        brier_score = mean(x$brier_component),
        log_loss = mean(x$log_loss_component),
        stringsAsFactors = FALSE
      )
    }
  )
)

write.csv(
  confidence_profile_summary,
  file.path(tables_dir, "confidence_profile_summary.csv"),
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

png(file.path(figures_dir, "calibration_reliability_diagram.png"), width = 1200, height = 800)
plot(
  calibration_table$average_forecast_probability,
  calibration_table$observed_frequency,
  xlim = c(0, 1),
  ylim = c(0, 1),
  xlab = "Average forecast probability",
  ylab = "Observed frequency",
  main = "Calibration Reliability Diagram",
  pch = 19
)
abline(0, 1, lty = 2)
grid()
dev.off()

png(file.path(figures_dir, "domain_brier_scores.png"), width = 1200, height = 800)
barplot(
  domain_summary$brier_score,
  names.arg = domain_summary$domain,
  las = 2,
  main = "Brier Score by Forecast Domain",
  ylab = "Brier score"
)
grid()
dev.off()

png(file.path(figures_dir, "calibration_gap_by_bin.png"), width = 1200, height = 800)
barplot(
  calibration_table$calibration_gap,
  names.arg = calibration_table$probability_bin,
  las = 2,
  main = "Calibration Gap by Probability Bin",
  ylab = "Forecast probability minus observed frequency"
)
abline(h = 0, lty = 2)
grid()
dev.off()

overall_metrics <- data.frame(
  metric = c(
    "overall_brier_score",
    "overall_log_loss",
    "expected_calibration_error",
    "average_forecast_probability",
    "observed_frequency"
  ),
  value = c(
    mean(forecast_data$brier_component),
    mean(forecast_data$log_loss_component),
    expected_calibration_error,
    mean(forecast_data$forecast_probability),
    mean(forecast_data$outcome)
  ),
  stringsAsFactors = FALSE
)

write.csv(
  overall_metrics,
  file.path(tables_dir, "overall_calibration_metrics.csv"),
  row.names = FALSE
)

print(overall_metrics)
print(calibration_table)
print(domain_summary)
print(threshold_rows)
