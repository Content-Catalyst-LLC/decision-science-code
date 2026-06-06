! numerical_bias_model.f90
! Compile with: gfortran numerical_bias_model.f90 -o numerical_bias_model

program numerical_bias_model
  implicit none

  real :: anchor
  real :: evidence
  real :: weight
  real :: anchored_estimate
  real :: probability
  real :: outcome
  real :: brier_score

  anchor = 0.80
  evidence = 0.42
  weight = 0.45
  probability = 0.72
  outcome = 1.0

  anchored_estimate = weight * anchor + (1.0 - weight) * evidence
  brier_score = (probability - outcome) ** 2

  print *, "Anchored estimate:", anchored_estimate
  print *, "Brier score:", brier_score

end program numerical_bias_model
