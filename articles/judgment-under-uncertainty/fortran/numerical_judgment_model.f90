! numerical_judgment_model.f90
! Compile with: gfortran numerical_judgment_model.f90 -o numerical_judgment_model

program numerical_judgment_model
  implicit none

  real :: prior
  real :: likelihood_true
  real :: likelihood_false
  real :: odds
  real :: posterior_odds
  real :: posterior
  real :: probability
  real :: outcome
  real :: brier_score

  prior = 0.35
  likelihood_true = 0.72
  likelihood_false = 0.28
  probability = 0.62
  outcome = 1.0

  odds = prior / (1.0 - prior)
  posterior_odds = odds * (likelihood_true / likelihood_false)
  posterior = posterior_odds / (1.0 + posterior_odds)
  brier_score = (probability - outcome) ** 2

  print *, "Posterior:", posterior
  print *, "Brier score:", brier_score

end program numerical_judgment_model
