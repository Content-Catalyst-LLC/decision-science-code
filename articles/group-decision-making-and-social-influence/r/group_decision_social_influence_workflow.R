# group_decision_social_influence_workflow.R
# Base R workflow for group judgment, social influence,
# hidden-profile risk, dissent, collective error, and review tables.

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

n_groups <- 240
members_per_group <- 7

groups <- data.frame(
  group_id = seq_len(n_groups),
  domain = sample(domains, n_groups, replace = TRUE),
  true_value = runif(n_groups, 0.20, 0.85),
  authority_concentration = runif(n_groups, 0.10, 0.60),
  consensus_pressure = runif(n_groups, 0.05, 0.75),
  shared_information = sample(4:12, n_groups, replace = TRUE),
  unique_information = sample(1:10, n_groups, replace = TRUE),
  stringsAsFactors = FALSE
)

member_rows <- list()

for (g in seq_len(n_groups)) {
  group <- groups[g, ]

  expertise <- runif(members_per_group, 0.30, 0.95)
  status <- runif(members_per_group, 0.10, 0.95)

  status[1] <- max(status[1], 0.90)
  expertise[1] <- runif(1, 0.45, 0.90)

  independent_noise <- rnorm(
    members_per_group,
    mean = 0,
    sd = 0.22 * (1 - expertise)
  )

  independent_estimate <- pmin(
    pmax(group$true_value + independent_noise, 0.01),
    0.99
  )

  initial_majority <- mean(independent_estimate)

  influenced_estimate <- pmin(
    pmax(
      (1 - group$consensus_pressure) * independent_estimate +
        group$consensus_pressure * initial_majority,
      0.01
    ),
    0.99
  )

  raw_weight <- (1 - group$authority_concentration) * expertise +
    group$authority_concentration * status

  influence_weight <- raw_weight / sum(raw_weight)

  member_rows[[g]] <- data.frame(
    group_id = group$group_id,
    domain = group$domain,
    member_id = seq_len(members_per_group),
    expertise = expertise,
    status = status,
    independent_estimate = independent_estimate,
    influenced_estimate = influenced_estimate,
    influence_weight = influence_weight,
    true_value = group$true_value,
    stringsAsFactors = FALSE
  )
}

members <- do.call(rbind, member_rows)

write.csv(
  members,
  file.path(tables_dir, "group_member_estimates.csv"),
  row.names = FALSE
)

group_summary <- do.call(
  rbind,
  lapply(
    split(members, members$group_id),
    function(x) {
      group_meta <- groups[groups$group_id == unique(x$group_id), ]

      independent_group_estimate <- mean(x$independent_estimate)
      influenced_group_estimate <- sum(x$influenced_estimate * x$influence_weight)
      collective_error <- abs(influenced_group_estimate - unique(x$true_value))
      independent_error <- abs(independent_group_estimate - unique(x$true_value))

      dissent_ratio <- mean(abs(x$independent_estimate - independent_group_estimate) > 0.12)
      influence_concentration <- max(x$influence_weight)
      hidden_profile_risk <- group_meta$unique_information /
        (group_meta$shared_information + group_meta$unique_information)

      evidence_values <- c(group_meta$shared_information, group_meta$unique_information)
      evidence_prob <- evidence_values / sum(evidence_values)
      evidence_diversity <- -sum(evidence_prob * log(evidence_prob))

      data.frame(
        group_id = unique(x$group_id),
        domain = unique(x$domain),
        true_value = unique(x$true_value),
        independent_group_estimate = independent_group_estimate,
        influenced_group_estimate = influenced_group_estimate,
        independent_error = independent_error,
        collective_error = collective_error,
        social_influence_error_change = collective_error - independent_error,
        dissent_ratio = dissent_ratio,
        influence_concentration = influence_concentration,
        consensus_pressure = group_meta$consensus_pressure,
        authority_concentration = group_meta$authority_concentration,
        shared_information = group_meta$shared_information,
        unique_information = group_meta$unique_information,
        hidden_profile_risk = hidden_profile_risk,
        evidence_diversity = evidence_diversity,
        stringsAsFactors = FALSE
      )
    }
  )
)

group_summary$review_flag <- ifelse(
  group_summary$collective_error > 0.15 |
    group_summary$social_influence_error_change > 0.05 |
    group_summary$influence_concentration > 0.35 |
    group_summary$hidden_profile_risk > 0.45 |
    group_summary$consensus_pressure > 0.60,
  "review",
  "acceptable"
)

write.csv(
  group_summary,
  file.path(tables_dir, "group_decision_summary.csv"),
  row.names = FALSE
)

domain_summary <- do.call(
  rbind,
  lapply(
    split(group_summary, group_summary$domain),
    function(x) {
      data.frame(
        domain = unique(x$domain),
        n_groups = nrow(x),
        average_collective_error = mean(x$collective_error),
        average_independent_error = mean(x$independent_error),
        average_social_influence_error_change = mean(x$social_influence_error_change),
        average_dissent_ratio = mean(x$dissent_ratio),
        average_influence_concentration = mean(x$influence_concentration),
        average_hidden_profile_risk = mean(x$hidden_profile_risk),
        average_consensus_pressure = mean(x$consensus_pressure),
        review_rate = mean(x$review_flag == "review"),
        stringsAsFactors = FALSE
      )
    }
  )
)

domain_summary <- domain_summary[order(-domain_summary$review_rate), ]

write.csv(
  domain_summary,
  file.path(tables_dir, "domain_group_decision_summary.csv"),
  row.names = FALSE
)

review_queue <- group_summary[group_summary$review_flag == "review", ]

review_queue <- review_queue[order(
  -review_queue$collective_error,
  -review_queue$influence_concentration,
  -review_queue$hidden_profile_risk
), ]

write.csv(
  review_queue,
  file.path(tables_dir, "group_decision_review_queue.csv"),
  row.names = FALSE
)

overall_metrics <- data.frame(
  metric = c(
    "mean_collective_error",
    "mean_independent_error",
    "mean_social_influence_error_change",
    "mean_dissent_ratio",
    "mean_influence_concentration",
    "mean_hidden_profile_risk",
    "mean_consensus_pressure",
    "review_rate"
  ),
  value = c(
    mean(group_summary$collective_error),
    mean(group_summary$independent_error),
    mean(group_summary$social_influence_error_change),
    mean(group_summary$dissent_ratio),
    mean(group_summary$influence_concentration),
    mean(group_summary$hidden_profile_risk),
    mean(group_summary$consensus_pressure),
    mean(group_summary$review_flag == "review")
  ),
  stringsAsFactors = FALSE
)

write.csv(
  overall_metrics,
  file.path(tables_dir, "overall_group_decision_metrics.csv"),
  row.names = FALSE
)

png(file.path(figures_dir, "group_error_by_domain.png"), width = 1200, height = 800)
barplot(
  domain_summary$average_collective_error,
  names.arg = domain_summary$domain,
  las = 2,
  main = "Average Collective Error by Domain",
  ylab = "Average collective error"
)
grid()
dev.off()

png(file.path(figures_dir, "hidden_profile_risk_by_domain.png"), width = 1200, height = 800)
barplot(
  domain_summary$average_hidden_profile_risk,
  names.arg = domain_summary$domain,
  las = 2,
  main = "Hidden-Profile Risk by Domain",
  ylab = "Average hidden-profile risk"
)
grid()
dev.off()

png(file.path(figures_dir, "influence_concentration_vs_error.png"), width = 1200, height = 800)
plot(
  group_summary$influence_concentration,
  group_summary$collective_error,
  xlab = "Influence concentration",
  ylab = "Collective error",
  main = "Influence Concentration and Collective Error",
  pch = 19
)
grid()
dev.off()

print(overall_metrics)
print(domain_summary)
print(head(review_queue, 25))
