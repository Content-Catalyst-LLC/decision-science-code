! numerical_calibration_model.f90
! Compile with: gfortran numerical_calibration_model.f90 -o numerical_calibration_model

program numerical_calibration_model
  implicit none

  real :: probability
  real :: outcome
  real :: brier_score

  probability = 0.72
  outcome = 1.0
  brier_score = (probability - outcome) ** 2

  print *, "Brier score:", brier_score

end program numerical_calibration_model
