! statistical_decision_model.f90
! Compile with: gfortran statistical_decision_model.f90 -o statistical_decision_model

program statistical_decision_model
  implicit none

  real :: p(5)
  real :: optimize(5), balanced(5), robust(5)

  p = (/0.22, 0.34, 0.18, 0.16, 0.10/)
  optimize = (/145.0, 92.0, 30.0, -95.0, -40.0/)
  balanced = (/112.0, 84.0, 58.0, 12.0, 30.0/)
  robust = (/78.0, 72.0, 65.0, 48.0, 55.0/)

  print *, "Optimize EV:", sum(p * optimize)
  print *, "Balanced EV:", sum(p * balanced)
  print *, "Robust EV:", sum(p * robust)

end program statistical_decision_model
