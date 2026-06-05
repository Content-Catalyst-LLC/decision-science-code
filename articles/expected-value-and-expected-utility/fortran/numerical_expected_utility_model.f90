! numerical_expected_utility_model.f90
! Compile with: gfortran numerical_expected_utility_model.f90 -o numerical_expected_utility_model

program numerical_expected_utility_model
  implicit none

  real :: outcomes(2)
  real :: probabilities(2)
  real :: expected_value
  real :: expected_utility

  outcomes = (/180.0, 40.0/)
  probabilities = (/0.60, 0.40/)

  expected_value = sum(outcomes * probabilities)
  expected_utility = sum(log(outcomes + 151.0) * probabilities)

  print *, "Expected value:", expected_value
  print *, "Expected utility rho=1:", expected_utility

end program numerical_expected_utility_model
