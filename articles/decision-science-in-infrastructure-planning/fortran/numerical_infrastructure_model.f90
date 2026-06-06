! numerical_infrastructure_model.f90
! Compile with: gfortran numerical_infrastructure_model.f90 -o numerical_infrastructure_model

program numerical_infrastructure_model
  implicit none

  real :: values(5)
  real :: probabilities(5)
  real :: expected_value
  real :: worst_case

  values = (/ 76.0, 76.0, 82.0, 70.0, 78.0 /)
  probabilities = (/ 0.30, 0.20, 0.20, 0.15, 0.15 /)

  expected_value = sum(values * probabilities)
  worst_case = minval(values)

  print *, "Expected service value:", expected_value
  print *, "Worst-case value:", worst_case
  print *, "Adaptive trigger reached:", 0.74 >= 0.70

end program numerical_infrastructure_model
