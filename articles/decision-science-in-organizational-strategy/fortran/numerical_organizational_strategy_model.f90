! numerical_organizational_strategy_model.f90
! Compile with: gfortran numerical_organizational_strategy_model.f90 -o numerical_organizational_strategy_model

program numerical_organizational_strategy_model
  implicit none

  real :: values(4)
  real :: probabilities(4)
  real :: expected_value
  real :: downside_robustness
  real :: robust_score

  values = (/ 68.0, 82.0, 89.0, 66.0 /)
  probabilities = (/ 0.25, 0.35, 0.20, 0.20 /)

  expected_value = sum(values * probabilities)
  downside_robustness = minval(values)
  robust_score = 0.36 * expected_value / 100.0 + 0.30 * downside_robustness / 100.0 + 0.20 * 0.84 + 0.14 * 0.82

  print *, "Expected strategic value:", expected_value
  print *, "Downside robustness:", downside_robustness
  print *, "Robust strategy score:", robust_score

end program numerical_organizational_strategy_model
