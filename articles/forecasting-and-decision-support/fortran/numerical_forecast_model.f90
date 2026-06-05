! numerical_forecast_model.f90
! Compile with: gfortran numerical_forecast_model.f90 -o numerical_forecast_model

program numerical_forecast_model
  implicit none

  real :: probability
  real :: outcome
  real :: brier_score
  real :: false_positive_cost
  real :: false_negative_cost
  real :: threshold

  probability = 0.62
  outcome = 1.0
  false_positive_cost = 15.0
  false_negative_cost = 85.0

  brier_score = (probability - outcome) ** 2
  threshold = false_positive_cost / (false_positive_cost + false_negative_cost)

  print *, "Brier score:", brier_score
  print *, "Decision threshold:", threshold

end program numerical_forecast_model
