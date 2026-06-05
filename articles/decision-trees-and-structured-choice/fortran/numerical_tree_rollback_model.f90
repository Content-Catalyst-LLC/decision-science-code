! numerical_tree_rollback_model.f90
! Compile with: gfortran numerical_tree_rollback_model.f90 -o numerical_tree_rollback_model

program numerical_tree_rollback_model
  implicit none

  real :: immediate_ev
  real :: staged_ev

  immediate_ev = 125.0 * 0.58 + (-35.0) * 0.42
  staged_ev = 145.0 * 0.54 + (-20.0) * 0.46 - 12.0 + 18.0

  print *, "Immediate EV:", immediate_ev
  print *, "Staged EV:", staged_ev
  print *, "Net value of staging:", staged_ev - immediate_ev

end program numerical_tree_rollback_model
