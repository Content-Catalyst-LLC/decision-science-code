! numerical_risk_model.f90
! Compile with: gfortran numerical_risk_model.f90 -o numerical_risk_model

program numerical_risk_model
  implicit none

  real :: probabilities(3)
  real :: losses(3)
  real :: expected_loss

  probabilities = (/0.08, 0.06, 0.03/)
  losses = (/0.035, 0.040, 0.075/)

  expected_loss = sum(probabilities * losses)

  print *, "Expected loss:", expected_loss

end program numerical_risk_model
