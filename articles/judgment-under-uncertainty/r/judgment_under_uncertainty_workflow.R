# judgment_under_uncertainty_workflow.R
# Base R workflow for calibration, Bayesian updating,
# confidence error, Brier scoring, and judgment review tables.

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

cases <- data.frame(
  case_id = seq_len(n),
  domain = sample(domains, n, replace = TRUE),
  prior = runif(n, 0.08, 0.85),
  likelihood_if_true = runif(n, 0.45, 0.95),
  likelihood_if_false = runif(n, 0.05, 0.60),
  anchor = runif(n, 0.10, 0.90),
  anchor_weight = runif(n, 0.15, 0.55),
  confidence_noise = rnorm(n, mean = 0, sd = 0.08),
  evidence_quality = sample(c("low", "medium", "high"), n, replace = TRUE, prob = c(0.25, 0.50, 0.25)),
  stringsAsFactors = FALSE
)

posterior_odds <- (cases$prior / (1 - cases$prior)) *
  (cases$likelihood_if_true / cases$likelihood_if_false)

cases$posterior <- posterior_odds / (1 + posterior_odds)

cases$anchor_adjusted_judgment <- pmin(
  pmax(
    cases$anchor_weight * cases$anchor +
      (1 - cases$anchor_weight) * cases$posterior,
    0.01
  ),
  0.99
)

quality_multiplier <- ifelse(
  cases$evidence_quality == "high",
  0.03,
  ifelse(cases$evidence_quality == "medium", 0.07, 0.12)
)

cases$forecast_probability <- pmin(
  pmax(
    cases$anchor_adjusted_judgment + rnorm(n, 0, quality_multiplier),
    0.01
  ),
  0.99
)

cases$confidence <- pmin(
  pmax(
    cases$forecast_probability + cases$confidence_noise,
    0.01
  ),
  0.99
)

cases$outcome <- rbinom(n, size = 1, prob = cases$posterior)

cases$brier_score <- (cases$forecast_probability - cases$outcome)^2
cases$absolute_error <- abs(cases$forecast_probability - cases$outcome)
cases$confidence_gap <- cases$confidence - cases$forecast_probability
cases$anchor_distortion <- abs(cases$anchor_adjusted_judgment - cases$posterior)
cases$probability_bin <- cut(
  cases$forecast_probability,
  breaks = seq(0, 1, by = 0.1),
  include.lowest = TRUE,
  right = FALSE
)

cases$confidence_flag <- ifelse(
  cases$confidence_gap > 0.10,
  "overconfident",
  ifelse(cases$confidence_gap < -0.10, "underconfident", "approximately calibrated")
)

cases$review_flag <- ifelse(
  cases$brier_score > 0.25 |
    abs(cases$confidence_gap) > 0.15 |
    cases$anchor_distortion > 0.15,
  "review",
  "acceptable"
)

write.csv(
  cases,
  file.path(tables_dir, "judgment_under_uncertainty_cases.csv"),
  row.names = FALSE
)

domain_summary <- do.call(
  rbind,
  lapply(
    split(cases, cases$domain),
    function(x) {
      data.frame(
        domain = unique(x$domain),
        n_cases = nrow(x),
        average_prior = mean(x$prior),
        average_posterior = mean(x$posterior),
        average_forecast_probability = mean(x$forecast_probability),
        observed_frequency = mean(x$outcome),
        average_brier_score = mean(x$brier_score),
        average_absolute_error = mean(x$absolute_error),
        average_confidence_gap = mean(x$confidence_gap),
        average_anchor_distortion = mean(x$anchor_distortion),
        review_rate = mean(x$review_flag == "review"),
        stringsAsFactors = FALSE
      )
    }
  )
)

domain_summary <- domain_summary[order(-domain_summary$average_brier_score), ]

write.csv(
  domain_summary,
  file.path(tables_dir, "domain_judgment_quality_summary.csv"),
  row.names = FALSE
)

evidence_quality_summary <- do.call(
  rbind,
  lapply(
    split(cases, cases$evidence_quality),
    function(x) {
      data.frame(
        evidence_quality = unique(x$evidence_quality),
        n_cases = nrow(x),
        average_forecast_probability = mean(x$forecast_probability),
        observed_frequency = mean(x$outcome),
        average_brier_score = mean(x$brier_score),
        average_absolute_error = mean(x$absolute_error),
        average_anchor_distortion = mean(x$anchor_distortion),
        review_rate = mean(x$review_flag == "review"),
        stringsAsFactors = FALSE
      )
    }
  )
)

write.csv(
  evidence_quality_summary,
  file.path(tables_dir, "evidence_quality_summary.csv"),
  row.names = FALSE
)

calibration_table <- do.call(
  rbind,
  lapply(
    split(cases, cases$probability_bin),
    function(x) {
      data.frame(
        probability_bin = as.character(unique(x$probability_bin)),
        n_cases = nrow(x),
        average_forecast_probability = mean(x$forecast_probability),
        observed_frequency = mean(x$outcome),
        calibration_gap = mean(x$forecast_probability) - mean(x$outcome),
        absolute_calibration_gap = abs(mean(x$forecast_probability) - mean(x$outcome)),
        average_brier_score = mean(x$brier_score),
        stringsAsFactors = FALSE
      )
    }
  )
)

calibration_table$weighted_calibration_error <- (
  calibration_table$n_cases / sum(calibration_table$n_cases)
) * calibration_table$absolute_calibration_gap

write.csv(
  calibration_table,
  file.path(tables_dir, "judgment_calibration_table.csv"),
  row.names = FALSE
)

confidence_summary <- do.call(
  rbind,
  lapply(
    split(cases, cases$confidence_flag),
    function(x) {
      data.frame(
        confidence_flag = unique(x$confidence_flag),
        n_cases = nrow(x),
        average_forecast_probability = mean(x$forecast_probability),
        average_confidence = mean(x$confidence),
        observed_frequency = mean(x$outcome),
        average_brier_score = mean(x$brier_score),
        review_rate = mean(x$review_flag == "review"),
        stringsAsFactors = FALSE
      )
    }
  )
)

write.csv(
  confidence_summary,
  file.path(tables_dir, "confidence_error_summary.csv"),
  row.names = FALSE
)

review_queue <- cases[cases$review_flag == "review", c(
  "case_id",
  "domain",
  "prior",
  "posterior",
  "forecast_probability",
  "confidence",
  "outcome",
  "brier_score",
  "confidence_gap",
  "anchor_distortion",
  "confidence_flag",
  "review_flag"
)]

write.csv(
  review_queue,
  file.path(tables_dir, "judgment_review_queue.csv"),
  row.names = FALSE
)

overall_metrics <- data.frame(
  metric = c(
    "mean_brier_score",
    "expected_calibration_error",
    "mean_absolute_error",
    "mean_confidence_gap",
    "mean_anchor_distortion",
    "review_rate"
  ),
  value = c(
    mean(cases$brier_score),
    sum(calibration_table$weighted_calibration_error),
    mean(cases$absolute_error),
    mean(cases$confidence_gap),
    mean(cases$anchor_distortion),
    mean(cases$review_flag == "review")
  ),
  stringsAsFactors = FALSE
)

write.csv(
  overall_metrics,
  file.path(tables_dir, "overall_judgment_under_uncertainty_metrics.csv"),
  row.names = FALSE
)

png(file.path(figures_dir, "judgment_calibration_diagram.png"), width = 1200, height = 800)
plot(
  calibration_table$average_forecast_probability,
  calibration_table$observed_frequency,
  xlim = c(0, 1),
  ylim = c(0, 1),
  xlab = "Average forecast probability",
  ylab = "Observed frequency",
  main = "Judgment Under Uncertainty Calibration Diagram",
  pch = 19
)
abline(0, 1, lty = 2)
grid()
dev.off()

png(file.path(figures_dir, "brier_score_by_domain.png"), width = 1200, height = 800)
barplot(
  domain_summary$average_brier_score,
  names.arg = domain_summary$domain,
  las = 2,
  main = "Average Brier Score by Domain",
  ylab = "Average Brier score"
)
grid()
dev.off()

png(file.path(figures_dir, "confidence_error_summary.png"), width = 1200, height = 800)
barplot(
  confidence_summary$average_brier_score,
  names.arg = confidence_summary$confidence_flag,
  las = 2,
  main = "Brier Score by Confidence Flag",
  ylab = "Average Brier score"
)
grid()
dev.off()

print(overall_metrics)
print(domain_summary)
print(calibration_table)
print(confidence_summary)
