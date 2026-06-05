! historical_numerical_decision_model.f90
! Compile with: gfortran historical_numerical_decision_model.f90 -o historical_numerical_decision_model

program historical_numerical_decision_model
  implicit none

  real :: p(4)
  real :: aggressive(4), balanced(4), defensive(4), adaptive(4)

  p = (/0.42, 0.28, 0.18, 0.12/)
  aggressive = (/128.0, 50.0, -90.0, -20.0/)
  balanced = (/92.0, 68.0, 18.0, 42.0/)
  defensive = (/62.0, 58.0, 44.0, 54.0/)
  adaptive = (/88.0, 70.0, 36.0, 72.0/)

  print *, "Aggressive EV:", sum(p * aggressive)
  print *, "Balanced EV:", sum(p * balanced)
  print *, "Defensive EV:", sum(p * defensive)
  print *, "Adaptive EV:", sum(p * adaptive)

end program historical_numerical_decision_model
