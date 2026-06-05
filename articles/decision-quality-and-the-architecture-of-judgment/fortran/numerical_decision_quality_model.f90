! numerical_decision_quality_model.f90
! Compile with: gfortran numerical_decision_quality_model.f90 -o numerical_decision_quality_model

program numerical_decision_quality_model
  implicit none

  real :: weights(9)
  real :: staged(9)
  real :: robust(9)

  weights = (/0.11,0.10,0.12,0.13,0.11,0.10,0.11,0.11,0.11/)
  staged = (/0.92,0.90,0.94,0.90,0.88,0.86,0.82,0.94,0.96/)
  robust = (/0.88,0.86,0.82,0.91,0.86,0.84,0.90,0.86,0.90/)

  print *, "Staged Learning Decision quality:", sum(weights * staged)
  print *, "Robust Adaptive Pathway quality:", sum(weights * robust)

end program numerical_decision_quality_model
