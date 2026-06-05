! numerical_decision_model.f90
! Compile with: gfortran numerical_decision_model.f90 -o numerical_decision_model

program numerical_decision_model
  implicit none

  real :: probabilities(3)
  real :: optimize(3), hedge(3), preserve(3)

  probabilities = (/0.40, 0.35, 0.25/)
  optimize = (/120.0, 25.0, -80.0/)
  hedge = (/90.0, 62.0, 12.0/)
  preserve = (/66.0, 58.0, 42.0/)

  print *, "Optimize EV:", sum(optimize * probabilities)
  print *, "Hedge EV:", sum(hedge * probabilities)
  print *, "Preserve Option EV:", sum(preserve * probabilities)

end program numerical_decision_model
