# heuristics_cognitive_biases_workflow.R
# Base R workflow for heuristic judgment diagnostics,
# calibration error, confidence distortion, and debiasing review tables.

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

bias_profiles <- c(
  "availability",
  "representativeness",
  "anchoring",
  "confirmation",
  "overconfidence",
  "balanced"
)

judgments <- data.frame(
  case_id = seq_len(n),
  domain = sample(domains, n, replace = TRUE),
  bias_profile = sample(
    bias_profiles,
    n,
    replace = TRUE,
    prob = c(0.16, 0.15, 0.16, 0.16, 0.17, 0.20)
  ),
  base_rate = runif(n, 0.10, 0.85),
  evidence_signal = runif(n, -0.25, 0.25),
  anchor = runif(n, 0.20, 0.90),
  salience_multiplier = runif(n, 0.70, 1.60),
  confirming_evidence = runif(n, 0.00, 0.30),
  disconfirming_evidence = runif(n, 0.00, 0.30),
  stringsAsFactors = FALSE
)

judgments$evidence_based_probability <- pmin(
  pmax(judgments$base_rate + judgments$evidence_signal, 0.01),
  0.99
)

judgments$judged_probability <- judgments$evidence_based_probability

availability_idx <- judgments$bias_profile == "availability"
representativeness_idx <- judgments$bias_profile == "representativeness"
anchoring_idx <- judgments$bias_profile == "anchoring"
confirmation_idx <- judgments$bias_profile == "confirmation"
overconfidence_idx <- judgments$bias_profile == "overconfidence"

judgments$judged_probability[availability_idx] <- pmin(
  pmax(
    judgments$evidence_based_probability[availability_idx] *
      judgments$salience_multiplier[availability_idx],
    0.01
  ),
  0.99
)

judgments$judged_probability[representativeness_idx] <- pmin(
  pmax(
    0.35 * judgments$base_rate[representativeness_idx] +
      0.65 * judgments$evidence_based_probability[representativeness_idx],
    0.01
  ),
  0.99
)

judgments$judged_probability[anchoring_idx] <- pmin(
  pmax(
    0.45 * judgments$anchor[anchoring_idx] +
      0.55 * judgments$evidence_based_probability[anchoring_idx],
    0.01
  ),
  0.99
)

judgments$judged_probability[confirmation_idx] <- pmin(
  pmax(
    judgments$evidence_based_probability[confirmation_idx] +
      0.80 * judgments$confirming_evidence[confirmation_idx] -
      0.35 * judgments$disconfirming_evidence[confirmation_idx],
    0.01
  ),
  0.99
)

judgments$confidence <- judgments$judged_probability

judgments$confidence[overconfidence_idx] <- pmin(
  pmax(
    0.5 + 1.40 * (judgments$judged_probability[overconfidence_idx] - 0.5),
    0.01
  ),
  0.99
)

judgments$confidence[!overconfidence_idx] <- pmin(
  pmax(
    judgments$judged_probability[!overconfidence_idx] + rnorm(sum(!overconfidence_idx), 0, 0.04),
    0.01
  ),
  0.99
)

judgments$outcome <- rbinom(n, size = 1, prob = judgments$evidence_based_probability)

judgments$brier_score <- (judgments$judged_probability - judgments$outcome)^2
judgments$confidence_gap <- judgments$confidence - judgments$judged_probability
judgments$bias_magnitude <- abs(judgments$judged_probability - judgments$evidence_based_probability)
judgments$probability_bin <- cut(
  judgments$judged_probability,
  breaks = seq(0, 1, by = 0.1),
  include.lowest = TRUE,
  right = FALSE
)

judgments$review_flag <- ifelse(
  judgments$bias_magnitude > 0.12 |
    abs(judgments$confidence_gap) > 0.12 |
    judgments$brier_score > 0.25,
  "review",
  "acceptable"
)

write.csv(
  judgments,
  file.path(tables_dir, "heuristic_judgment_cases.csv"),
  row.names = FALSE
)

bias_summary <- do.call(
  rbind,
  lapply(
    split(judgments, judgments$bias_profile),
    function(x) {
      data.frame(
        bias_profile = unique(x$bias_profile),
        n_cases = nrow(x),
        average_evidence_based_probability = mean(x$evidence_based_probability),
        average_judged_probability = mean(x$judged_probability),
        observed_frequency = mean(x$outcome),
        average_brier_score = mean(x$brier_score),
        average_bias_magnitude = mean(x$bias_magnitude),
        average_confidence_gap = mean(x$confidence_gap),
        review_rate = mean(x$review_flag == "review"),
        stringsAsFactors = FALSE
      )
    }
  )
)

bias_summary <- bias_summary[order(-bias_summary$average_bias_magnitude), ]

write.csv(
  bias_summary,
  file.path(tables_dir, "bias_profile_summary.csv"),
  row.names = FALSE
)

domain_summary <- do.call(
  rbind,
  lapply(
    split(judgments, judgments$domain),
    function(x) {
      data.frame(
        domain = unique(x$domain),
        n_cases = nrow(x),
        average_judged_probability = mean(x$judged_probability),
        observed_frequency = mean(x$outcome),
        calibration_gap = mean(x$judged_probability) - mean(x$outcome),
        average_brier_score = mean(x$brier_score),
        average_bias_magnitude = mean(x$bias_magnitude),
        review_rate = mean(x$review_flag == "review"),
        stringsAsFactors = FALSE
      )
    }
  )
)

domain_summary <- domain_summary[order(-domain_summary$review_rate), ]

write.csv(
  domain_summary,
  file.path(tables_dir, "domain_bias_diagnostics.csv"),
  row.names = FALSE
)

calibration_table <- do.call(
  rbind,
  lapply(
    split(judgments, judgments$probability_bin),
    function(x) {
      data.frame(
        probability_bin = as.character(unique(x$probability_bin)),
        n_cases = nrow(x),
        average_judged_probability = mean(x$judged_probability),
        observed_frequency = mean(x$outcome),
        calibration_gap = mean(x$judged_probability) - mean(x$outcome),
        absolute_calibration_gap = abs(mean(x$judged_probability) - mean(x$outcome)),
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
  file.path(tables_dir, "heuristic_calibration_table.csv"),
  row.names = FALSE
)

debiasing_review <- judgments[judgments$review_flag == "review", c(
  "case_id",
  "domain",
  "bias_profile",
  "evidence_based_probability",
  "judged_probability",
  "confidence",
  "outcome",
  "brier_score",
  "bias_magnitude",
  "confidence_gap",
  "review_flag"
)]

write.csv(
  debiasing_review,
  file.path(tables_dir, "debiasing_review_queue.csv"),
  row.names = FALSE
)

overall_metrics <- data.frame(
  metric = c(
    "mean_brier_score",
    "expected_calibration_error",
    "mean_bias_magnitude",
    "mean_confidence_gap",
    "review_rate"
  ),
  value = c(
    mean(judgments$brier_score),
    sum(calibration_table$weighted_calibration_error),
    mean(judgments$bias_magnitude),
    mean(judgments$confidence_gap),
    mean(judgments$review_flag == "review")
  ),
  stringsAsFactors = FALSE
)

write.csv(
  overall_metrics,
  file.path(tables_dir, "overall_bias_diagnostics.csv"),
  row.names = FALSE
)

png(file.path(figures_dir, "bias_magnitude_by_profile.png"), width = 1200, height = 800)
barplot(
  bias_summary$average_bias_magnitude,
  names.arg = bias_summary$bias_profile,
  las = 2,
  main = "Average Bias Magnitude by Heuristic Profile",
  ylab = "Average absolute distortion"
)
grid()
dev.off()

png(file.path(figures_dir, "heuristic_calibration_diagram.png"), width = 1200, height = 800)
plot(
  calibration_table$average_judged_probability,
  calibration_table$observed_frequency,
  xlim = c(0, 1),
  ylim = c(0, 1),
  xlab = "Average judged probability",
  ylab = "Observed frequency",
  main = "Heuristic Judgment Calibration Diagram",
  pch = 19
)
abline(0, 1, lty = 2)
grid()
dev.off()

png(file.path(figures_dir, "review_rate_by_domain.png"), width = 1200, height = 800)
barplot(
  domain_summary$review_rate,
  names.arg = domain_summary$domain,
  las = 2,
  main = "Bias Review Rate by Domain",
  ylab = "Share of cases flagged for review"
)
grid()
dev.off()

print(overall_metrics)
print(bias_summary)
print(domain_summary)
print(calibration_table)
