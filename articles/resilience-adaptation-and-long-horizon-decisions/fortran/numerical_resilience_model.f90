! numerical_resilience_model.f90
! Compile with: gfortran numerical_resilience_model.f90 -o numerical_resilience_model

program numerical_resilience_model
  implicit none

  real :: next_resilience_stock
  real :: resilient_decision_score
  logical :: revise

  next_resilience_stock = max(0.0, 35.0 + 3.0 + 2.0 - 1.0 - 1.6)
  resilient_decision_score = 0.30 * 0.80 + 0.24 * 0.79 + 0.22 * 0.74 + 0.18 * 1.0 - 0.06 * 0.10
  revise = (72.0 >= 80.0) .or. (24.0 <= 25.0)

  print *, "Next resilience stock:", next_resilience_stock
  print *, "Resilient decision score:", resilient_decision_score
  print *, "Revise?", revise

end program numerical_resilience_model
