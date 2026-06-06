# bounded_rationality_workflow.R
# Base R workflow for satisficing, optimization comparison,
# search cost, aspiration drift, and bounded decision diagnostics.

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

n_cycles <- 500
n_options <- 12

domains <- c(
  "Public Policy",
  "Healthcare",
  "Financial Risk",
  "Infrastructure",
  "AI Governance",
  "Organizational Strategy"
)

decision_cases <- data.frame()

for (cycle in seq_len(n_cycles)) {
  domain <- sample(domains, 1)
  aspiration <- runif(1, 0.55, 0.82)
  search_cost <- runif(1, 0.005, 0.035)
  uncertainty_penalty <- runif(1, 0.00, 0.08)

  utilities <- pmin(pmax(rnorm(n_options, mean = 0.68, sd = 0.14), 0.05), 0.98)
  implementation_risk <- runif(n_options, 0.00, 0.20)
  adjusted_utility <- pmax(utilities - implementation_risk - uncertainty_penalty, 0.00)

  searched <- data.frame(
    cycle = cycle,
    domain = domain,
    option_id = seq_len(n_options),
    aspiration = aspiration,
    search_cost_per_option = search_cost,
    raw_utility = utilities,
    implementation_risk = implementation_risk,
    uncertainty_penalty = uncertainty_penalty,
    adjusted_utility = adjusted_utility,
    cumulative_search_cost = seq_len(n_options) * search_cost,
    stringsAsFactors = FALSE
  )

  searched$net_value <- searched$adjusted_utility - searched$cumulative_search_cost
  searched$satisfies_aspiration <- searched$adjusted_utility >= searched$aspiration

  decision_cases <- rbind(decision_cases, searched)
}

write.csv(
  decision_cases,
  file.path(tables_dir, "bounded_rationality_option_search_cases.csv"),
  row.names = FALSE
)

cycle_summary <- do.call(
  rbind,
  lapply(
    split(decision_cases, decision_cases$cycle),
    function(x) {
      optimizing_row <- x[which.max(x$adjusted_utility), ]

      if (any(x$satisfies_aspiration)) {
        satisficing_row <- x[which(x$satisfies_aspiration)[1], ]
        satisficing_found <- TRUE
      } else {
        satisficing_row <- x[which.max(x$adjusted_utility), ]
        satisficing_found <- FALSE
      }

      full_search_cost <- max(x$option_id) * unique(x$search_cost_per_option)
      optimizing_net_value <- optimizing_row$adjusted_utility - full_search_cost

      data.frame(
        cycle = unique(x$cycle),
        domain = unique(x$domain),
        aspiration = unique(x$aspiration),
        search_cost_per_option = unique(x$search_cost_per_option),
        optimizing_option = optimizing_row$option_id,
        optimizing_adjusted_utility = optimizing_row$adjusted_utility,
        optimizing_net_value = optimizing_net_value,
        satisficing_option = satisficing_row$option_id,
        satisficing_adjusted_utility = satisficing_row$adjusted_utility,
        satisficing_net_value = satisficing_row$net_value,
        satisficing_found = satisficing_found,
        search_length = satisficing_row$option_id,
        opportunity_loss = optimizing_row$adjusted_utility - satisficing_row$adjusted_utility,
        net_value_advantage = satisficing_row$net_value - optimizing_net_value,
        stringsAsFactors = FALSE
      )
    }
  )
)

cycle_summary$review_flag <- ifelse(
  cycle_summary$opportunity_loss > 0.20 |
    cycle_summary$search_length > 10 |
    !cycle_summary$satisficing_found,
  "review",
  "acceptable"
)

write.csv(
  cycle_summary,
  file.path(tables_dir, "bounded_rationality_cycle_summary.csv"),
  row.names = FALSE
)

domain_summary <- do.call(
  rbind,
  lapply(
    split(cycle_summary, cycle_summary$domain),
    function(x) {
      data.frame(
        domain = unique(x$domain),
        n_cycles = nrow(x),
        average_aspiration = mean(x$aspiration),
        average_search_length = mean(x$search_length),
        satisficing_found_rate = mean(x$satisficing_found),
        average_opportunity_loss = mean(x$opportunity_loss),
        average_net_value_advantage = mean(x$net_value_advantage),
        review_rate = mean(x$review_flag == "review"),
        stringsAsFactors = FALSE
      )
    }
  )
)

domain_summary <- domain_summary[order(-domain_summary$review_rate), ]

write.csv(
  domain_summary,
  file.path(tables_dir, "domain_bounded_rationality_summary.csv"),
  row.names = FALSE
)

# Adaptive aspiration simulation
n_periods <- 80
aspiration_path <- data.frame(
  period = seq_len(n_periods),
  aspiration = NA_real_,
  selected_value = NA_real_,
  search_length = NA_real_,
  feedback = NA_real_,
  stringsAsFactors = FALSE
)

aspiration_path$aspiration[1] <- 0.70
learning_rate <- 0.12
search_cost <- 0.02

for (t in 2:n_periods) {
  options <- pmin(pmax(rnorm(10, mean = 0.68, sd = 0.13), 0.05), 0.98)
  found_index <- which(options >= aspiration_path$aspiration[t - 1])

  if (length(found_index) > 0) {
    selected_index <- found_index[1]
  } else {
    selected_index <- which.max(options)
  }

  selected_value <- options[selected_index] - selected_index * search_cost
  feedback <- selected_value + rnorm(1, mean = 0, sd = 0.03)

  aspiration_path$selected_value[t] <- selected_value
  aspiration_path$search_length[t] <- selected_index
  aspiration_path$feedback[t] <- feedback
  aspiration_path$aspiration[t] <- pmin(
    pmax(
      aspiration_path$aspiration[t - 1] +
        learning_rate * (feedback - aspiration_path$aspiration[t - 1]),
      0.35
    ),
    0.95
  )
}

write.csv(
  aspiration_path,
  file.path(tables_dir, "adaptive_aspiration_path.csv"),
  row.names = FALSE
)

overall_metrics <- data.frame(
  metric = c(
    "average_search_length",
    "satisficing_found_rate",
    "average_opportunity_loss",
    "average_net_value_advantage",
    "review_rate",
    "final_adaptive_aspiration"
  ),
  value = c(
    mean(cycle_summary$search_length),
    mean(cycle_summary$satisficing_found),
    mean(cycle_summary$opportunity_loss),
    mean(cycle_summary$net_value_advantage),
    mean(cycle_summary$review_flag == "review"),
    tail(aspiration_path$aspiration, 1)
  ),
  stringsAsFactors = FALSE
)

write.csv(
  overall_metrics,
  file.path(tables_dir, "overall_bounded_rationality_metrics.csv"),
  row.names = FALSE
)

png(file.path(figures_dir, "search_length_by_domain.png"), width = 1200, height = 800)
barplot(
  domain_summary$average_search_length,
  names.arg = domain_summary$domain,
  las = 2,
  main = "Average Search Length by Domain",
  ylab = "Options searched before stopping"
)
grid()
dev.off()

png(file.path(figures_dir, "opportunity_loss_by_domain.png"), width = 1200, height = 800)
barplot(
  domain_summary$average_opportunity_loss,
  names.arg = domain_summary$domain,
  las = 2,
  main = "Average Opportunity Loss by Domain",
  ylab = "Optimizing utility minus satisficing utility"
)
grid()
dev.off()

png(file.path(figures_dir, "adaptive_aspiration_path.png"), width = 1200, height = 800)
plot(
  aspiration_path$period,
  aspiration_path$aspiration,
  type = "l",
  xlab = "Decision period",
  ylab = "Aspiration level",
  main = "Adaptive Aspiration Path"
)
lines(aspiration_path$period, aspiration_path$selected_value, lty = 2)
legend(
  "bottomright",
  legend = c("Aspiration", "Selected net value"),
  lty = c(1, 2)
)
grid()
dev.off()

print(overall_metrics)
print(domain_summary)
