! numerical_future_decision_model.f90
! Compile with: gfortran numerical_future_decision_model.f90 -o numerical_future_decision_model

program numerical_future_decision_model
  implicit none

  real :: maturity

  maturity = max(0.0, min(1.0, 0.12 * 0.86 + 0.14 * 0.90 + 0.14 * 0.88 + 0.12 * 0.84 + &
       0.12 * 0.88 + 0.12 * 0.86 + 0.14 * 0.90 + 0.14 * 0.88 - 0.14 * 0.24))

  print *, "Future maturity:", maturity

end program numerical_future_decision_model
