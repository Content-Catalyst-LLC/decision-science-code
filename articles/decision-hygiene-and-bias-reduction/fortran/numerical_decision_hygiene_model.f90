! numerical_decision_hygiene_model.f90
! Compile with: gfortran numerical_decision_hygiene_model.f90 -o numerical_decision_hygiene_model

program numerical_decision_hygiene_model
  implicit none

  real :: pre_error
  real :: post_error
  real :: error_reduction
  real :: probability
  real :: outcome
  real :: brier

  pre_error = 0.20
  post_error = 0.08
  error_reduction = abs(pre_error) - abs(post_error)

  probability = 0.69
  outcome = 0.0
  brier = (probability - outcome) ** 2

  print *, "Error reduction:", error_reduction
  print *, "Brier score:", brier

end program numerical_decision_hygiene_model
