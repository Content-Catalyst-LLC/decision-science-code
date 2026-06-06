! numerical_sustainability_model.f90
! Compile with: gfortran numerical_sustainability_model.f90 -o numerical_sustainability_model

program numerical_sustainability_model
  implicit none

  real :: sustainability_value_score
  real :: resource_next
  real :: pressure_next
  logical :: threshold_breach

  sustainability_value_score = 0.22 * 0.61 + 0.20 * 0.74 - 0.12 * 0.49 + 0.18 * 0.82 + 0.12 * 0.66 + 0.16 * 0.82
  resource_next = max(0.0, 100.0 - 28.0 + 13.2)
  pressure_next = max(5.0, 28.0 + 0.60 - 0.050 * 8.0 + 0.030 * 5.0)
  threshold_breach = 34.0 < 35.0

  print *, "Sustainability value score:", sustainability_value_score
  print *, "Resource next:", resource_next
  print *, "Pressure next:", pressure_next
  print *, "Threshold breach?", threshold_breach

end program numerical_sustainability_model
