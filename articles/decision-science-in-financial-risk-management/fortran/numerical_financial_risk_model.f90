! numerical_financial_risk_model.f90
! Compile with: gfortran numerical_financial_risk_model.f90 -o numerical_financial_risk_model

program numerical_financial_risk_model
  implicit none

  real :: losses(4)
  real :: probabilities(4)
  real :: expected_loss
  real :: capital_next

  losses = (/ -1.2, -4.8, -3.6, -6.2 /)
  probabilities = (/ 0.55, 0.20, 0.15, 0.10 /)

  expected_loss = sum(losses * probabilities)
  capital_next = max(20.0, 100.0 * (1.0 - 8.5 / 100.0))

  print *, "Expected loss:", expected_loss
  print *, "Capital next:", capital_next

end program numerical_financial_risk_model
