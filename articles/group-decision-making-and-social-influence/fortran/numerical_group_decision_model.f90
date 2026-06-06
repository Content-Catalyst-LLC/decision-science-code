! numerical_group_decision_model.f90
! Compile with: gfortran numerical_group_decision_model.f90 -o numerical_group_decision_model

program numerical_group_decision_model
  implicit none

  real :: group_estimate
  real :: true_value
  real :: collective_error
  real :: shared_information
  real :: unique_information
  real :: hidden_profile_risk

  group_estimate = 0.64
  true_value = 0.62
  shared_information = 5.0
  unique_information = 9.0

  collective_error = abs(group_estimate - true_value)
  hidden_profile_risk = unique_information / (shared_information + unique_information)

  print *, "Collective error:", collective_error
  print *, "Hidden-profile risk:", hidden_profile_risk

end program numerical_group_decision_model
