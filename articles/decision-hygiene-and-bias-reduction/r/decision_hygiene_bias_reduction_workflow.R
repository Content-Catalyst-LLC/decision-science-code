# decision_hygiene_bias_reduction_workflow.R
# Base R workflow for decision hygiene, bias diagnostics,
# noise audits, calibration, and review tables.

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

domains <- c(
  "Public Policy",
  "Healthcare",
  "Financial Risk",
  "Infrastructure",
  "AI Governance",
  "Organizational Strategy"
)

bias_sources <- c(
  "anchoring",
  "availability",
  "confirmation",
  "overconfidence",
  "framing",
  "groupthink",
  "model_overtrust"
)

hygiene_practices <- c(
  "independent_estimates",
  "base_rate_check",
  "structured_dissent",
  "premortem",
  "calibration_review",
  "decision_record",
  "model_validation"
)

n <- 900

cases <- data.frame(
  case_id = seq_len(n),
  domain = sample(domains, n, replace = TRUE),
  bias_source = sample(bias_sources, n, replace = TRUE),
  hygiene_practice = sample(hygiene_practices, n, replace = TRUE),
  true_value = runif(n, 0.10, 0.90),
  evidence_quality = sample(c("low", "medium", "high"), n, replace = TRUE, prob = c(0.25, 0.50, 0.25)),
  decision_stakes = sample(c("low", "medium", "high"), n, replace = TRUE, prob = c(0.25, 0.45, 0.30)),
  stringsAsFactors = FALSE
)

bias_direction <- ifelse(
  cases$bias_source %in% c("anchoring", "overconfidence", "confirmation", "model_overtrust"),
  runif(n, 0.04, 0.16),
  runif(n, -0.10, 0.10)
)

noise_level <- ifelse(
  cases$evidence_quality == "high",
  0.05,
  ifelse(cases$evidence_quality == "medium", 0.09, 0.14)
)

hygiene_effect <- ifelse(
  cases$hygiene_practice %in% c("independent_estimates", "base_rate_check", "structured_dissent", "calibration_review"),
  runif(n, 0.25, 0.55),
  runif(n, 0.15, 0.45)
)

cases$pre_hygiene_judgment <- pmin(
  pmax(cases$true_value + bias_direction + rnorm(n, 0, noise_level), 0.01),
  0.99
)

cases$post_hygiene_judgment <- pmin(
  pmax(
    cases$true_value + bias_direction * (1 - hygiene_effect) +
      rnorm(n, 0, noise_level * (1 - hygiene_effect / 2)),
    0.01
  ),
  0.99
)

cases$outcome <- rbinom(n, size = 1, prob = cases$true_value)

cases$pre_error <- cases$pre_hygiene_judgment - cases$true_value
cases$post_error <- cases$post_hygiene_judgment - cases$true_value

cases$pre_absolute_error <- abs(cases$pre_error)
cases$post_absolute_error <- abs(cases$post_error)

cases$error_reduction <- cases$pre_absolute_error - cases$post_absolute_error

cases$pre_brier_score <- (cases$pre_hygiene_judgment - cases$outcome)^2
cases$post_brier_score <- (cases$post_hygiene_judgment - cases$outcome)^2
cases$brier_improvement <- cases$pre_brier_score - cases$post_brier_score

cases$post_probability_bin <- cut(
  cases$post_hygiene_judgment,
  breaks = seq(0, 1, by = 0.1),
  include.lowest = TRUE,
  right = FALSE
)

cases$review_flag <- ifelse(
  cases$post_absolute_error > 0.15 |
    cases$post_brier_score > 0.25 |
    cases$error_reduction < 0 |
    (cases$decision_stakes == "high" & cases$evidence_quality == "low"),
  "review",
  "acceptable"
)

write.csv(
  cases,
  file.path(tables_dir, "decision_hygiene_cases.csv"),
  row.names = FALSE
)

summarize_group <- function(x, group_field) {
  pre_bias <- mean(x$pre_error)
  post_bias <- mean(x$post_error)
  pre_noise <- sd(x$pre_error)
  post_noise <- sd(x$post_error)
  pre_mse <- mean(x$pre_error^2)
  post_mse <- mean(x$post_error^2)

  data.frame(
    group = unique(x[[group_field]])[1],
    n_cases = nrow(x),
    pre_bias = pre_bias,
    post_bias = post_bias,
    bias_reduction = abs(pre_bias) - abs(post_bias),
    pre_noise = pre_noise,
    post_noise = post_noise,
    noise_reduction = pre_noise - post_noise,
    pre_mse = pre_mse,
    post_mse = post_mse,
    mse_reduction = pre_mse - post_mse,
    mean_error_reduction = mean(x$error_reduction),
    mean_brier_improvement = mean(x$brier_improvement),
    review_rate = mean(x$review_flag == "review"),
    stringsAsFactors = FALSE
  )
}

domain_summary <- do.call(
  rbind,
  lapply(split(cases, cases$domain), summarize_group, group_field = "domain")
)
names(domain_summary)[names(domain_summary) == "group"] <- "domain"
domain_summary <- domain_summary[order(-domain_summary$mse_reduction), ]

write.csv(
  domain_summary,
  file.path(tables_dir, "domain_decision_hygiene_summary.csv"),
  row.names = FALSE
)

practice_summary <- do.call(
  rbind,
  lapply(split(cases, cases$hygiene_practice), summarize_group, group_field = "hygiene_practice")
)
names(practice_summary)[names(practice_summary) == "group"] <- "hygiene_practice"
practice_summary <- practice_summary[order(-practice_summary$mse_reduction), ]

write.csv(
  practice_summary,
  file.path(tables_dir, "hygiene_practice_summary.csv"),
  row.names = FALSE
)

bias_source_summary <- do.call(
  rbind,
  lapply(split(cases, cases$bias_source), summarize_group, group_field = "bias_source")
)
names(bias_source_summary)[names(bias_source_summary) == "group"] <- "bias_source"
bias_source_summary <- bias_source_summary[order(-bias_source_summary$mse_reduction), ]

write.csv(
  bias_source_summary,
  file.path(tables_dir, "bias_source_summary.csv"),
  row.names = FALSE
)

calibration_table <- do.call(
  rbind,
  lapply(
    split(cases, cases$post_probability_bin, drop = TRUE),
    function(x) {
      data.frame(
        probability_bin = as.character(unique(x$post_probability_bin))[1],
        n_cases = nrow(x),
        average_probability = mean(x$post_hygiene_judgment),
        observed_frequency = mean(x$outcome),
        calibration_gap = mean(x$post_hygiene_judgment) - mean(x$outcome),
        absolute_calibration_gap = abs(mean(x$post_hygiene_judgment) - mean(x$outcome)),
        average_brier_score = mean(x$post_brier_score),
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
  file.path(tables_dir, "decision_hygiene_calibration_table.csv"),
  row.names = FALSE
)

review_queue <- cases[cases$review_flag == "review", c(
  "case_id",
  "domain",
  "bias_source",
  "hygiene_practice",
  "evidence_quality",
  "decision_stakes",
  "true_value",
  "post_hygiene_judgment",
  "post_absolute_error",
  "post_brier_score",
  "error_reduction",
  "review_flag"
)]

review_queue <- review_queue[order(
  -review_queue$post_absolute_error,
  -review_queue$post_brier_score
), ]

write.csv(
  review_queue,
  file.path(tables_dir, "decision_hygiene_review_queue.csv"),
  row.names = FALSE
)

overall_metrics <- data.frame(
  metric = c(
    "pre_bias",
    "post_bias",
    "bias_reduction",
    "pre_noise",
    "post_noise",
    "noise_reduction",
    "pre_mse",
    "post_mse",
    "mse_reduction",
    "expected_calibration_error",
    "review_rate"
  ),
  value = c(
    mean(cases$pre_error),
    mean(cases$post_error),
    abs(mean(cases$pre_error)) - abs(mean(cases$post_error)),
    sd(cases$pre_error),
    sd(cases$post_error),
    sd(cases$pre_error) - sd(cases$post_error),
    mean(cases$pre_error^2),
    mean(cases$post_error^2),
    mean(cases$pre_error^2) - mean(cases$post_error^2),
    sum(calibration_table$weighted_calibration_error),
    mean(cases$review_flag == "review")
  ),
  stringsAsFactors = FALSE
)

write.csv(
  overall_metrics,
  file.path(tables_dir, "overall_decision_hygiene_metrics.csv"),
  row.names = FALSE
)

png(file.path(figures_dir, "mse_reduction_by_practice.png"), width = 1200, height = 800)
barplot(
  practice_summary$mse_reduction,
  names.arg = practice_summary$hygiene_practice,
  las = 2,
  main = "Mean Squared Error Reduction by Hygiene Practice",
  ylab = "MSE reduction"
)
grid()
dev.off()

png(file.path(figures_dir, "bias_and_noise_by_domain.png"), width = 1200, height = 800)
plot(
  domain_summary$bias_reduction,
  domain_summary$noise_reduction,
  xlab = "Bias reduction",
  ylab = "Noise reduction",
  main = "Bias and Noise Reduction by Domain",
  pch = 19
)
text(
  domain_summary$bias_reduction,
  domain_summary$noise_reduction,
  labels = domain_summary$domain,
  pos = 4,
  cex = 0.8
)
grid()
dev.off()

png(file.path(figures_dir, "decision_hygiene_calibration_diagram.png"), width = 1200, height = 800)
plot(
  calibration_table$average_probability,
  calibration_table$observed_frequency,
  xlim = c(0, 1),
  ylim = c(0, 1),
  xlab = "Average post-hygiene probability",
  ylab = "Observed frequency",
  main = "Decision Hygiene Calibration Diagram",
  pch = 19
)
abline(0, 1, lty = 2)
grid()
dev.off()

print(overall_metrics)
print(practice_summary)
print(domain_summary)
print(head(review_queue, 25))
