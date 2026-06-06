! numerical_cascade_model.f90
! Compile with: gfortran numerical_cascade_model.f90 -o numerical_cascade_model

program numerical_cascade_model
  implicit none

  real :: cascade_risk_score
  real :: effective_stress
  logical :: threshold_failure

  cascade_risk_score = 0.22 * 0.82 + 0.22 * 0.88 + 0.20 * 0.76 + 0.18 * 0.79 - 0.09 * 0.42 - 0.09 * 0.40
  effective_stress = 0.52 + 0.18 + max(0.0, 0.40 - 0.31)
  threshold_failure = effective_stress >= 0.66

  print *, "Cascade risk score:", cascade_risk_score
  print *, "Effective stress:", effective_stress
  print *, "Threshold failure?", threshold_failure

end program numerical_cascade_model
